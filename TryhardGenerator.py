#!/usr/bin/python3

import NinjaScraper as ninja
import FilterFactory as factory
import PoEInfos as poe

import math
import collections
from PIL import Image
from datetime import datetime

NAME = "GeneratedLogic"
LEAGUE = "Delirium" # "Hardcore Delirium" "Standard" "Hardcore"
# TODO       [1000, 100, 10, 1, .5, .1, .05] ?
THRESHOLDS = [1000, 100, 50, 10, 1, .1, .05]

# TODO tweak color palette
# name             rgb              hsl
UNIQUE_COLOR    = (175,  96,  37) #  26°  65.1%  41.6%
RARE_COLOR      = (255, 255, 119) #  60° 100.0%  73.3%
MAGIC_COLOR     = (136, 136, 255) # 240° 100.0%  76.7%
NORMAL_COLOR    = (200, 200, 200) #   -    0.0%  78.4%
NO_COLOR        = (  0,   0,   0)
NUTRAL_COLOR    = (100, 100, 100)
CRAFTED_COLOR   = (184, 218, 242)
CORRUPTED_COLOR = (210,   0,   0)
QUEST_COLOR     = ( 74, 230,  58)
MAP_COLOR       = (200, 155, 155)
CARD_COLOR      = ( 14, 186, 255)
CURRENCY_COLOR  = (170, 158, 130) #  42°  19.0%  58.8%
GEM_COLOR       = ( 27, 162, 155)
INFLUENCE_COLOR = (127,   0, 255)
OMG_COLOR       = (127,   0, 127)
VENDOR_COLOR    = (  0, 127,   0)
ERROR_COLOR_1   = (255,   0,   0)
ERROR_COLOR_2   = (255, 255, 255)

OMG_SIZE       = 45
ERROR_SIZE     = 44
VERY_HIGH_SIZE = 36
HIGH_SIZE      = 33
NORMAL_SIZE    = 30
LOW_SIZE       = 27
HIDE_SIZE      = 18

PRICE_CATEGORY_NAMES = ["OMFG (>= 1000C)", "OMG (>= 100C)", "Very High (>= 50C)", "High (>= 10C)", "normal (>= 1C)", "low (>= .1C)", "very low (>= .05C)", "rest (< .05C)"]

class Style:
	def __init__(self, primaryColor, secondaryColor=None, iconColor=None, iconShape=poe.ICON.SHAPE.HEXAGON):
		lowPrimaryColor = primaryColor
		if secondaryColor:
			lowSecondaryColor    = secondaryColor
			normalPrimaryColor   = secondaryColor
			normalSecondaryColor = primaryColor
		else:
			lowSecondaryColor    = NO_COLOR
			normalPrimaryColor   = primaryColor
			normalSecondaryColor = NO_COLOR
		highPrimaryColor   = OMG_COLOR
		highSecondaryColor = primaryColor
		if iconColor:
			lowIconColor  = iconColor
			highIconColor = iconColor
		else:
			lowIconColor  = poe.ICON.COLOR.WHITE
			highIconColor = poe.ICON.COLOR.YELLOW
		iconShape = iconShape

		self.appearances = []

		# OMFG
		display = factory.Display(highSecondaryColor, highPrimaryColor, highSecondaryColor, OMG_SIZE)
		effect  = factory.Effect(poe.EFFECT.COLOR.RED)
		icon    = factory.Icon(poe.ICON.SIZE.LARGE, poe.ICON.COLOR.RED, iconShape)
		self.appearances.append(factory.Appearance(display, effect, icon))

		# OMG
		display = factory.Display(highPrimaryColor, highSecondaryColor, highPrimaryColor, OMG_SIZE)
		effect  = factory.Effect(poe.EFFECT.COLOR.RED)
		icon    = factory.Icon(poe.ICON.SIZE.LARGE, poe.ICON.COLOR.RED, iconShape)
		self.appearances.append(factory.Appearance(display, effect, icon))

		# Very High
		display = factory.Display(normalSecondaryColor, normalPrimaryColor, normalSecondaryColor, VERY_HIGH_SIZE)
		effect  = factory.Effect(highIconColor)
		icon    = factory.Icon(poe.ICON.SIZE.MEDIUM, highIconColor, iconShape)
		self.appearances.append(factory.Appearance(display, effect, icon))

		# High
		display = factory.Display(normalSecondaryColor, normalPrimaryColor, normalSecondaryColor, HIGH_SIZE)
		effect  = factory.Effect(lowIconColor)
		icon    = factory.Icon(poe.ICON.SIZE.SMALL, lowIconColor, iconShape)
		self.appearances.append(factory.Appearance(display, effect, icon))

		# normal
		display = factory.Display(normalPrimaryColor, normalSecondaryColor, normalPrimaryColor, NORMAL_SIZE)
		effect  = factory.Effect(lowIconColor, temp=True)
		self.appearances.append(factory.Appearance(display, effect))

		# low
		display = factory.Display(lowPrimaryColor, NO_COLOR, lowSecondaryColor, LOW_SIZE)
		self.appearances.append(factory.Appearance(display))

		# very low
		display = factory.Display(lowPrimaryColor, NO_COLOR, NO_COLOR, LOW_SIZE)
		self.appearances.append(factory.Appearance(display))

		#rest
		display = factory.Display(lowPrimaryColor, NO_COLOR, NO_COLOR, HIDE_SIZE)
		self.appearances.append(factory.Appearance(display))

