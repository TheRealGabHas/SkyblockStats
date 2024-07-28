ROMANS_NBR: dict[int, str] = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X"
}

# --- SKILLS ---

SKILLS: list = ["RUNECRAFTING", "COMBAT", "MINING", "TAMING", "ALCHEMY",
                "FARMING", "ENCHANTING", "FISHING", "FORAGING", "SOCIAL2", "CARPENTRY"]

SKILLS_XP_REQUIREMENTS: list = [
    50, 125, 200, 300, 500, 750, 1_000, 1_500, 2_000, 3_500,
    5_000, 7_500, 10_000, 15_000, 20_000, 30_000, 50_000, 75_000, 100_000,
    200_000, 300_000, 400_000, 500_000, 600_000, 700_000, 800_000, 900_000, 1_000_000,
    1_100_000, 1_200_000, 1_300_000, 1_400_000, 1_500_000, 1_600_000, 1_700_000, 1_800_000, 1_900_000,
    2_000_000, 2_100_000, 2_200_000, 2_300_000, 2_400_000, 2_500_000, 2_600_000, 2_750_000, 2_900_000,
    3_100_000, 3_400_000, 3_700_000, 4_000_000, 4_300_000, 4_600_000, 4_900_000, 5_200_000, 5_500_000,
    5_800_000, 6_100_000, 6_400_000, 6_700_000, 7_000_000
]

DUNGEON_XP_REQUIREMENTS: list = [
    50, 75, 110, 160, 230, 330, 470, 670, 950,
    1_340, 1_890, 2_665, 3_760, 5_260, 7_380, 10_300, 14_400, 20_000,
    27_600, 38_000, 52_500, 71_500, 97_000, 132_000, 180_000, 243_000, 328_000,
    445_000, 600_000, 800_000, 1_065_000,  1_410_000, 1_900_000, 2_500_000, 3_300_000, 4_300_000,
    5_600_000, 7_200_000, 9_200_000, 12_000_000, 15_000_000, 19_000_000, 24_000_000, 30_000_000, 38_000_000,
    48_000_000, 600_00_000, 75_000_000, 93_000_000, 116_250_000, 200_000_000,
]

RUNECRAFTING_XP_REQUIREMENTS: list = [
    50, 100, 125, 160, 200, 250, 315, 400, 500,
    625, 785, 1_000, 1_250, 1_600, 2_000, 2_465, 3_125,
    4_000, 5_000, 6_200, 7_800, 9_800, 12_200, 15_300, 19_050,
]

SOCIAL_XP_REQUIREMENTS: list = [
    50, 100, 150, 250, 500, 750, 1000, 1250, 1500,
    2_000, 2_500, 3_000, 3_750, 4_500, 6_000, 8_000, 10_000,
    12_500, 15_000, 20_000, 25_000, 30_000, 35_000, 40_000, 50_000,
]

# --- SLAYER ---

SLAYER_XP_REQUIREMENTS: dict = {
    "zombie": [5, 15, 200, 1000, 5000, 20_000, 100_000, 400_000, 1_000_000],
    "spider": [5, 25, 200, 1000, 5000, 20_000, 100_000, 400_000, 1_000_000],
    "wolf": [10, 30, 250, 1500, 5000, 20_000, 100_000, 400_000, 1_000_000],
    "enderman": [10, 30, 250, 1500, 5000, 20_000, 100_000, 400_000, 1_000_000],
    "blaze": [10, 30, 250, 1500, 5000, 20_000, 100_000, 400_000, 1_000_000],
    "vampire": [20, 75, 240, 840, 2400],
}

SLAYER_MAX_BOSS_TIER: dict = {
    "zombie": 5,
    "spider": 4,
    "wolf": 4,
    "enderman": 4,
    "blaze": 4,
    "vampire": 5
}

SLAYER_BOSS_ICONS: dict = {
    "zombie": "Rotten_Flesh",
    "spider": "Cobweb",
    "wolf": "Raw_Mutton",
    "enderman": "Ender_Pearl",
    "blaze": "Blaze_Powder",
    "vampire": "Redstone_Dust"
}

# --- RIFT ---

TIMECHARMS: list = ["Wyldly supreme Timecharm", "Mirrored Timecharm", "Chicken n egg Timecharm",
                    "Citizen Timecharm", "Lazy living Timecharm", "Slime Timecharm", "Vampiric Timecharm"]

# --- TROPHY FISHING ---

TROPHY_FISH: list = ['blobfish', 'flyfish', 'golden_fish', 'gusher', 'karate_fish', 'lava_horse', 'mana_ray', 'moldfin',
                     'obfuscated_fish_1', 'obfuscated_fish_2', 'obfuscated_fish_3', 'skeleton_fish', 'slugfish',
                     'soul_fish', "steaming_hot_flounder", 'sulphur_skitter', 'vanille', 'volcanic_stonefish']

TROPHY_RARITIES: list = ["bronze", "silver", "gold", "diamond"]
TROPHY_MISC: list = ["rewards", "last_caught", "total_caught"]
TROPHY_REWARDS: list = ["Bronze Hunter Reward", "Silver Hunter Reward", "Gold Hunter Reward", "Diamond Hunter Reward"]

TROPHY_FISH_ICONS: dict = {
    "Blobfish": "Blobfish_bronze",
    "Flyfish": "Flyfish_bronze",
    "Golden fish": "Golden_fish_bronze",
    "Gusher": "Gusher_bronze",
    "Karate fish": "Karate_fish_bronze",
    "Lava horse": "Lava_horse_bronze",
    "Mana ray": "Mana_ray_bronze",
    "Moldfin": "Moldfin_bronze",
    "Obfuscated fish": "Obfuscated_fish_1_bronze",
    "Obfuscated fish 2": "Obfuscated_fish_2_bronze",
    "Obfuscated fish 3": "Obfuscated_fish_3_bronze",
    "Skeleton fish": "Skeleton_fish_bronze",
    "Slugfish": "Slugfish_bronze",
    "Soul fish": "Soul_fish_bronze",
    "Steaming hot flounder": "Steaming_hot_flounder_bronze",
    "Sulphur skitter": "Sulphur_skitter_bronze",
    "Vanille": "Vanille_bronze",
    "Volcanic stonefish": "Volcanic_stonefish_bronze",
}

# --- COLORS ---

LEVELS_COLOR: dict = {
    0: 0xbebebe,
    40: 0xffffff,
    80: 0xfefe3f,
    120: 0x3ffe3f,
    160: 0x00be00,
    200: 0x3ffefe,
    240: 0x00bebe,
    280: 0x3f3ffe,
    320: 0xfe3ffe,
    360: 0xbe00be,
    400: 0xd9a334,
    440: 0xfe3f3f,
    480: 0xbe0000
}

RANKS_COLOR: dict = {
    "VIP": 0x3ffe3f,
    "VIP+": 0x3ffe3f,
    "MVP": 0x3ffefe,
    "MVP+": 0x3ffefe,
    "MVP++": 0xd9a334,
}

RABBITS_RANK_COLOR: dict = {
    "Intern": 0xffffff,
    "Employee": 0x3ffe3f,
    "Assistant": 0x3f3ffe,
    "Manager": 0xbe00be,
    "Director": 0xd9a334,
    "Executive": 0xfe3ffe,
    "Board Member": 0x3ffefe,
}

# --- CHOCOLATE FACTORY ---

RABBITS_LEVEL: dict = {
    0: "Intern",
    20: "Employee",
    75: "Assistant",
    120: "Assistant",
    140: "Manager",
    180: "Director",
    200: "Executive",
    220: "Board Member"
}
