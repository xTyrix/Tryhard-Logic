#!/usr/bin/python3

from PoEInfos import FILTER as f

def buildArgumentString(argList):
	argString = ""
	for arg in argList:
		if " " in arg:
			argString += " \"" + arg + "\""
		else:
			argString += " " + arg
	return argString

def buildConditionString(condition, argList):
	return condition + " "*(len(f.ACTION.BACKGROUND_COLOR)-len(condition)+2) + buildArgumentString(argList)

def colorPartToString(part):
	s = str(part)
	return "0"*(3-len(s)) + s

def colorToString(color):
	return map(colorPartToString, color)

class ItemFilter:
	def __init__(self, name, version=None, information=[]):
		self.name = name
		self.indent = 0
		self.header  = f.COMMENT*(len(name)+6) + "\n"
		self.header += f.COMMENT + " "*(len(name)+4) + f.COMMENT + "\n"
		self.header += f.COMMENT + "  " + name + "  " + f.COMMENT
		if version:
			self.header += "  " + version
		self.header += "\n"
		self.header += f.COMMENT + " "*(len(name)+4) + f.COMMENT + "\n"
		self.header += f.COMMENT*(len(name)+6) + "\n\n"
		if information:
			for info in information:
				self.header += f.COMMENT + " " + info + "\n"
			self.header += "\n"
		self.content = ""
		self.contConditions = []

	def __str__(self):
		return self.header + self.content

	def beginContinuousCondition(self, condition):
		if condition in self.contConditions:
			print("Warning: \"" + condition + "\" is already in continuous condition and will not be added (again).")
			return
		self.contConditions.append(condition)

	def endContinuousCondition(self, condition):
		if condition not in self.contConditions:
			print("Warning: \"" + condition + "\" is not in continuous conditions and could not be removed.")
			return
		self.contConditions.remove(condition)

	def beginContinuousConditions(self, conditions):
		for condition in conditions:
			self.beginContinuousCondition(condition)

	def endContinuousConditions(self, conditions):
		for condition in conditions:
			self.endContinuousCondition(condition)

	def addLine(self, line="", comment=False):
		if not line:
			self.content += "\n"
			return
		self.content += "\t"*self.indent
		if comment:
			self.content += f.COMMENT + " "
		self.content += line + "\n"

	def addBlock(self, name, conditions, appearance, doShow=True, doContinue=False, comments=[]):
		if doShow:
			blockType = f.SHOW
		else:
			blockType = f.HIDE
		self.addLine(blockType + " " + f.COMMENT + " " + name)
		self.indent += 1
		for comment in comments:
			self.addLine(f.COMMENT + " " + comment)
		for condition in self.contConditions + conditions:
			self.addLine(condition)
		self.addLine(f.COMMENT)
		for line in appearance.toLines():
			self.addLine(line)
		if doContinue:
			addLine(f.CONTINUE)
		self.indent -= 1

	def write(self):
		f = open(self.name + ".filter", "w+")
		f.write(str(self))
		f.close()

class Display:
	def __init__(self, textColor, backgroundColor, borderColor, fontSize):
		self.textColor       = textColor
		self.backgroundColor = backgroundColor
		self.borderColor     = borderColor
		self.fontSize        = fontSize

	def toLines(self):
		lines = []
		lines.append(buildConditionString(f.ACTION.TEXT_COLOR,       colorToString(self.textColor)))
		lines.append(buildConditionString(f.ACTION.BACKGROUND_COLOR, colorToString(self.backgroundColor)))
		lines.append(buildConditionString(f.ACTION.BORDER_COLOR,     colorToString(self.borderColor)))
		lines.append(buildConditionString(f.ACTION.FONT_SIZE,        [str(self.fontSize)]))
		return lines

class Effect:
	def __init__(self, color, temp=False):
		self.color = color
		self.temp = temp

	def toLine(self):
		argList = [self.color]
		if self.temp:
			argList.append(f.TEMP_EFFECT)
		return buildConditionString(f.ACTION.EFFECT, argList)

class Icon:
	def __init__(self, size, color, shape):
		self.size  = str(size)
		self.color = color
		self.shape = shape

	def toLine(self):
		return buildConditionString(f.ACTION.ICON, [self.size, self.color, self.shape])

class Appearance:
	NO_ICON          = buildConditionString(f.COMMENT + " " + f.ACTION.ICON,   ["None"])
	NO_EFFECT        = buildConditionString(f.COMMENT + " " + f.ACTION.EFFECT, ["None"])

	def __init__(self, display, effect=None, icon=None):
		self.display = display
		self.effect = effect
		self.icon = icon

	def toLines(self):
		lines = self.display.toLines()

		if not self.effect:
			lines.append(Appearance.NO_EFFECT)
		else:
			lines.append(self.effect.toLine())

		if not self.icon:
			lines.append(Appearance.NO_ICON)
		else:
			lines.append(self.icon.toLine())

		return lines
