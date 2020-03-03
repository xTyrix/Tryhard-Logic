#!/usr/bin/python3

import NinjaScraper as ninja
import FilterFactory as factory
import PoEInfos as poe

import math
import collections
from PIL import Image
from datetime import datetime

NAME = "GeneratedLogic"
LEAGUE = "Metamorph" # "Hardcore Metamorph" "Standard" "Hardcore"
THRESHOLDS = [1000, 100, 50, 10, 1, .1, .05]

UNIQUE_COLOR    = (175,  96,  37)
RARE_COLOR      = (255, 255, 119)
MAGIC_COLOR     = (136, 136, 255)
NORMAL_COLOR    = (200, 200, 200)
NO_COLOR        = (  0,   0,   0)
NUTRAL_COLOR    = (100, 100, 100)
CRAFTED_COLOR   = (184, 218, 242)
CORRUPTED_COLOR = (210,   0,   0)
QUEST_COLOR     = ( 74, 230,  58)
MAP_COLOR       = (200, 155, 155)
CARD_COLOR      = ( 14, 186, 255)
CURRENCY_COLOR  = (170, 158, 130)
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

# SHARDS = {"Alchemy":       "Orb of Alchemy",
#           "Alteration":    "Orb of Alteration",
#           "Transmutation": "Orb of Transmutation",
#           "Ancient":       "Ancient Orb",
#           "Annulment":     "Orb of Annulment",
#           "Binding":       "Orb of Binding",
#           "Chaos":         "Chaos Orb",
#           "Engineer's":    "Engineer's Orb",
#           "Exalted":       "Exalted Orb",
#           "Harbinger's":   "Harbinger's Orb",
#           "Horizon":       "Orb of Horizons",
#           "Mirror":        "Mirror of Kalandra",
#           "Regal":         "Regal Orb"}
# 
# NETS = ["Simple Rope Net",
#         "Reinforced Rope Net",
#         "Strong Rope Net",
#         "Simple Iron Net",
#         "Reinforced Iron Net",
#         "Strong Iron Net",
#         "Simple Steel Net",
#         "Reinforced Steel Net",
#         "Strong Steel Net",
#         "Thaumaturgical Net",
#         "Necromancy Net"]

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
	def __init__(self, name, conditions=[]):
		super().__init__()
		self.name       = name
		self.conditions = conditions

	def addToFilter(self, itemFilter):
		itemFilter.addLine(self.name, comment=True)
		itemFilter.indent += 1
		itemFilter.beginContinuousConditions(self.conditions)
		super().addToFilter(itemFilter)
		itemFilter.endContinuousConditions(self.conditions)
		itemFilter.indent -= 1

class Block(FilterComponent):
	def __init__(self, name, conditions, appearance, doShow=True, doContinue=False):
		self.name       = name
		self.conditions = conditions
		self.appearance = appearance
		self.doShow     = doShow
		self.doContinue = doContinue
		super().__init__()

	def addToFilter(self, itemFilter):
		itemFilter.addBlock(self.name, self.conditions, self.appearance, self.doShow, self.doContinue)

	def addComponent(self, component):
		assert False, "Cannot add components to Blocks!"

def getCategory(price, thresholds=THRESHOLDS):
	i = 0
	while i < len(thresholds) and price < thresholds[i]:
		i += 1
	return i

def addPriceCategoryBlocks(section, priceCategories, style, condition=poe.FILTER.CONDITION.BASE_TYPE, thresholds=THRESHOLDS):
	for i in range(8):
		if priceCategories[i]:
			section.addComponent(Block(PRICE_CATEGORY_NAMES[i], [factory.buildConditionString(condition, priceCategories[i])], style.appearances[i]))