class StyleSheet:
	def __init__(self, styles=[]):
		self.X = 5
		self.Y = 5
		self.styles = styles

	def addStyle(self, style):
		self.styles.append(style)

	def addStyles(self, styles):
		self.styles += styles

	def addItem(self, display, symbol):
		f = [] # from
		t = [] # to
		for i in range(18):
			f.append(round((    i*display.fontSize)/18))
			t.append(round(((i+1)*display.fontSize)/18))
		self.image.paste(display.borderColor,     (self.X+f[ 0], self.Y+f[ 0], self.X+t[17], self.Y+t[17]))
		self.image.paste(display.backgroundColor, (self.X+f[ 2], self.Y+f[ 2], self.X+t[15], self.Y+t[15]))
		if symbol == "F":
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 4], self.X+t[ 7], self.Y+t[13]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 4], self.X+t[11], self.Y+t[ 5]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 8], self.X+t[ 9], self.Y+t[ 9]))
		elif symbol == "I":
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 4], self.X+t[11], self.Y+t[ 5]))
			self.image.paste(display.textColor,   (self.X+f[ 8], self.Y+f[ 4], self.X+t[ 9], self.Y+t[13]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[12], self.X+t[11], self.Y+t[13]))
		elif symbol == "L":
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 4], self.X+t[ 7], self.Y+t[13]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[12], self.X+t[11], self.Y+t[13]))
		elif symbol == "T":
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 4], self.X+t[11], self.Y+t[ 5]))
			self.image.paste(display.textColor,   (self.X+f[ 8], self.Y+f[ 4], self.X+t[ 9], self.Y+t[13]))
		elif symbol == "E":
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 4], self.X+t[ 7], self.Y+t[13]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 4], self.X+t[11], self.Y+t[ 5]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 8], self.X+t[ 9], self.Y+t[ 9]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[12], self.X+t[11], self.Y+t[13]))
		elif symbol == "R":
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 4], self.X+t[ 7], self.Y+t[13]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 4], self.X+t[10], self.Y+t[ 5]))
			self.image.paste(display.textColor,   (self.X+f[10], self.Y+f[ 5], self.X+t[11], self.Y+t[ 8]))
			self.image.paste(display.textColor,   (self.X+f[ 8], self.Y+f[ 8], self.X+t[10], self.Y+t[ 9]))
			self.image.paste(display.textColor,   (self.X+f[ 9], self.Y+f[ 9], self.X+t[10], self.Y+t[10]))
			self.image.paste(display.textColor,   (self.X+f[10], self.Y+f[10], self.X+t[11], self.Y+t[13]))
		elif symbol == "$":
			self.image.paste(display.textColor,   (self.X+f[11], self.Y+f[ 6], self.X+t[11], self.Y+t[ 6]))
			self.image.paste(display.textColor,   (self.X+f[ 7], self.Y+f[ 5], self.X+t[10], self.Y+t[ 6]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[ 6], self.X+t[ 7], self.Y+t[ 8]))
			self.image.paste(display.textColor,   (self.X+f[ 7], self.Y+f[ 8], self.X+t[10], self.Y+t[ 9]))
			self.image.paste(display.textColor,   (self.X+f[10], self.Y+f[ 9], self.X+t[11], self.Y+t[11]))
			self.image.paste(display.textColor,   (self.X+f[ 7], self.Y+f[11], self.X+t[10], self.Y+t[12]))
			self.image.paste(display.textColor,   (self.X+f[ 6], self.Y+f[11], self.X+t[ 6], self.Y+t[11]))
			self.image.paste(display.textColor,   (self.X+f[ 9], self.Y+f[ 4], self.X+t[ 9], self.Y+t[ 8]))
			self.image.paste(display.textColor,   (self.X+f[ 8], self.Y+f[10], self.X+t[ 8], self.Y+t[13]))
		else:
			assert False, "Unsupported symbol: " + symbol
		self.X += display.fontSize + 10

	def addLine(self, style):
		symbols = "$FILTER$"
		for i in range(8):
			self.addItem(style.appearances[i].display, symbols[i])

		self.X = 5
		self.Y += OMG_SIZE+10

	def save(self, name="Stylesheet"):
		width  = 2*OMG_SIZE + VERY_HIGH_SIZE + HIGH_SIZE + NORMAL_SIZE + 2*LOW_SIZE + HIDE_SIZE + 8*10
		height = (OMG_SIZE+10)*len(styles)
		self.image = Image.new("RGB", (width, height), (68, 68, 68))
		for style in self.styles:
			self.addLine(style)
		self.image.save("./" + name + ".png", "PNG")

