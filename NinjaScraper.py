#!/usr/bin/python3

import requests
from PoEInfos import FILTER as f

STANDARD = "Standard"

CURRENCY   	= "Currency"
FRAGMENT   	= "Fragment"
WATCHSTONE 	= "Watchstone"
OIL        	= "Oil"
INCUBATOR  	= "Incubator"
SCARAB     	= "Scarab"
FOSSIL     	= "Fossil"
RESONATOR  	= "Resonator"
ESSENCE    	= "Essence"
CARD       	= "DivinationCard"
PROPHECY   	= "Prophecy"
GEM        	= "SkillGem" # TODO
BASE       	= "BaseType" # TODO
ENCHANT    	= "HelmetEnchant" # TODO
U_MAP      	= "UniqueMap" # TODO
MAP        	= "Map" # TODO
U_JEWEL    	= "UniqueJewel" # TODO
U_FLASK    	= "UniqueFlask" # TODO
U_WEAPON   	= "UniqueWeapon" # TODO
U_ARMOUR   	= "UniqueArmour" # TODO
U_ACCESSORY = "UniqueAccessory" # TODO
BEAST       = "Beast" # TODO
VIAL        = "Vial" # TODO

CURRENCY_CATEGORIES = [FRAGMENT, CURRENCY]
ITEM_CATEGORIES = [WATCHSTONE, OIL, INCUBATOR, SCARAB, FOSSIL, RESONATOR, ESSENCE, CARD, PROPHECY, GEM, BASE, ENCHANT, U_MAP, MAP, U_JEWEL, U_FLASK, U_WEAPON, U_ARMOUR, U_ACCESSORY, BEAST, VIAL]

NINJA_CURRENCY_NAME  = "currencyTypeName"
NINJA_CURRENCY_PRICE = "chaosEquivalent"
NINJA_ITEM_NAME      = "name"
NINJA_ITEM_PRICE     = "chaosValue"
NINJA_BASE_TYPE      = "baseType"
NINJA_STACK_SIZE     = "stackSize"
NINJA_EXPLICITS      = "explicitModifiers"
NINJA_PROPHECY       = "prophecyText"
NINJA_VARIANT        = "variant"
NINJA_CORRUPTED      = "corrupted"
NINJA_GEM_LVL        = "gemLevel"
NINJA_QUALITY        = "gemQuality"
NINJA_LEVEL          = "levelRequired"
NINJA_TIER           = "mapTier"
NINJA_LINKS          = "links"

NAME       = "name"
PRICE      = "price"
BASE_TYPE  = f.CONDITION.BASE_TYPE
PROPHECY   = f.CONDITION.PROPHECY
STACK_SIZE = "maxStackSize"
EFFECT     = "effect"
REWARD     = "reward"
MAP_TIER   = f.CONDITION.MAP_TIER
LINKS      = f.CONDITION.LINKS
ITEM_LVL   = f.CONDITION.ITEM_LVL
INFLUENCE  = f.CONDITION.INFLUENCE
GEM_LVL    = f.CONDITION.GEM_LVL
QUALITY    = f.CONDITION.QUALITY
CORRUPTED  = f.CONDITION.CORRUPTED

FILTER_INFORMATION = [BASE_TYPE, PROPHECY, MAP_TIER, LINKS, ITEM_LVL, INFLUENCE, GEM_LVL, QUALITY, CORRUPTED]
ADDITIONAL_INFORMATION = [PRICE, STACK_SIZE, EFFECT, REWARD]

