#!/usr/bin/python3

COMMENT = "# "

SHOW = "Show "
HIDE = "Hide "

CLASS =            "Class             "
BASE_TYPE =        "BaseType          "
RARITY =           "Rarity            "
PROPHECY =         "Prophecy          "

TEXT_COLOR =       "SetTextColor      "
BACKGROUND_COLOR = "SetBackgroundColor"
BORDER_COLOR =     "SetBorderColor    "
FONT_SIZE =        "SetFontSize       "
ICON =             "MinimapIcon       "
EFFECT =           "PlayEffect        "

NO_ICON =          "# MinimapIcon      None"
NO_EFFECT =        "# PlayEffect       None"

TEMP = " Temp"

def buildFilter(baseStyle, priceLists, thresholds, styles, optionLists):
	itemFilter = ItemFilter(baseStyle)
	itemFilter.addLine("# Generated Filter")
	itemFilter.indent += 1
	for name in priceLists:
		priceCategories = splitByPrice(priceLists[name], thresholds)
		itemFilter.addSection(name, priceCategories, styles[name], optionLists[name])
	return itemFilter

def splitByPrice(priceList, thresholds):
	priceCategories = [[] for i in range(len(thresholds)+1)]
	for item in priceList:
		i = 0
		while i < len(thresholds) and priceList[item] < thresholds[i]:
			i += 1
		priceCategories[i].append(item)
	return priceCategories

def argumentList(items):
	argumentList = ""
	for item in items:
		argumentList += " \"" + item + "\""
	return argumentList

class BaseStyle:
	def __init__(self, omgColor, omgSize, omgIconSize, omgIconColor,
	                   veryHighSize, veryHighIconSize,
	                   highSize, highIconSize, highIconColor,
	                   normalSize,
	                   lowSize, lowColor, lowIconColor,
	                   hideSize,
	                   errorColor1, errorColor2, errorSize, errorIconShape):
		self.omgColor = omgColor
		self.omgSize = omgSize
		self.omgIconSize = omgIconSize
		self.omgIconColor = omgIconColor
		self.veryHighSize = veryHighSize
		self.veryHighIconSize = veryHighIconSize
		self.highSize = highSize
		self.highIconSize = highIconSize
		self.highIconColor = highIconColor
		self.normalSize = normalSize
		self.lowSize = lowSize
		self.lowColor = lowColor
		self.lowIconColor = lowIconColor
		self.hideSize = hideSize
		self.errorColor1 = errorColor1
		self.errorColor2 = errorColor2
		self.errorSize = errorSize
		self.errorIconShape = errorIconShape

class Style:
	def __init__(self, color, color2=None, iconColor=None, iconShape=None, useOmgColor=True):
		self.color = color
		self.color2 = color2
		self.iconColor = iconColor
		self.iconShape = iconShape
		self.useOmgColor = useOmgColor

class Options:
	def __init__(self, condition=BASE_TYPE, specialConditions=[], defaultConditions=[]):
		self.condition = condition
		self.specialConditions = specialConditions
		self.defaultConditions = defaultConditions

class ItemFilter:
	def __init__(self, baseStyle):
		self.indent = 0
		self.content = ""
		self.baseStyle = baseStyle

	def addLine(self, line):
		self.content += "\t"*self.indent
		self.content += line + "\n"

	def addBlock(self, name, conditions, displayOptions, blockType=SHOW):
		self.addLine(blockType + COMMENT + name)
		self.indent += 1
		for condition in conditions:
			self.addLine(condition)
		self.addLine(COMMENT)
		self.addLine(TEXT_COLOR + displayOptions[0])
		self.addLine(BACKGROUND_COLOR + displayOptions[1])
		self.addLine(BORDER_COLOR + displayOptions[2])
		self.addLine(FONT_SIZE + displayOptions[3])
		if not displayOptions[4]:
			self.addLine(NO_ICON)
		else:
			self.addLine(ICON + displayOptions[4])
		if not displayOptions[5]:
			self.addLine(NO_EFFECT)
		else:
			self.addLine(EFFECT + displayOptions[5])
		self.indent -= 1

	def addSection(self, name, priceCategories, style, options):
		self.addLine(COMMENT + name)
		self.indent += 1
		color2 = style.color2
		lowerColor = style.color
		higherColor = style.color2
		if not color2:
			color2 = self.baseStyle.lowColor
			lowerColor = self.baseStyle.lowColor
			higherColor = style.color
		omgColor = self.baseStyle.omgColor
		if not style.useOmgColor:
			omgColor = color2
		highIconColor = self.baseStyle.highIconColor
		lowIconColor = self.baseStyle.lowIconColor
		if style.iconColor:
			highIconColor = style.iconColor
			lowIconColor = style.iconColor
		if priceCategories[0]:
			self.addBlock("OMFG (>= 1000C)",
				            options.specialConditions + [options.condition + argumentList(priceCategories[0])],
			                [style.color, omgColor, style.color, self.baseStyle.omgSize, self.baseStyle.omgIconSize + self.baseStyle.omgIconColor + style.iconShape, self.baseStyle.omgIconColor])
		if priceCategories[1]:
			self.addBlock("OMG (>= 100C)",
				            options.specialConditions + [options.condition + argumentList(priceCategories[1])],
			                [omgColor, style.color, omgColor, self.baseStyle.omgSize, self.baseStyle.omgIconSize + self.baseStyle.omgIconColor + style.iconShape, self.baseStyle.omgIconColor])
		if priceCategories[2]:
			self.addBlock("Very High (>= 50C)",
			                options.specialConditions + [options.condition + argumentList(priceCategories[2])],
			                [lowerColor, higherColor, lowerColor, self.baseStyle.veryHighSize, self.baseStyle.veryHighIconSize + highIconColor + style.iconShape, highIconColor])
		if priceCategories[3]:
			self.addBlock("High (>= 10C)",
				            options.specialConditions + [options.condition + argumentList(priceCategories[3])],
			                [lowerColor, higherColor, lowerColor, self.baseStyle.highSize, self.baseStyle.highIconSize + highIconColor + style.iconShape, highIconColor])
		if priceCategories[4]:
			self.addBlock("normal (>= 1C)",
				            options.specialConditions + [options.condition + argumentList(priceCategories[4])],
			                [higherColor, lowerColor, higherColor, self.baseStyle.normalSize, None, lowIconColor + TEMP])
		if priceCategories[5]:
			self.addBlock("low (>= .1C)",
			               options.specialConditions + [options.condition + argumentList(priceCategories[5])],
			               [style.color, self.baseStyle.lowColor, color2, self.baseStyle.lowSize, None, None])
		if priceCategories[6]:
			self.addBlock("very low (>= .05C)",
			               options.specialConditions + [options.condition + argumentList(priceCategories[6])],
			               [style.color, self.baseStyle.lowColor, self.baseStyle.lowColor, self.baseStyle.lowSize, None, None])
		if priceCategories[7]:
			self.addBlock("rest",
			               options.specialConditions + [options.condition + argumentList(priceCategories[7])],
			               [style.color, self.baseStyle.lowColor, self.baseStyle.lowColor, self.baseStyle.hideSize, None, None])
		if options.defaultConditions:
			self.addBlock("Remaining ERROR",
			               options.defaultConditions,
			               [self.baseStyle.errorColor1, self.baseStyle.errorColor2, self.baseStyle.errorColor1, self.baseStyle.errorSize, self.baseStyle.omgIconSize + self.baseStyle.omgIconColor + self.baseStyle.errorIconShape, self.baseStyle.omgIconColor])
		self.indent -= 1