class FilterComponent:
	def __init__(self):
		self.components = []

	def addToFilter(self, itemFilter):
		for component in self.components:
			component.addToFilter(itemFilter)

	def addComponent(self, component):
		self.components.append(component)

class Section(FilterComponent):
	def __init__(self, name, conditions=[], exceptions=[]):
		super().__init__()
		self.name       = name
		self.conditions = conditions
		self.exceptions = exceptions

	def addToFilter(self, itemFilter):
		itemFilter.addLine(self.name, comment=True)
		itemFilter.indent += 1
		itemFilter.endContinuousConditions(self.exceptions)
		itemFilter.beginContinuousConditions(self.conditions)
		super().addToFilter(itemFilter)
		itemFilter.endContinuousConditions(self.conditions)
		itemFilter.beginContinuousConditions(self.exceptions)
		itemFilter.indent -= 1

class Block(FilterComponent):
	def __init__(self, name, conditions, appearance, doShow=True, doContinue=False, comments=[]):
		self.name       = name
		self.conditions = conditions
		self.appearance = appearance
		self.doShow     = doShow
		self.doContinue = doContinue
		self.comments   = comments
		super().__init__()

	def addToFilter(self, itemFilter):
		itemFilter.addBlock(self.name, self.conditions, self.appearance, self.doShow, self.doContinue, self.comments)

	def addComponent(self, component):
		assert False, "Cannot add components to Blocks!"

def getCategory(price, thresholds=THRESHOLDS):
	i = 0
	while i < len(thresholds) and price < thresholds[i]:
		i += 1
	return i

def addPriceCategoryBlocks(section, infoCategories, style, thresholds=THRESHOLDS):
	for i in range(8):
		if infoCategories[i]:
			if ninja.BASE_TYPE in infoCategories[i][0]:
				assert ninja.PROPHECY not in infoCategories[i][0], "Found item group with \"" + ninja.BASE_TYPE + "\" and \"" + ninja.PROPHECY + "\" entries! Don't know what to do."
				condition = poe.FILTER.CONDITION.BASE_TYPE
				info = ninja.BASE_TYPE
			else:
				assert ninja.PROPHECY in infoCategories[i][0], "Unsupported Item Group! Only groups with \"" + ninja.BASE_TYPE + "\" or \"" + ninja.PROPHECY + "\" entries are supported."
				condition = poe.FILTER.CONDITION.PROPHECY
				info = ninja.PROPHECY
			section.addComponent(Block(PRICE_CATEGORY_NAMES[i], [factory.buildConditionString(condition, [line[info] for line in infoCategories[i]])], style.appearances[i]))

