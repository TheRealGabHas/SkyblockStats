# The intent of this program is to retrieve a list of every chocolate rabbit associated with their rarity and icon.
# It is only possible thanks to the work of the editor of the Hypixel Skyblock Fandom Wiki.


from bs4 import BeautifulSoup
import json

# This file contains the <tbody> with all the rabbits from the Fandom page:
# https://hypixel-skyblock.fandom.com/wiki/Chocolate_Rabbits/List
with open("../../../.tests/rabbits.html", "r") as file:
    content = file.read()

soup = BeautifulSoup(content, "html.parser")

rabbit_list = []

# Each rabbit is in a <tr> tag
for entry in soup.find_all("tr"):
    fields = entry.find_all("td")

    img_tag = fields[0].find("img")
    if img_tag is not None:
        link_fd = img_tag.get("src")
    else:
        link_fd = "https://placehold.co/300x300"

    name_fd = fields[1]
    rarity_fd = fields[2].find_all("span")[-1]

    rabbit_list.append({
        "name": name_fd.get_text().strip(),
        "rarity": rarity_fd.get_text(),
        "img": link_fd,
    })

with open("rabbits.json", "w") as file:
    json.dump(rabbit_list, file)