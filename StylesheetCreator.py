#!/usr/bin/python3

from PIL import Image, ImageDraw
from FilterFactory import Style, BaseStyle
import re

def getActualColor(weirdString):
	splitString = re.findall("[0-9]*", weirdString)
	return (int(splitString[1]), int(splitString[3]), int(splitString[5]))

class StyleSheet:
	def __init__(self, styles, baseStyle):
		self.X = 2
		self.Y = 2
		self.styles = styles
		self.baseStyle = baseStyle
		self.image = Image.new("RGB", (80, 15*len(styles)), (68, 68, 68))
		self.created = False

	def addItem(self, textColor, backgroundColor, borderColor, symbol):
		draw = ImageDraw.Draw(self.image)
		self.image.paste(borderColor, (self.X, self.Y, self.X+11, self.Y+11))
		self.image.paste(backgroundColor, (self.X+1, self.Y+1, self.X+10, self.Y+10))
		if symbol == "F":
			draw.line((self.X+4, self.Y+3, self.X+4, self.Y+7), fill=textColor)
			draw.line((self.X+4, self.Y+3, self.X+6, self.Y+3), fill=textColor)
			draw.line((self.X+4, self.Y+5, self.X+6, self.Y+5), fill=textColor)
		elif symbol == "I":
			draw.line((self.X+5, self.Y+3, self.X+5, self.Y+7), fill=textColor)
			draw.line((self.X+4, self.Y+3, self.X+6, self.Y+3), fill=textColor)
			draw.line((self.X+4, self.Y+7, self.X+6, self.Y+7), fill=textColor)
		elif symbol == "L":
			draw.line((self.X+4, self.Y+3, self.X+4, self.Y+7), fill=textColor)
			draw.line((self.X+4, self.Y+7, self.X+6, self.Y+7), fill=textColor)
		elif symbol == "T":
			draw.line((self.X+5, self.Y+3, self.X+5, self.Y+7), fill=textColor)
			draw.line((self.X+4, self.Y+3, self.X+6, self.Y+3), fill=textColor)
		elif symbol == "E":
			draw.line((self.X+4, self.Y+3, self.X+4, self.Y+7), fill=textColor)
			draw.line((self.X+4, self.Y+3, self.X+6, self.Y+3), fill=textColor)
			draw.line((self.X+4, self.Y+5, self.X+6, self.Y+5), fill=textColor)
			draw.line((self.X+4, self.Y+7, self.X+6, self.Y+7), fill=textColor)
		else:
			assert symbol == "R", "Unknown symbol: " + symbol
			draw.line((self.X+4, self.Y+3, self.X+4, self.Y+7), fill=textColor)
			draw.line((self.X+5, self.Y+3, self.X+5, self.Y+3), fill=textColor)
			draw.line((self.X+6, self.Y+4, self.X+6, self.Y+4), fill=textColor)
			draw.line((self.X+5, self.Y+5, self.X+5, self.Y+5), fill=textColor)
			draw.line((self.X+6, self.Y+6, self.X+6, self.Y+7), fill=textColor)
		del draw
		self.X += 13

	def addLine(self, style):
		color = getActualColor(style.color)
		lowColor = getActualColor(self.baseStyle.lowColor)
		if style.color2:
			color2 = getActualColor(style.color2)
			lowerColor = color
			higherColor = color2
		else:
			color2 = lowColor
			lowerColor = color2
			higherColor = color
		if style.useOmgColor:
			omgColor = getActualColor(self.baseStyle.omgColor)
		else:
			omgColor = color2

		self.addItem(color, omgColor, color, "F")
		self.addItem(omgColor, color, omgColor, "I")
		self.addItem(lowerColor, higherColor, lowerColor, "L")
		self.addItem(higherColor, lowerColor, higherColor, "T")
		self.addItem(color, lowColor, color2, "E")
		self.addItem(color, lowColor, lowColor, "R")

		self.X = 2
		self.Y += 15

	def save(self, name="Stylesheet"):
		if not self.created:
			for style in self.styles:
				self.addLine(self.styles[style])
			self.created = True
		self.image.save("./" + name + ".png", "PNG")