def addBlocksWithStackSizes(section, infos, style, condition=poe.FILTER.CONDITION.BASE_TYPE, thresholds=THRESHOLDS):
	categorieGroups = {}
	baseGroup = [[] for j in range(len(thresholds)+1)]
	highestMaxStackSize = 1
	for line in infos:
		# TODO do properly
		if line[ninja.NAME] == "Perandus Coin":
			line[ninja.STACK_SIZE] = 1000
		category1 = getCategory(line[ninja.PRICE])
		baseGroup[category1].append(line[ninja.NAME])
		if ninja.STACK_SIZE in line:
			highestMaxStackSize = max(highestMaxStackSize, line[ninja.STACK_SIZE])
			for category in range(category1)[::-1]:
				amount = math.ceil(thresholds[category] / line[ninja.PRICE])
				if amount > line[ninja.STACK_SIZE]:
					break
				if not str(amount) in categorieGroups:
					categorieGroups[str(amount)] = [[] for j in range(len(thresholds)+1)]
				categorieGroups[str(amount)][category].append(line[ninja.NAME])
	if categorieGroups:
		stacksSection = Section("Stacks")
		section.addComponent(stacksSection)
	for i in range(1, highestMaxStackSize+1)[::-1]:
		if str(i) in categorieGroups:
			currentSection = Section(str(i), [factory.buildConditionString(poe.FILTER.CONDITION.STACK_SIZE, [poe.FILTER.GE, str(i)])])
			stacksSection.addComponent(currentSection)
			group = categorieGroups[str(i)]
			for j in range(8):
				if group[j]:
					currentSection.addComponent(Block(PRICE_CATEGORY_NAMES[j], [factory.buildConditionString(condition, group[j])], style.appearances[j]))
	for i in range(8):
		if baseGroup[i]:
			section.addComponent(Block(PRICE_CATEGORY_NAMES[i], [factory.buildConditionString(condition, baseGroup[i])], style.appearances[i]))

def regroup(json):
	newJson = {UNIQUE_QUESTS: {},
	           CARDS_:        priceLists[ninja.CARD],
	           INCUBATOR_:    priceLists[ninja.INCUBATOR],
	           UNIQUE_MAPS:   priceLists[ninja.FRAGMENT],
	           C:             {}}
# 
# 	newPriceLists[UNIQUE_QUESTS][PROPHECIES] = priceLists[ninja.PROPHECY]
# 	newPriceLists[UNIQUE_QUESTS][REMAINING]  = priceLists[ninja.SCARAB]
# 	newPriceLists[UNIQUE_QUESTS][REMAINING]["Divine Vessel"] = newPriceLists[UNIQUE_MAPS].pop("Divine Vessel")
# 
# 	newPriceLists[C][INFLUENCED_C]  = {}
# 	newPriceLists[C][UNIQUE_C]      = priceLists[ninja.OIL]
# 	newPriceLists[C][UNIQUE_C].update(priceLists[ninja.FOSSIL])
# 	newPriceLists[C][UNIQUE_C].update(priceLists[ninja.ESSENCE])
# 	newPriceLists[C][REMAINING]     = priceLists[ninja.RESONATOR]
# 
# 	for item in priceLists[ninja.CURRENCY]:
# 		if item.find("'s Exalted Orb") != -1 or item == "Awakener's Orb":
# 			newPriceLists[C][INFLUENCED_C][item] = priceLists[ninja.CURRENCY][item]
# 		elif item.find("Blessing") != -1 or item.find("Catalyst") != -1:
# 			newPriceLists[C][UNIQUE_C][item] = priceLists[ninja.CURRENCY][item]
# 		elif item == "Stacked Deck":
# 			newPriceLists[CARDS_][item] = priceLists[ninja.CURRENCY][item]
# 		elif item.find("Splinter") != -1:
# 			newPriceLists[UNIQUE_MAPS][item] = priceLists[ninja.CURRENCY][item]
# 		elif item.find("Shard") == -1 and item.find("Fragment") == -1:
# 			newPriceLists[C][REMAINING][item] = priceLists[ninja.CURRENCY][item]
# 
# 	for shard in SHARDS:
# 		newPriceLists[C][REMAINING][shard + " Shard"] = priceLists[ninja.CURRENCY][SHARDS[shard]]/20
# 	newPriceLists[C][REMAINING]["Scroll Fragment"] = priceLists[ninja.CURRENCY]["Scroll of Wisdom"]/5
# 	newPriceLists[C][REMAINING]["Albino Rhoa Feather"] = THRESHOLDS[0]
# 	newPriceLists[C][REMAINING]["Eternal Orb"] = THRESHOLDS[0]
# 	newPriceLists[C][REMAINING]["Unshaping Orb"] = 20*newPriceLists[C][REMAINING]["Cartographer's Chisel"] + 5*newPriceLists[C][REMAINING]["Orb of Regret"]
# 	newPriceLists[C][REMAINING]["Apprentice Cartographer's Seal"] = 3*newPriceLists[C][REMAINING]["Simple Sextant"] + newPriceLists[C][REMAINING]["Orb of Scouring"]
# 	newPriceLists[C][REMAINING]["Journeyman Cartographer's Seal"] = 3*newPriceLists[C][REMAINING]["Prime Sextant"] + newPriceLists[C][REMAINING]["Orb of Scouring"]
# 	newPriceLists[C][REMAINING]["Master Cartographer's Seal"] = 3*newPriceLists[C][REMAINING]["Awakened Sextant"] + newPriceLists[C][REMAINING]["Orb of Scouring"]
# 	for net in NETS:
# 		newPriceLists[C][REMAINING][net] = newPriceLists[C][REMAINING]["Scroll Fragment"]
# 
# 	newPriceLists[UNIQUE_QUESTS][REMAINING][ninja.IVORY_WATCHSTONE] = priceLists[ninja.OTHER_CATEGORY][ninja.IVORY_WATCHSTONE]
# 	return newPriceLists

