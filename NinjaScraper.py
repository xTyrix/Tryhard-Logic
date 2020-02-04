#!/usr/bin/python3

import requests

STANDARD = "Standard"

OIL = "Oil"
INCUBATOR = "Incubator"
SCARAB = "Scarab"
FOSSIL = "Fossil"
RESONATOR = "Resonator"
ESSENCE = "Essence"
CARD = "DivinationCard"
PROPHECY = "Prophecy"
FRAGMENT = "Fragment"
CURRENCY = "Currency"

# TODO Watchstones (cannot match properly), Skill Gems?, Base Types?, Helmet Enchantments?, Unique Maps?, Maps?, Unique Jewels?, Unique Flasks?, Unique Weapons?, Unique Armours?, Unique Accessories?, Beasts?

ITEM_CATEGORIES = [OIL, INCUBATOR, SCARAB, FOSSIL, RESONATOR, ESSENCE, CARD, PROPHECY]
CURRENCY_CATEGORIES = [FRAGMENT, CURRENCY]

WATCHSTONE_CATEGORY = "Watchstone"
OTHER_CATEGORY = "Others"

IVORY_WATCHSTONE = "Ivory Watchstone"
 
def scrapeItemPriceList(category, league=STANDARD):
	result = requests.get("https://poe.ninja/api/data/itemoverview?league=" + league + "&type=" + category)
	assert result.status_code == 200, "https://poe.ninja/api/data/itemoverview?league=" + league + "&type=" + category + str(result.status_code)
	prices = {}
	for line in result.json()["lines"]:
		if category == PROPHECY and line["name"].find("A Master Seeks Help") != -1:
			if "A Master Seeks Help" in prices:
				prices["A Master Seeks Help"] = max(prices["A Master Seeks Help"], float(line["chaosValue"]))
			else:
				prices["A Master Seeks Help"] = float(line["chaosValue"])
			continue
		prices[line["name"]] = float(line["chaosValue"])
	return prices

def scrapeCurrencyPriceList(category, league=STANDARD):
	result = requests.get("https://poe.ninja/api/data/currencyoverview?league=" + league + "&type=" + category)
	assert result.status_code == 200, "https://poe.ninja/api/data/itemoverview?league=" + league + "&type=" + category + str(result.status_code)
	prices = {}
	if category == CURRENCY:
		prices["Chaos Orb"] = 1.0
	for line in result.json()["lines"]:
		prices[line["currencyTypeName"]] = float(line["chaosEquivalent"])
	return prices

def scrapeMaxItemPrice(category, league=STANDARD):
	result = requests.get("https://poe.ninja/api/data/itemoverview?league=" + league + "&type=" + category)
	assert result.status_code == 200, "https://poe.ninja/api/data/itemoverview?league=" + league + "&type=" + category + str(result.status_code)
	price = 0.0
	for line in result.json()["lines"]:
		price = max(price, line["chaosValue"])
	return price

def scrapeAllPriceLists(league=STANDARD):
	priceLists = {}
	for category in ITEM_CATEGORIES:
		priceLists[category] = scrapeItemPriceList(category, league)
	for category in CURRENCY_CATEGORIES:
		priceLists[category] = scrapeCurrencyPriceList(category, league)
	priceLists[OTHER_CATEGORY] = {}
	priceLists[OTHER_CATEGORY][IVORY_WATCHSTONE] = scrapeMaxItemPrice(WATCHSTONE_CATEGORY, league)
	return priceLists
