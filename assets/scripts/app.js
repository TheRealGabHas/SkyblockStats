// Adding the icon to the slayer cards
const bossIconNames = ["Rotten_Flesh", "Cobweb", "Raw_Mutton", "Ender_Pearl", "Blaze_Powder", "Redstone_Dust"]

const slayerDiv = document.getElementById("slayer-cards")
const bossImgTag = slayerDiv.querySelectorAll("img")

for (let i = 0; i < bossImgTag.length; i++) {
    bossImgTag[i].src = `/images/${bossIconNames[i]}.webp`
}