def addBlocks(section, infos, style, thresholds=THRESHOLDS):
	group = [[] for j in range(len(thresholds)+1)]
	for name in infos:
		group[getCategory(infos[name][ninja.PRICE])].append(infos[name])
	addPriceCategoryBlocks(section, group, style, thresholds)

# TODO stack size Rundungsfehler prüfen
def addBlocksWithStackSizes(section, infos, style, thresholds=THRESHOLDS, disableStacks=False):
	categorieGroups = {}
	baseGroup = [[] for j in range(len(thresholds)+1)]
	highestMaxStackSize = 1
	for name in infos:
		category1 = getCategory(infos[name][ninja.PRICE])
		baseGroup[category1].append(infos[name])
		highestMaxStackSize = max(highestMaxStackSize, poe.getStackSize(name))
		for category in range(category1)[::-1]:
			amount = math.ceil(thresholds[category] / infos[name][ninja.PRICE])
			if amount > poe.getStackSize(name):
				break
			if not str(amount) in categorieGroups:
				categorieGroups[str(amount)] = [[] for j in range(len(thresholds)+1)]
			categorieGroups[str(amount)][category].append(infos[name])
	if categorieGroups:
		stacksSection = Section("Stacks")
		section.addComponent(stacksSection)
	for i in range(2, highestMaxStackSize+1)[::-1]:
		if str(i) in categorieGroups:
			currentSection = Section(str(i), [factory.buildConditionString(poe.FILTER.CONDITION.STACK_SIZE, [poe.FILTER.GE, str(i)])])
			stacksSection.addComponent(currentSection)
			addPriceCategoryBlocks(currentSection, categorieGroups[str(i)], style, thresholds)
	addPriceCategoryBlocks(section, baseGroup, style, thresholds)

C = "Currency"
PROPHECIES = "Prophecies (displayed as Unique Quests)"
CARDS_C = "Stacked Decks (displayed as Divination Card)"
FRAGMENTS_C = "Splinter (displayed as Unique Maps)"
INFLUENCED_C = "Influenced Currency"
UNIQUE_C = "Targeted Currency"
UNIQUE_QUESTS = "Scarabs & Divine Vessels (displayed as Unique Quests)"
MAPS = "Maps"
UNIQUE_MAPS = "Unique Maps"
FRAGMENTS = "Map Fragments"
CARDS = "Divination Cards"
INCUBATOR = "Incubator"
WATCHSTONES = "Watchstones"
IVORY_WATCHSTONES = "Ivory Watchstones"

OTHER = "Remaining "
ERROR = " ERROR"

def getMaxIvoryWatchstones(json):
	maxCategory = 7
	iwsList = []
	for name in json:
		if getCategory(json[name][ninja.PRICE]) <= maxCategory:
			maxCategory = getCategory(json[name][ninja.PRICE])
			iwsList.append(name)
	return (maxCategory, iwsList)

