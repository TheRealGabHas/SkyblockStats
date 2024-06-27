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

SKILLS: list = ["RUNECRAFTING", "COMBAT", "MINING", "TAMING", "ALCHEMY",
                "FARMING", "ENCHANTING", "FISHING", "FORAGING", "SOCIAL2", "CARPENTRY"]

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

TIMECHARMS: list = ["Wyldly supreme Timecharm", "Mirrored Timecharm", "Chicken n egg Timecharm",
                    "Citizen Timecharm", "Lazy living Timecharm", "Slime Timecharm", "Vampiric Timecharm"]

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
