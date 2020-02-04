#!/usr/bin/python3

import NinjaScraper as ninja
import FilterFactory as factory

NAME = "GeneratedLogic"
LEAGUE = "Metamorph" # "Hardcore Metamorph" "Standard" "Hardcore"
THRESHOLDS = [1000.0, 100.0, 50.0, 10.0, 1.0, 0.1, 0.05]

UNIQUE_COLOR    = " 175 096 037"
RARE_COLOR      = " 255 255 119"
MAGIC_COLOR     = " 136 136 255"
NORMAL_COLOR    = " 200 200 200"
NO_COLOR        = " 000 000 000"
NUTRAL_COLOR    = " 100 100 100"
CRAFTED_COLOR   = " 184 218 242"
CORRUPTED_COLOR = " 210 000 000"
QUEST_COLOR     = " 074 230 058"
MAP_COLOR       = " 200 155 155"
CARD_COLOR      = " 014 186 255"
CURRENCY_COLOR  = " 170 158 130"
GEM_COLOR       = " 027 162 155"
INFLUENCE_COLOR = " 127 000 255"
OMG_COLOR       = " 127 000 127"
VENDOR_COLOR    = " 000 127 000"
ERROR_COLOR_1   = " 255 000 000"
ERROR_COLOR_2   = " 255 255 255"

OMG_SIZE       = " 45"
ERROR_SIZE     = " 44"
VERY_HIGH_SIZE = " 36"
HIGH_SIZE      = " 33"
NORMAL_SIZE    = " 30"
LOW_SIZE       = " 27"
HIDE_SIZE      = " 18"

OMG_ICON_SIZE       = " 0"
VERY_HIGH_ICON_SIZE = " 1"
HIGH_ICON_SIZE      = " 2"

RED    = " Red"
YELLOW = " Yellow"
WHITE  = " White"
BROWN  = " Brown"
BLUE   = " Blue"
GREEN  = " Green"

HEXAGON  = " Hexagon"
TRIANGLE = " Triangle"
DIAMOND  = " Diamond"
STAR     = " Star"
SQUARE   = " Square"

CURRENCY      = " Currency"
INCUBATR      = " Incubator"
MAP_FRAGMANTS = " \"Map Fragments\""
CARDS         = " \"Divination Card\""

SHARDS = {"Alchemy":       "Orb of Alchemy",
          "Alteration":    "Orb of Alteration",
          "Transmutation": "Orb of Transmutation",
          "Ancient":       "Ancient Orb",
          "Annulment":     "Orb of Annulment",
          "Binding":       "Orb of Binding",
          "Chaos":         "Chaos Orb",
          "Engineer's":    "Engineer's Orb",
          "Exalted":       "Exalted Orb",
          "Harbinger's":   "Harbinger's Orb",
          "Horizon":       "Orb of Horizons",
          "Mirror":        "Mirror of Kalandra",
          "Regal":         "Regal Orb"}

TARGETED_C      = "Targeted Currency"
CARDS_INCUBATOR = "Divination Cards & Incubator"
UNIQUE_MAPS     = "Unique Maps (and Fragments)"
C               = "Currency"
UNIQUE_QUESTS   = "Unique Quests"
INFLUENCED_C    = "Influenced Currency"

def regroup(priceLists):
	# TODO reorder
	# TODO add missing currency
	newPriceLists = {TARGETED_C:      priceLists[ninja.OIL],
	                 CARDS_INCUBATOR: priceLists[ninja.INCUBATOR],
	                 UNIQUE_MAPS:     priceLists[ninja.SCARAB],
	                 C:               priceLists[ninja.RESONATOR],
	                 UNIQUE_QUESTS:   priceLists[ninja.PROPHECY],
	                 INFLUENCED_C:    {}}
	newPriceLists[TARGETED_C].update(priceLists[ninja.FOSSIL])
	newPriceLists[TARGETED_C].update(priceLists[ninja.ESSENCE])
	newPriceLists[CARDS_INCUBATOR].update(priceLists[ninja.CARD])
	newPriceLists[UNIQUE_MAPS].update(priceLists[ninja.FRAGMENT])