# TODO don't froce override things if existing
def regroup(json):
	newJson = {}
	newJson[PROPHECIES]    = json[ninja.PROPHECY]
	newJson[UNIQUE_QUESTS] = json[ninja.SCARAB]
	newJson[UNIQUE_QUESTS].update({"Divine Vessel": json[ninja.FRAGMENT].pop("Divine Vessel")})
	newJson[CARDS]         = json[ninja.CARD]
	newJson[INCUBATOR]     = json[ninja.INCUBATOR]
	newJson[CARDS_C]       = {"Stacked Deck": json[ninja.CURRENCY].pop("Stacked Deck")}
	newJson[FRAGMENTS]     = {}
	newJson[FRAGMENTS_C]   = {}
	newJson[UNIQUE_MAPS]   = json[ninja.U_MAP]
	if "Awakener's Orb" in json[ninja.CURRENCY]:
		newJson[INFLUENCED_C] = {"Awakener's Orb": json[ninja.CURRENCY].pop("Awakener's Orb")}
	else:
		newJson[INFLUENCED_C] = {}
	newJson[UNIQUE_C]      = json[ninja.OIL]
	newJson[UNIQUE_C].update(json[ninja.FOSSIL])
	newJson[UNIQUE_C].update(json[ninja.ESSENCE])
	newJson[UNIQUE_C].update(json[ninja.VIAL])
	newJson[WATCHSTONES]   = json[ninja.WATCHSTONE]
	newJson[C]             = json[ninja.RESONATOR]
	for item in json[ninja.FRAGMENT]:
		if item.find("Splinter") != -1:
			newJson[FRAGMENTS_C][item] = json[ninja.FRAGMENT][item]
		else:
			newJson[FRAGMENTS][item] = json[ninja.FRAGMENT][item]
	for item in json[ninja.CURRENCY]:
		if item.find("'s Exalted Orb") != -1 or item.find("Delirium Orb") != -1:
			newJson[INFLUENCED_C][item] = json[ninja.CURRENCY][item]
		elif item.find("Blessing") != -1 or item.find("Catalyst") != -1:
			newJson[UNIQUE_C][item] = json[ninja.CURRENCY][item]
		elif item.find("Splinter") != -1:
			newJson[FRAGMENTS_C][item] = json[ninja.CURRENCY][item]
		else:
			newJson[C][item] = json[ninja.CURRENCY][item]

	for shard in poe.SHARDS:
		if shard not in newJson[C]:
			newJson[C][shard] = {ninja.PRICE: json[ninja.CURRENCY][poe.SHARDS[shard]][ninja.PRICE]/poe.STACK_SIZES[shard],
			                     ninja.BASE_TYPE: shard}
	newJson[C]["Albino Rhoa Feather"] = {ninja.PRICE: THRESHOLDS[0],
	                                     ninja.BASE_TYPE: "Albino Rhoa Feather"}
	newJson[C]["Eternal Orb"] = {ninja.PRICE: THRESHOLDS[0],
	                             ninja.BASE_TYPE: "Eternal Orb"}
	newJson[C]["Unshaping Orb"] = {ninja.PRICE: 20*json[ninja.CURRENCY]["Cartographer's Chisel"][ninja.PRICE] +
	                                             5*json[ninja.CURRENCY]["Orb of Regret"][ninja.PRICE],
	                               ninja.BASE_TYPE: "Unshaping Orb"}
	newJson[C]["Apprentice Cartographer's Seal"] = {ninja.PRICE: 3*json[ninja.CURRENCY]["Simple Sextant"][ninja.PRICE] +
	                                                               json[ninja.CURRENCY]["Orb of Scouring"][ninja.PRICE],
	                                                ninja.BASE_TYPE: "Apprentice Cartographer's Seal"}
	newJson[C]["Journeyman Cartographer's Seal"] = {ninja.PRICE: 3*json[ninja.CURRENCY]["Prime Sextant"][ninja.PRICE] +
	                                                               json[ninja.CURRENCY]["Orb of Scouring"][ninja.PRICE],
	                                                ninja.BASE_TYPE: "Journeyman Cartographer's Seal"}
	newJson[C]["Master Cartographer's Seal"] = {ninja.PRICE: 3*json[ninja.CURRENCY]["Awakened Sextant"][ninja.PRICE] +
	                                                           json[ninja.CURRENCY]["Orb of Scouring"][ninja.PRICE],
	                                            ninja.BASE_TYPE: "Master Cartographer's Seal"}
	for net in poe.NETS:
		newJson[C][net] = {ninja.PRICE: newJson[C]["Scroll Fragment"][ninja.PRICE],
		                   ninja.BASE_TYPE: net}
	return newJson