#                               primaryColor    secondaryColor   iconColor             iconShape
uniqueQuestStyle        = Style(QUEST_COLOR,    UNIQUE_COLOR,    poe.ICON.COLOR.GREEN, poe.ICON.SHAPE.TRIANGLE)
questStyle              = Style(QUEST_COLOR,    None,            poe.ICON.COLOR.GREEN, poe.ICON.SHAPE.TRIANGLE)
uniqueMapStyle          = Style(MAP_COLOR,      UNIQUE_COLOR,    poe.ICON.COLOR.BROWN, poe.ICON.SHAPE.SQUARE)
mapStyle                = Style(MAP_COLOR,      None,            None,                 poe.ICON.SHAPE.SQUARE)
cardStyle               = Style(CARD_COLOR,     None,            None,                 poe.ICON.SHAPE.STAR)
influencedCurrencyStyle = Style(CURRENCY_COLOR, INFLUENCE_COLOR, poe.ICON.COLOR.BLUE,  poe.ICON.SHAPE.DIAMOND)
uniqueCurrencyStyle     = Style(CURRENCY_COLOR, UNIQUE_COLOR,    poe.ICON.COLOR.BROWN, poe.ICON.SHAPE.DIAMOND)
currencyStyle           = Style(CURRENCY_COLOR, None,            None,                 poe.ICON.SHAPE.DIAMOND)
errorStyle              = Style(ERROR_COLOR_1,  ERROR_COLOR_2,   poe.ICON.COLOR.RED,   poe.ICON.SHAPE.TRIANGLE)

styles = [uniqueQuestStyle, questStyle, uniqueMapStyle, mapStyle, cardStyle, influencedCurrencyStyle, uniqueCurrencyStyle, currencyStyle, errorStyle]
styleSheet = StyleSheet(styles)
styleSheet.save()

filterInfo = ["League: " + LEAGUE]
filterInfo.append("Price Info from poe.ninja (" + datetime.now().strftime("%d.%m.%Y - %H:%M") + ")")
itemFilter = factory.ItemFilter(NAME, information=filterInfo)

# Main Section
mainSection        = Section("Actual Filter")
ninjaSection       = Section("Ninja Section (generated)")
handCraftedSection = Section("Hand Written (kind of)")
mainSection.addComponent(ninjaSection)
mainSection.addComponent(handCraftedSection)

# Ninja Section
json = ninja.scrapeAll(LEAGUE)
cardSection     = Section("Divination Cards & Incubator", [factory.buildConditionString(poe.FILTER.CONDITION.CLASS, [poe.CLASS.CARD, poe.CLASS.INCUBATOR])])
mapSection      = Section("Maps",                         [factory.buildConditionString(poe.FILTER.CONDITION.CLASS, [poe.CLASS.ALL_MAP_ITEMS])])
currencySection = Section("Currency",                     [factory.buildConditionString(poe.FILTER.CONDITION.CLASS, [poe.CLASS.CURRENCY])])
ninjaSection.addComponent(cardSection)
ninjaSection.addComponent(currencySection)
ninjaSection.addComponent(mapSection)

# Map Section
uniqueMapSection = Section("Unique Maps")
mapSection.addComponent(uniqueMapSection)
addBlocksWithStackSizes(uniqueMapSection, json[ninja.FRAGMENT] +
                                          json[ninja.SCARAB],  uniqueMapStyle)

# Cards and Incubator
addBlocksWithStackSizes(cardSection, json[ninja.INCUBATOR] +
                                     json[ninja.CARD],     cardStyle)

# Currency Section
influencedCurrencySection = Section("Influenced Currency")
uniqueCurrencySection     = Section("Targeted Currency")
currencySection.addComponent(influencedCurrencySection)
currencySection.addComponent(uniqueCurrencySection)
# TODO fill influencedCurrencySection
addBlocksWithStackSizes(uniqueCurrencySection, json[ninja.OIL] + # TODO baseType for some
                                               json[ninja.FOSSIL] +
                                               json[ninja.ESSENCE],    uniqueCurrencyStyle)
addBlocksWithStackSizes(currencySection,       json[ninja.CURRENCY] +
                                               json[ninja.RESONATOR], currencyStyle)

mainSection.addToFilter(itemFilter)
itemFilter.write()
