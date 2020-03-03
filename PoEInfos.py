#!/usr/bin/python3

class CLASS():
	CURRENCY = "Currency"
	## "Stackable Currency"
	## "Delve Socketable Currency"
	## "Delve Stackable Socketable Currency"

	ALL_MAP_ITEMS = "Map" #pseudo class
	## "Maps"
	## "Map Fragments"
	## "Labyrinth Map Item"
	## "Misc Map Items"

	CARD = "Divination Card"
	INCUBATOR = "Incubator"
	# "Life Flasks"
	# "Mana Flasks"
	# "Hybrid Flasks"
	# "Amulets"
	# "Rings"
	# "Claws"
	# "Daggers"
	# "Wands"
	# "One Hand Swords"
	# "Thrusting One Hand Swords"
	# "One Hand Axes"
	# "One Hand Maces"
	# "Bows"
	# "Staves"
	# "Two Hand Swords"
	# "Two Hand Axes"
	# "Two Hand Maces"
	# "Active Skill Gems"
	# "Support Skill Gems"
	# "Quivers"
	# "Belts"
	# "Gloves"
	# "Boots"
	# "Body Armours"
	# "Helmets"
	# "Shields"
	# "Quest Items"
	# "Sceptres"
	# "Utility Flasks"
	# "Fishing Rods"
	# "Hideout Doodads"
	# "Microtransactions"
	# "Jewel"
	# "Labyrinth Item"
	# "Labyrinth Trinket"
	# "Leaguestones"
	# "Pantheon Soul"
	# "Piece"
	# "Abyss Jewel"
	# "Incursion Item"
	# "Shard"
	# "Shard Heart"
	# "Rune Daggers"
	# "Warstaves"
	# "Atlas Region Upgrade Item"
	# "Metamorph Sample"

class FILTER():
	HIDE        = "Hide"
	SHOW        = "Show"
	COMMENT     = "#"
	TEMP_EFFECT = "Temp"
	EQ          = "="
	LT          = "<"
	GT          = ">"
	LE          = "<="
	GE          = ">="

	class CONDITION():
		#            "AreaLevel"       # [Operator] <Value>
		ITEM_LVL   = "ItemLevel"       # [Operator] <Level>
		#            "DropLevel"       # [Operator] <Level>
		QUALITY    = "Quality"         # [Operator] <Quality>
		RARITY     = "Rarity"          # [Operator] <Rarity>
		CLASS      = "Class"           #            <Class>
		BASE_TYPE  = "BaseType"        #            <Type>
		PROPHECY   = "Prophecy"        #            <Type>
		LINKS      = "LinkedSockets"   # [Operator] <Links>
		#            "SocketGroup"     # [Operator] <GroupSyntax>
		#            "Sockets"         # [Operator] <GroupSyntax>
		#            "Height"          # [Operator] <Value>
		#            "Width"           # [Operator] <Value>
		#            "HasExplicitMod"  #            <Value>
		#            "AnyEnchantment"  #            <Boolean>
		#            "HasEnchantment"  #            <Value>
		STACK_SIZE = "StackSize"       # [Operator] <Value>
		GEM_LVL    = "GemLevel"        # [Operator] <Value>
		#            "Identified"      #            <Boolean>
		CORRUPTED  = "Corrupted"       #            <Boolean>
		#            "CorruptedMods"   # [Operator] <Value>
		#            "Mirrored"        #            <Boolean>
		#            "ElderItem"       #            <Boolean>
		#            "ShaperItem"      #            <Boolean>
		INFLUENCE  = "HasInfluence"    #            <Type>
		#            "FracturedItem"   #            <Boolean>
		#            "SynthesisedItem" #            <Boolean>
		#            "ShapedMap"       #            <Boolean>
		MAP_TIER   = "MapTier"         # [Operator] <Value>

	class ACTION():
		TEXT_COLOR       = "SetTextColor"             # <Red> <Green> <Blue> [Alpha]
		BACKGROUND_COLOR = "SetBackgroundColor"       # <Red> <Green> <Blue> [Alpha]
		BORDER_COLOR     = "SetBorderColor"           # <Red> <Green> <Blue> [Alpha]
		FONT_SIZE        = "SetFontSize"              # <FontSize>
		EFFECT           = "PlayEffect"               #        <Color>         [Temp]
		ICON             = "MinimapIcon"              # <Size> <Color> <Shape>
		#                  "PlayAlertSound"           # <Id> [Volume]
		#                  "PlayAlertSoundPositional" # <Id> [Volume]
		#                  "DisableDropSound"
		#                  "CustomAlertSound"         # <FileName | FileFullPath>
		CONTINUE         = "Continue"

class EFFECT():
	class COLOR():
		RED    = "Red"
		YELLOW = "Yellow"
		WHITE  = "White"
		BROWN  = "Brown"
		BLUE   = "Blue"
		GREEN  = "Green"

class ICON:
	class SIZE():
		SMALL  = 2
		MEDIUM = 1
		LARGE  = 0

	class COLOR():
		RED    = "Red"
		YELLOW = "Yellow"
		WHITE  = "White"
		BROWN  = "Brown"
		BLUE   = "Blue"
		GREEN  = "Green"

	class SHAPE():
		HEXAGON  = "Hexagon"
		TRIANGLE = "Triangle"
		DIAMOND  = "Diamond"
		STAR     = "Star"
		SQUARE   = "Square"
		CIRCLE   = "Circle"