# Styles                        primaryColor    secondaryColor   iconColor             iconShape
uniqueQuestStyle        = Style(QUEST_COLOR,    UNIQUE_COLOR,    poe.ICON.COLOR.GREEN, poe.ICON.SHAPE.TRIANGLE)
questStyle              = Style(QUEST_COLOR,    None,            poe.ICON.COLOR.GREEN, poe.ICON.SHAPE.TRIANGLE)
uniqueMapStyle          = Style(MAP_COLOR,      UNIQUE_COLOR,    poe.ICON.COLOR.BROWN, poe.ICON.SHAPE.SQUARE)
mapStyle                = Style(MAP_COLOR,      None,            None,                 poe.ICON.SHAPE.SQUARE)
cardStyle               = Style(CARD_COLOR,     None,            None,                 poe.ICON.SHAPE.STAR)
influencedCurrencyStyle = Style(CURRENCY_COLOR, INFLUENCE_COLOR, poe.ICON.COLOR.BLUE,  poe.ICON.SHAPE.DIAMOND)
uniqueCurrencyStyle     = Style(CURRENCY_COLOR, UNIQUE_COLOR,    poe.ICON.COLOR.BROWN, poe.ICON.SHAPE.DIAMOND)
currencyStyle           = Style(CURRENCY_COLOR, None,            None,                 poe.ICON.SHAPE.DIAMOND)

tyrixErrorDisplay = factory.Display(ERROR_COLOR_1, ERROR_COLOR_2, ERROR_COLOR_1, ERROR_SIZE)
gggErrorDisplay = factory.Display(ERROR_COLOR_2, ERROR_COLOR_1, ERROR_COLOR_2, ERROR_SIZE)
errorEffect = factory.Effect(poe.EFFECT.COLOR.RED)
errorIcon = factory.Icon(poe.ICON.SIZE.LARGE, poe.ICON.COLOR.RED, poe.ICON.SHAPE.TRIANGLE)
tyrixErrorAppearance = factory.Appearance(tyrixErrorDisplay, errorEffect, errorIcon)
gggErrorAppearance = factory.Appearance(gggErrorDisplay, errorEffect, errorIcon)

mainQuestDisplay = factory.Display(NO_COLOR, QUEST_COLOR, NO_COLOR, VERY_HIGH_SIZE)
questEffect = factory.Effect(poe.EFFECT.COLOR.GREEN)
questIcon = factory.Icon(poe.ICON.SIZE.LARGE, poe.ICON.COLOR.GREEN, poe.ICON.SHAPE.TRIANGLE)
mainQuestAppearance = factory.Appearance(mainQuestDisplay, questEffect, questIcon)

# Infos
filterInfo = ["League: " + LEAGUE]
filterInfo.append("Price Info from poe.ninja (" + datetime.now().strftime("%d.%m.%Y - %H:%M") + ")")
itemFilter = factory.ItemFilter(NAME, information=filterInfo)

json = regroup(ninja.scrapeAll(LEAGUE))


# saving stylesheet file
styles = [uniqueQuestStyle, questStyle, uniqueMapStyle, mapStyle, cardStyle, influencedCurrencyStyle, uniqueCurrencyStyle, currencyStyle]
styleSheet = StyleSheet(styles)
styleSheet.save()


# Main Section
mainSection = Section("Actual Filter")

currencySection = Section(C, [factory.buildConditionString(poe.FILTER.CONDITION.CLASS, [poe.CLASS.CURRENCY])])
mainSection.addComponent(currencySection)

mapSection = Section(MAPS, [factory.buildConditionString(poe.FILTER.CONDITION.CLASS, [poe.CLASS.ALL_MAP_ITEMS])])
mainSection.addComponent(mapSection)

cardSection = Section(CARDS, [factory.buildConditionString(poe.FILTER.CONDITION.CLASS, [poe.CLASS.CARD])])
mainSection.addComponent(cardSection)

incubatorSection = Section(INCUBATOR, [factory.buildConditionString(poe.FILTER.CONDITION.CLASS, [poe.CLASS.INCUBATOR])])
mainSection.addComponent(incubatorSection)