TRANSLATION_INFO = {VIAL:        (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_ITEM_NAME, STACK_SIZE: NINJA_STACK_SIZE}),
                    OIL:         (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_BASE_TYPE, STACK_SIZE: NINJA_STACK_SIZE}),
                    RESONATOR:   (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_ITEM_NAME, STACK_SIZE: NINJA_STACK_SIZE}),
                    FOSSIL:      (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_ITEM_NAME, STACK_SIZE: NINJA_STACK_SIZE, EFFECT: NINJA_EXPLICITS}),
                    # for ESSENCE NINJA_BASE_TYPE exists, but is less precise then NINJA_ITEM_NAME
                    ESSENCE:     (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_ITEM_NAME, STACK_SIZE: NINJA_STACK_SIZE, EFFECT: NINJA_EXPLICITS}),
                    CARD:        (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_ITEM_NAME, STACK_SIZE: NINJA_STACK_SIZE, REWARD: NINJA_EXPLICITS}),
                    SCARAB:      (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_ITEM_NAME,                               REWARD: NINJA_EXPLICITS}),
                    INCUBATOR:   (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_ITEM_NAME,                               REWARD: NINJA_EXPLICITS}),
                    PROPHECY:    (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     PROPHECY:  NINJA_ITEM_NAME,                               REWARD: NINJA_PROPHECY}),
                    CURRENCY:    (NINJA_CURRENCY_NAME, {PRICE: NINJA_CURRENCY_PRICE, BASE_TYPE: NINJA_CURRENCY_NAME}),
                    FRAGMENT:    (NINJA_CURRENCY_NAME, {PRICE: NINJA_CURRENCY_PRICE, BASE_TYPE: NINJA_CURRENCY_NAME}),
                    U_JEWEL:     (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_BASE_TYPE}),
                    U_FLASK:     (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_BASE_TYPE}),
                    U_ACCESSORY: (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_BASE_TYPE}),
                    U_MAP:       (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_BASE_TYPE, MAP_TIER: NINJA_TIER}),
                    MAP:         (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_BASE_TYPE, MAP_TIER: NINJA_TIER}),
                    # TODO for U_WEAPON and U_ARMOR ignore links
                    U_WEAPON:    (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_BASE_TYPE, LINKS: NINJA_LINKS}),
                    U_ARMOUR:    (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_BASE_TYPE, LINKS: NINJA_LINKS}),
                    BASE:        (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE,     BASE_TYPE: NINJA_BASE_TYPE, ITEM_LVL: NINJA_LEVEL, INFLUENCE: NINJA_VARIANT}),
                    WATCHSTONE:  (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE}),
                    BEAST:       (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE}),
                    # TODO ENCHANT needs info for filters; "tradeInfo" has alternate "range" representation
                    ENCHANT:     (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE, "range": NINJA_VARIANT}),
                    # GEM has an alternative representation for level, quality, and corrupted in NINJA_VARIANT
                    GEM:         (NINJA_ITEM_NAME,     {PRICE: NINJA_ITEM_PRICE, GEM_LVL: NINJA_GEM_LVL, QUALITY: NINJA_QUALITY, CORRUPTED: NINJA_CORRUPTED})}

# TODO
	# preprocess infos in here?

def translate(category, json):
	# TODO dont remove duplicate name lines!
	return {line[TRANSLATION_INFO[category][0]]: {key: line[TRANSLATION_INFO[category][1][key]] for key in TRANSLATION_INFO[category][1]} for line in json}

def scrapeList(category, league=STANDARD):
	if category in CURRENCY_CATEGORIES:
		listType = "currency"
	else:
		assert category in ITEM_CATEGORIES, "Category \"" + category + "\" does not exist!"
		listType = "item"
	website = "https://poe.ninja/api/data/" + listType + "overview?league=" + league + "&type=" + category
	result = requests.get(website)
	assert result.status_code == 200, website + " status code: " + result.status_code
	json = result.json()
	assert "lines" in json, "Expected \"lines\" in json: " + str(json)
	json = translate(category, json["lines"])
	if category == CURRENCY:
		json["Chaos Orb"] = {PRICE: 1, BASE_TYPE: "Chaos Orb"}
	return json

def scrapeAll(league=STANDARD):
	json = {}
	for category in CURRENCY_CATEGORIES + ITEM_CATEGORIES:
		json[category] = scrapeList(category, league)
	return json
