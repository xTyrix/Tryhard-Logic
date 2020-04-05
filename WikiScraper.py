#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

website = "https://pathofexile.gamepedia.com/Currency"
result = requests.get(website)
assert result.status_code == 200, website + " status code: " + result.status_code

soup = BeautifulSoup(result.content, "html.parser")

for line in soup.find_all("table")[0]:
	print(line.prettify())
	print()