#	newPriceLists[UNIQUE_QUESTS]["Divine Vessel"] = newPriceLists[UNIQUE_MAPS].pop("Divine Vessel")

	for item in priceLists[ninja.CURRENCY]:
		if item.find("'s Exalted Orb") != -1 or item == "Awakener's Orb":
			newPriceLists[INFLUENCED_C][item] = priceLists[ninja.CURRENCY][item]
		elif item.find("Blessing") != -1 or item.find("Catalyst") != -1:
			newPriceLists[TARGETED_C][item] = priceLists[ninja.CURRENCY][item]
		elif item == "Stacked Deck":
			newPriceLists[CARDS_INCUBATOR][item] = priceLists[ninja.CURRENCY][item]
		elif item.find("Splinter") != -1:
			newPriceLists[UNIQUE_MAPS][item] = priceLists[ninja.CURRENCY][item]
		elif item.find("Shard") == -1 and item.find("Fragment") == -1:
			newPriceLists[C][item] = priceLists[ninja.CURRENCY][item]
	for shard in SHARDS:
		newPriceLists[C][shard + " Shard"] = priceLists[ninja.CURRENCY][SHARDS[shard]]/20.0
	newPriceLists[C]["Scroll Fragment"] = priceLists[ninja.CURRENCY]["Scroll of Wisdom"]/5.0
	return newPriceLists

baseStyle = factory.BaseStyle(OMG_COLOR, OMG_SIZE, OMG_ICON_SIZE, RED,
                              VERY_HIGH_SIZE, VERY_HIGH_ICON_SIZE,
                              HIGH_SIZE, HIGH_ICON_SIZE, YELLOW,
                              NORMAL_SIZE,
                              LOW_SIZE, NO_COLOR, WHITE,
                              HIDE_SIZE,
                              ERROR_COLOR_1, ERROR_COLOR_2, ERROR_SIZE, TRIANGLE)

priceLists = ninja.scrapeAllPriceLists(LEAGUE)
priceLists = regroup(priceLists)

styles = {TARGETED_C:      factory.Style(CURRENCY_COLOR, color2=UNIQUE_COLOR,    iconColor=BROWN, iconShape=DIAMOND),
          CARDS_INCUBATOR: factory.Style(CARD_COLOR,                                              iconShape=STAR),
          UNIQUE_MAPS:     factory.Style(MAP_COLOR,      color2=UNIQUE_COLOR,    iconColor=BROWN, iconShape=SQUARE),
          C:               factory.Style(CURRENCY_COLOR,                                          iconShape=DIAMOND),
          UNIQUE_QUESTS:   factory.Style(QUEST_COLOR,                            iconColor=GREEN, iconShape=TRIANGLE),
          INFLUENCED_C:    factory.Style(CURRENCY_COLOR, color2=INFLUENCE_COLOR, iconColor=BLUE,  iconShape=DIAMOND, useOmgColor=False)}

optionLists = {TARGETED_C:      factory.Options(specialConditions=[factory.CLASS + CURRENCY],         defaultConditions=[factory.CLASS + CURRENCY, factory.BASE_TYPE + " Oil Fossil Essence Blessing Catalyst"]),
               CARDS_INCUBATOR: factory.Options(specialConditions=[factory.CLASS + INCUBATR + CARDS], defaultConditions=[factory.CLASS + INCUBATR + CARDS]),
               UNIQUE_MAPS:     factory.Options(specialConditions=[factory.CLASS + MAP_FRAGMANTS],    defaultConditions=[factory.CLASS + MAP_FRAGMANTS]),
               C:               factory.Options(specialConditions=[factory.CLASS + CURRENCY],         defaultConditions=[factory.CLASS + CURRENCY]),
               UNIQUE_QUESTS:   factory.Options(specialConditions=[factory.CLASS + CURRENCY],         defaultConditions=[factory.CLASS + CURRENCY, factory.BASE_TYPE + " Prophecy"], condition=factory.PROPHECY),
               INFLUENCED_C:    factory.Options(specialConditions=[factory.CLASS + CURRENCY])}

factory.buildFilter(NAME, baseStyle, priceLists, THRESHOLDS, styles, optionLists)