watchstoneSection = Section(WATCHSTONES, [factory.buildConditionString(poe.FILTER.CONDITION.CLASS, [poe.CLASS.WATCHSTONE])])
mainSection.addComponent(watchstoneSection)


# Currency Section
prophecySection = Section(PROPHECIES)
currencySection.addComponent(prophecySection)
addBlocks(prophecySection, json[PROPHECIES], uniqueQuestStyle)

stackedDeckSection = Section(CARDS_C)
currencySection.addComponent(stackedDeckSection)
addBlocksWithStackSizes(stackedDeckSection, json[CARDS_C], cardStyle)

splinterSection = Section(FRAGMENTS_C)
currencySection.addComponent(splinterSection)
addBlocksWithStackSizes(splinterSection, json[FRAGMENTS_C], uniqueMapStyle)

influencedCurrencySection = Section(INFLUENCED_C)
currencySection.addComponent(influencedCurrencySection)
addBlocksWithStackSizes(influencedCurrencySection, json[INFLUENCED_C], influencedCurrencyStyle)

uniqueCurrencySection = Section(UNIQUE_C)
currencySection.addComponent(uniqueCurrencySection)
addBlocksWithStackSizes(uniqueCurrencySection, json[UNIQUE_C], uniqueCurrencyStyle)

addBlocksWithStackSizes(currencySection, json[C], currencyStyle)
currencySection.addComponent(Block(C+ERROR, [], tyrixErrorAppearance))


# Map Section
uniqueQuestSection = Section(UNIQUE_QUESTS)
mapSection.addComponent(uniqueQuestSection)
addBlocks(uniqueQuestSection, json[UNIQUE_QUESTS], uniqueQuestStyle)

fragmentSection = Section(FRAGMENTS)
mapSection.addComponent(fragmentSection)
addBlocks(fragmentSection, json[FRAGMENTS], uniqueMapStyle)

uniqueMapSection = Section(UNIQUE_MAPS, [factory.buildConditionString(poe.FILTER.CONDITION.RARITY, [poe.RARITY.UNIQUE])])
mapSection.addComponent(uniqueMapSection)
addBlocks(uniqueMapSection, json[UNIQUE_MAPS], uniqueMapStyle)

# mapSection.addComponent(Block(MAPS+ERROR, [], tyrixErrorAppearance))


# Card Section
addBlocksWithStackSizes(cardSection, json[CARDS], cardStyle)
cardSection.addComponent(Block(CARDS+ERROR, [], tyrixErrorAppearance))


# Incubator Section
addBlocks(incubatorSection, json[INCUBATOR], cardStyle)
incubatorSection.addComponent(Block(INCUBATOR+ERROR, [], tyrixErrorAppearance))


# Watchstone Section
maxIWSs = getMaxIvoryWatchstones(json[WATCHSTONES])
iwsComments = [PRICE_CATEGORY_NAMES[maxIWSs[0]], maxIWSs[1][0]]
for iws in maxIWSs[1][1:]:
	iwsComments[1] += ", " + iws
iwsConditions = [factory.buildConditionString(poe.FILTER.CONDITION.RARITY, [poe.RARITY.UNIQUE]),
                 factory.buildConditionString(poe.FILTER.CONDITION.BASE_TYPE, [poe.WATCHSTONE.IVORY])]
watchstoneSection.addComponent(Block(IVORY_WATCHSTONES, iwsConditions, uniqueQuestStyle.appearances[maxIWSs[0]], comments=iwsComments))
watchstoneSection.addComponent(Block(IVORY_WATCHSTONES+ERROR, iwsConditions[1:1], gggErrorAppearance))
watchstoneSection.addComponent(Block(OTHER+WATCHSTONES, [], mainQuestAppearance))


# ERROR (to see, what is missing)
# TODO remove when filter is done
# mainSection.addComponent(Block("Temporary"+ERROR, [], tyrixErrorAppearance))


# saving filter file
mainSection.addToFilter(itemFilter)
itemFilter.write()


# TODO Missed Curency
# "Bestiary Orb"
