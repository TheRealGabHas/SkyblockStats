import sys
import datetime
import json
import uuid as lib_uuid

import requests

import stats_gather.consts
import stats_gather.s_utils as utils
import stats_gather.consts as consts
from stats_gather.consts import (SKILLS, SLAYER_XP_REQUIREMENTS, SLAYER_MAX_BOSS_TIER, SLAYER_BOSS_ICONS, TIMECHARMS,
                                     RANKS_COLOR, LEVELS_COLOR, EMPLOYEE_PROD_PER_LVL, FACTORY_PRESTIGE_BUFF,
                                     EMPLOYEE_COLLECTION_PROD, EMPLOYEE_COLLECTION_MUL)


# Retrieve the API key from the configuration file
with open("config/settings.json", "r") as config_file:
    config = json.load(config_file)

    API_KEY: str = config['hypixel-api-key']
    # Simple check to ensure the field is filled with a correctly sized API key string
    if len(API_KEY) != 36:
        sys.exit("Invalid Hypixel API key in the config/settings.json file.")

    header = {
        "API-Key": API_KEY
    }


class Profile:

    def __init__(self, uuid: str):
        self.data = None
        self.uuid: str = uuid
        self.rank_data = None
        self.rank: str = "None"
        self.rank_color: str = "0xfff"
        self.skyblock_profiles: list = []

    def gather_rank(self):
        if self.rank_data is None:
            self.rank_data = requests.get(f"https://api.hypixel.net/v2/player?uuid={self.uuid}", headers=header).json()

        rank_data = self.rank_data

        if rank_data is not None:
            if rank_data.get('player') is not None:
                self.rank = rank_data['player'].get('newPackageRank', "None")
                self.rank = self.rank.replace("PLUS", "+").replace("_", "")

                self.rank_color = hex(RANKS_COLOR.get(self.rank, 0xfff)).replace("0x", "#")

                # Get a first taste of what profile the player owns (id, name)
                if rank_data['player']['stats'].get('SkyBlock', None) is not None:
                    _profiles = rank_data['player']['stats']['SkyBlock']['profiles']
                    for profile_id, profile_data in _profiles.items():
                        self.skyblock_profiles.append((str(lib_uuid.UUID(profile_id)), profile_data['cute_name']))

    def gather_stats(self) -> tuple[bool, int]:
        """
        Performs an API request to Hypixel to retrieve a profile's data
        :return: A tuple containing a boolean (success/ failure) and an HTTP response code
        """
        api_request = requests.get(f"https://api.hypixel.net/v2/skyblock/profiles?uuid={self.uuid}", headers=header)

        _data = api_request.json()
        if _data.get("success") is not None:
            self.data = _data

        return _data.get("success", False), api_request.status_code

    def get_stats(self) -> dict:
        return self.data

    def get_selected_profile(self) -> dict | None:
        """
        Fetch the selected profile and returns the associated datas (JSON dict)
        :return: JSON dictionary containing the profile data
        """
        if self.data is None:
            return {}
        if self.data.get("profiles") is None:
            return {}

        for profile in self.data['profiles']:
            if profile['selected']:
                return profile['members'][self.uuid.replace("-", "")]
                # Returns queried user profile in the coop. Replacing the uuid dashes

    def get_profile_list(self) -> list[dict]:
        """
        Fetch every profile of the player and retrieves essential information (uuid, name, game mode, selection state)
        :return: A list of dictionaries with the following keys : {uuid, name, selected, game_mode}
        """
        profile_list = []

        if self.data is None:
            return profile_list
        if self.data.get("profiles") is None:
            return profile_list

        for profile in self.data['profiles']:
            profile_list.append({
                "uuid": profile['profile_id'],
                "name": profile['cute_name'],
                "selected": profile['selected'],
                "game_mode": profile.get("game_mode", "normal")  # This field is only defined if custom game mode
            })

        return profile_list

    def get_profile_data(self, searched_field: str, profile: str = "selected") -> dict | int | float:
        """
        Fetch the data for a specific part of a user profile. The default profile is the selected one.
        :param searched_field: What to search (ex: "slayer_bosses")
        :param profile: Name of the profile to look in
        :return: The queried field for the specified profile.
        """

        if profile == "selected":
            return self.get_selected_profile().get(searched_field, {})
        for _profile in self.get_stats()['profiles']:
            if _profile['cute_name'].lower() == profile.lower():
                if _profile['members'][self.uuid.replace("-", "")]:
                    return _profile['members'][self.uuid.replace("-", "")].get(searched_field, {})

    def get_leveling_data(self, profile: str = "selected") -> dict:
        xp_data: dict = {}

        global_level = self.get_profile_data("leveling", profile=profile).get("experience", 0)
        level_color = 0xbebebe

        for level, color in LEVELS_COLOR.items():
            if global_level*0.01 > level:
                level_color = color
            else:
                break

        xp_data['Global'] = {
            "xp": global_level,
            "icon_path": "/images/Skyblock_Levels.webp",
            "color": f"#{level_color:06x}",
        }

        skill_field = self.get_profile_data("player_data", profile=profile).get("experience", {})
        skill_average: float = 0.0

        for skill in SKILLS:
            key = skill.lower().capitalize()
            value = skill_field.get(f'SKILL_{skill}', 1)

            if key == "Social":
                skill_table = consts.SOCIAL_XP_REQUIREMENTS
            elif key == "Runecrafting":
                skill_table = consts.RUNECRAFTING_XP_REQUIREMENTS
            elif key in ["Foraging", "Alchemy"]:  # Capped at 50 level (and not 60)
                skill_table = consts.SKILLS_XP_REQUIREMENTS[:-10]
            else:
                skill_table = consts.SKILLS_XP_REQUIREMENTS

            xp_data[key] = {
                "xp": f"{round(value):,}",
                "icon_path": f"/images/{key}.webp",
                "level_xp": 0,
                "next_level_xp": 100,
            }

            if key != "Global":
                xp_data[key]['level'] = utils.get_level_from_xp(f"{round(value):,}", skill_table=skill_table)
                progression = utils.get_level_info_from_xp(f"{round(value):,}", skill_table=skill_table)
                xp_data[key]['level_xp'] = progression['current_xp']
                xp_data[key]['next_level_xp'] = progression['required_xp']

            # Take the level cap into account
            if key == "Taming":
                given_pets: list = self.get_profile_data("pets_data", profile=profile).get("pet_care", {}).get("pet_types_sacrificed", [])
                cap = 60 - (10 - len(given_pets))

                if xp_data[key]['level'] > cap:
                    xp_data[key]['level'] = cap

            if key not in ["Social", "Runecrafting"]:  # Not counted in the skill average
                skill_average += float(xp_data[key]['level'])

        skill_average /= 9  # There are 9 skills counted in the skill average
        xp_data['Global']['skill_average'] = f"{skill_average:.1f}"

        return xp_data

    def get_slayer_data(self, profile: str = "selected") -> dict:
        sl_data = self.get_profile_data("slayer", profile=profile).get("slayer_bosses", {})

        def find_next_xp_req(_boss: str, xp: int):
            """
            Returns the next amount of Slayer XP to get to the next slayer level
            :param _boss: Name of the boss
            :param xp: Current amount of XP
            :return:
            """

            for BOSS in SLAYER_XP_REQUIREMENTS:
                if not BOSS == _boss:
                    continue

                all_reqs = SLAYER_XP_REQUIREMENTS[BOSS]
                if xp > all_reqs[-1]:  # Max level reached
                    return "MAX LEVEL"
                for level in all_reqs:
                    if xp < level:
                        return f"{level:,}"

        # Formatting the data
        final_dict: dict = {}

        for boss in sl_data:
            c = sl_data[boss].get("xp", 0)
            current_xp = f"{c:,}"
            next_level_xp = find_next_xp_req(boss, xp=int(c))

            boss_kills = []
            for i in range(5):
                if (v := sl_data[boss].get(f"boss_kills_tier_{i}")) is not None:
                    boss_kills.append({f"Tier {i + 1}": f"{v:,}"})
                elif SLAYER_MAX_BOSS_TIER[boss] >= i + 1:  # A boss of Tier 5 exists
                    boss_kills.append({f"Tier {i + 1}": 0})

            final_dict[boss.capitalize()] = {
                "current_level": len(sl_data[boss].get("claimed_levels", {}).keys()),  # Current level
                "xp": current_xp,
                "next_lvl_xp": next_level_xp,
                "boss_kills": boss_kills,
            }

        # Making sure every card has at least the icon  (even if the boss was never fought/ beaten)
        for boss, file_name in SLAYER_BOSS_ICONS.items():
            if final_dict.get(boss.capitalize()) is None:
                final_dict[boss.capitalize()] = {
                    "icon_path": f"/images/{file_name}.webp"
                }
            else:
                final_dict[boss.capitalize()]['icon_path'] = f"/images/{file_name}.webp"

        # Make sure the dictionary is correctly ordered
        final_dict = utils.order_dict(final_dict, key_order=[boss.capitalize() for boss in SLAYER_MAX_BOSS_TIER.keys()])

        return final_dict

    def get_rift_data(self, profile: str = "selected") -> dict:
        rift_data: dict = {}

        global_rift = self.get_profile_data("rift", profile=profile)

        trophies = global_rift.get("gallery", {}).get("secured_trophies")
        souls = global_rift.get("enigma", {}).get("found_souls", [])
        lonely = global_rift.get("village_plaza", {}).get("lonely", {}).get("seconds_sitting")
        montezuma = global_rift.get("dead_cats", {}).get("found_cats", [])
        burger = global_rift.get("castle", {}).get("grubber_stacks", 0)

        current_motes = int(self.get_profile_data("currencies", profile=profile).get("motes_purse", 0))

        stats = self.get_profile_data("player_stats", profile=profile).get("rift", {})
        lifetime_motes = int(stats.get("lifetime_motes_earned", 0))
        orb_picked = int(stats.get("motes_orb_pickup", 0))

        missing_trophies = []
        found_trophies = []

        if trophies is None:
            rift_data['trophies'] = []
        else:
            # (Timecharm name, unlocked at visit)
            for trophy in trophies:
                trophy['icon_path'] = f"/images/rift/{trophy['type']}.png"
                trophy['type'] = trophy['type'].replace("_", " ")
                del trophy['timestamp']
                found_trophies.append(trophy)

        rift_data['trophies'] = found_trophies
        obtained_trophies: tuple = tuple(tr['type'] for tr in rift_data['trophies'])
        for trophy in TIMECHARMS:
            if trophy.lower() not in obtained_trophies:
                missing_trophies.append({
                    "type": trophy,
                    "icon_path": f"/images/rift/{" ".join(word.lower() for word in trophy.replace("_", " ").split())}.png".replace(" ", "_")
                })

        rift_data['missing_trophies'] = missing_trophies

        # Number of found Enigma souls
        rift_data['souls'] = {
            "value": len(souls),
            "icon_path": "/images/Enigma_Soul.webp"
        }

        rift_data['time_sitting'] = {
            "value": 0,
            "icon_path": "/images/Oak_Stairs.webp"
        }

        # Amount of time spent sitting alone (minutes, seconds)
        if lonely is None:
            rift_data['time_sitting']['value'] = (0, 0)
        else:
            rift_data['time_sitting']['value'] = int(lonely / 60), lonely % 60

        # Amount of Montezuma soul fragments found
        rift_data['montezuma'] = {
            "value": len(montezuma),
            "icon_path": "/images/Montezuma.webp"
        }

        rift_data['burger'] = {
            "value": burger,
            "icon_path": "/images/McGrubber_Burger.webp"
        }

        rift_data['motes'] = {
            "value": f"{current_motes:,}",
            "icon_path": "/images/Motes.webp"
        }

        rift_data['lifetime_motes'] = {
            "value": f"{lifetime_motes:,}",
            "icon_path": "/images/Motes.webp"
        }

        rift_data['orbs'] = {
            "value": f"{orb_picked:,}",
            "icon_path": "/images/Experience_Bottle.webp"
        }

        return rift_data

    def get_misc_stats(self, profile: str = "selected") -> dict:
        profile_data = self.get_profile_data("profile", profile=profile)

        join_date = profile_data.get("first_join")
        soulflow = self.get_profile_data("item_data", profile=profile).get("soulflow", 0)
        fishing_treasures = self.get_profile_data("player_stats", profile=profile).get("items_fished", {}).get("treasure", 0)
        fairy_souls = self.get_profile_data("fairy_soul", profile=profile).get("total_collected", 0)
        coin_purse = self.get_profile_data("currencies", profile=profile).get("coin_purse", 0)
        bank_level = profile_data.get("personal_bank_upgrade", 0)
        personal_bank = profile_data.get("bank_account", 0.0)

        if join_date is None:
            first_join = "Not found"
        else:
            first_join = datetime.datetime.fromtimestamp(int(join_date / 1000)).strftime("%Y-%m-%d %H:%M:%S")


        final_dict: dict = {
            "First Join": {
                "value": first_join,
                "icon_path": "/images/Painting.webp"
            },
            "Soulflow": {
                "value": f"{soulflow:,.0f}",
                "icon_path": "/images/Soulflow.webp"
            },
            "Fished Treasures": {
                "value": f"{fishing_treasures:,.0f}",
                "icon_path": "/images/Treasurite.webp"
            },
            "Fairy Souls": {
                "value": fairy_souls,
                "icon_path": "/images/Fairy_Soul.webp"
            },
            "Purse": {
                "value": f"{coin_purse:,.2f}",
                "icon_path": "/images/Personal_Bank.webp"
            },
            "Bank Account": {
                "value": f"{personal_bank:,.2f}",
                "icon_path": "/images/Personal_Bank.webp"
            },
            "Personal Bank Upgrade": {
                "value": bank_level,
                "icon_path": "/images/Personal_Bank.webp"
            }
        }

        return final_dict

    def get_trophy_stats(self, profile: str = "selected") -> tuple[list, dict]:
        trophy_stats = self.get_profile_data("trophy_fish", profile=profile)

        fishes = list(trophy_stats.keys())

        # Removing misc data from the trophy fish list
        for misc_item in stats_gather.consts.TROPHY_MISC:
            fishes.remove(misc_item) if misc_item in fishes else ()
        fishes.sort()
        fishes = {_key: trophy_stats.get(_key, 0) for _key in fishes}

        # Check if the reward level is at least 1
        if len(trophy_stats.get("rewards", [])) == 0:
            reward_tier = "No claimed reward"
        elif (s := trophy_stats.get("rewards", [0])[-1]) > 0:
            reward_tier = consts.TROPHY_REWARDS[s - 1]
        else:
            reward_tier = "No claimed reward"

        reward_icons: dict = {
            "No claimed reward": "/images/Barrier.webp",
            "Bronze Hunter Reward": "/images/Leather_Tunic.webp",
            "Silver Hunter Reward": "/images/Iron_Chestplate.webp",
            "Gold Hunter Reward": "/images/Golden_Chestplate.webp",
            "Diamond Hunter Reward": "/images/Diamond_Chestplate.webp",
        }

        total_caught = f"{trophy_stats.get('total_caught', 0):,.0f}"
        misc_trophy_stats = {
            "Claimed reward": {
                "name": reward_tier,
                "icon_path": reward_icons.get(reward_tier, "/images/Barrier.webp")
            },
            "Trophy fished": {
                "amount": total_caught,
                "icon_path": "/images/Pufferfish.webp"
            },
        }
        fish_record = []

        for fish in consts.TROPHY_FISH:
            label = fish.replace("_", " ").capitalize()
            current_fish = {label: {}}

            for rarity in consts.TROPHY_RARITIES:
                amount_fished = fishes.get(f"{fish}_{rarity}", "X")

                if amount_fished != "X":
                    amount_fished = f"{amount_fished:,.0f}"

                current_fish[label][rarity.capitalize()] = amount_fished

            current_fish["icon_path"] = f"/images/trophy_fish/{label}_bronze.webp"
            fish_record.append(current_fish)

        return fish_record, misc_trophy_stats

    def get_chocolate_factory_stats(self, profile: str = "selected"):
        cf = self.get_profile_data("events", profile=profile)

        # Fetch the chocolate factory statistics
        cf = cf.get("easter", {})

        # Fetch the level of every rabbit employee (0 = not unlocked)
        default_state: dict = {
            "level": 0,
            "rank": "Not unlocked",
            "color": "#9e9e9e",
            "icon_path": "/images/Barrier.webp",
        }

        employees = {
            "rabbit_bro": 0,
            "rabbit_cousin": 0,
            "rabbit_sis": 0,
            "rabbit_father": 0,
            "rabbit_grandma": 0,
            "rabbit_uncle": 0,
            "rabbit_dog": 0,
        }

        for employee, level in cf.get("employees", {}).items():
            employee_data = utils.get_rabbit_employee_data(level)
            employees[employee] = {
                "level": level,
                "rank": employee_data[0],
                "color": employee_data[1],
                "icon_path": f"/images/chocolate/{employee}.webp",
            }

        # Put the default state if there is no data (level 0)
        for rabbit, data in employees.copy().items():
            if data == 0:
                employees[rabbit] = default_state.copy()

        # Fetch the rabbit collection (Rabbit name, number of found time)
        collection: dict = {}

        for rabbit_name, quantity in cf.get("rabbits", {}).items():
            beautified_name = " ".join(word.capitalize() for word in str(rabbit_name).split("_"))
            collection[beautified_name] = quantity


        # Removing useless keys
        if collection.get("Collected Eggs") is not None:
            del collection['Collected Eggs']
        if collection.get("Collected Locations") is not None:
            del collection['Collected Locations']

        # This name isn't correctly beautified by the above piece of code
        if collection.get("Hop A Long"):
            collection['Hop-a-long'] = collection["Hop A Long"]
            del collection["Hop A Long"]

        # The dicts that will be passed in the template
        rabbit_collection: dict = {
            "COMMON": [],
            "UNCOMMON": [],
            "RARE": [],
            "EPIC": [],
            "LEGENDARY": [],
            "MYTHIC": [],
            "DIVINE": [],
        }
        collection_data: dict = {}
        with open("stats_gather/miscellaneous/rabbits.json", "r") as rabbit_file:
            rabbits_list = json.load(rabbit_file)

            for i, rabbit_data in enumerate(rabbits_list.copy()):
                rabbits_list[i]['amount'] = collection.get(rabbit_data['name'], 0)
                rabbits_list[i]['img'] = consts.RABBIT_ICONS[rabbit_data['rarity']]
                rabbit_collection[rabbit_data['rarity']].append(rabbits_list[i])


        # Filling the data dictionary
        for rarity, rabbit_list in rabbit_collection.items():

            collection_data[rarity] = {
                "total_unique": len(rabbit_list),
                "found_unique": sum(1 for rb in rabbit_list if rb.get('amount', 0) > 0),  # Adds 1 if the rabbit has been found at least 1 time
                "total_found": f"{sum(rb.get('amount', 0) for rb in rabbit_list):,.0f}",
            }

        # Fetch the chocolate factory upgrades level
        upgrades: dict = {
            "barn": cf.get("rabbit_barn_capacity_level", 0),
            "click": cf.get("click_upgrades", 0),
            "tower": cf.get("time_tower", {}).get("level", 0),
            "shrine": cf.get("rabbit_rarity_upgrades", 0),
            "jackrabbit": cf.get("chocolate_multiplier_upgrades", 0),
            "hitmen": cf.get("rabbit_hitmen", {}).get("rabbit_hitmen_slots", 0)
        }
        upgrades["barn_slots"] = utils.get_barn_capacity(upgrades['barn'])

        # Fetch chocolate statistics
        chocolate: dict = {
            "factory_level": cf.get("chocolate_level", 0),
            "current_chocolate": f"{cf.get("chocolate", 0):,.0f}",
            "alltime_chocolate": f"{cf.get("total_chocolate", 0):,.0f}",
            "prestige_chocolate": f"{cf.get("chocolate_since_prestige", 0):,.0f}",
        }

        # Misc
        misc: dict = {
            "chocolate_bar_counter": cf.get("supreme_chocolate_bars", 0),
            "shop_spent": cf.get("shop", {}).get("chocolate_spent", 0),
            "unique_rabbit": f"{len(collection.keys()):,.0f}",
            "total_rabbit": f"{sum(collection.values()):,.0f}",
            "missing_hitmen_egg": f"{cf.get("rabbit_hitmen", {}).get("missed_uncollected_eggs", 0):,.0f}",
            "truffle": f"{cf.get("refined_dark_cacao_truffles", 0):.0f}"
        }
        misc['shop_milestone'] = utils.get_shop_milestone(misc['shop_spent'])
        misc['chocolate_bar_counter'] = f"{misc['chocolate_bar_counter']:,.0f}"
        misc['shop_spent'] = f"{misc['shop_spent']:,.0f}"


        # Estimating the factory production
        production: dict = {
            "per_sec": 0,
            "per_sec_with_tower": 0,
            "production": [],
            "multiplier": []
        }

        cookie_buff = self.get_profile_data("profile", profile=profile).get("cookie_buff_active", False)
        cookie_buff = 0.25 if cookie_buff else 0

        talisman_prod: int = 0
        talisman_bag = self.get_profile_data("inventory", profile=profile)

        if talisman_bag is not None and isinstance(talisman_bag, dict):
            talisman_bag = talisman_bag.get("bag_contents", {}).get("talisman_bag", {}).get("data", {})
            if talisman_bag != {}:
                talisman_bag = utils.process_inv(talisman_bag)

                for talisman, buff in consts.CHOCOLATE_TALISMAN_BUFF.items():
                    if talisman in talisman_bag:
                        talisman_prod = buff

        employee_prod: int = 0
        for employee, employee_data in employees.items():
            employee_prod += EMPLOYEE_PROD_PER_LVL[employee] * employee_data['level']

        prestige_multiplier: float = FACTORY_PRESTIGE_BUFF[chocolate['factory_level']]
        jackrabbit_multiplier: float = upgrades['jackrabbit'] * 0.01
        collection_multiplier: float = 0
        collection_production: float = 0

        for rarity, data in collection_data.items():
            collection_multiplier += EMPLOYEE_COLLECTION_MUL[rarity] * data['found_unique']
            collection_production += EMPLOYEE_COLLECTION_PROD[rarity] * data['found_unique']

        # Some mythic gives unique bonus
        if collection.get('Dante', 0) > 0:
            collection_production += 50
        if collection.get('Galaxy', 0) > 0:
            collection_multiplier += 0.05
        if collection.get('Sigma', 0) > 0:
            collection_production += 5 * len(collection_data['MYTHIC'])
        if collection.get('Zest Zephyr', 0) > 0:
            collection_multiplier += 0.03
            collection_production += 30

        collection_multiplier = round(collection_multiplier, 3)

        production['production'].append({"Employees": f"{employee_prod:,}"})
        production['production'].append({"Hoppity collection": collection_production, "comment": "This value may be inaccurate"}) # Inaccurate
        production['production'].append({"Chocolate Talisman": talisman_prod, "comment": f"Tier {talisman_prod/10:.0f}"}) # Assuming maxed

        production['multiplier'].append({"Hoppity collection": collection_multiplier, "comment": "This value may be inaccurate"})  # Inaccurate
        production['multiplier'].append({"Jackrabbit": jackrabbit_multiplier})
        production['multiplier'].append({"Factory Prestige": prestige_multiplier})
        production['multiplier'].append({"Booster Cookie": cookie_buff})

        total_prod: int = employee_prod + collection_production + talisman_prod
        total_mul: float = prestige_multiplier + jackrabbit_multiplier + collection_multiplier + cookie_buff
        tower_bonus: float = (upgrades['tower'] / 10) + 0.7 * bool(misc['shop_milestone'] >= 12)

        production['per_sec'] = f"{(total_prod * total_mul):,.2f}"
        production['per_sec_with_tower'] = f"{(total_prod * (total_mul + tower_bonus)):,.2f}"
        production['total_prod'] = f"{total_prod:,}"
        production['total_mul'] = f"{total_mul:,.3f}"
        production['tower_bonus'] = f"{tower_bonus:,.1f}"

        return {
            "employees": employees,
            "collection": rabbit_collection,
            "collection_data": collection_data,
            "upgrades": upgrades,
            "chocolate": chocolate,
            "misc": misc,
            "production": production,
        }

    def get_magical_power(self, profile: str = "selected") -> dict:
        talisman_bag = self.get_profile_data("inventory",
                                             profile=profile)

        if talisman_bag is not None:
            talisman_bag = talisman_bag.get("bag_contents", {}).get("talisman_bag", {}).get("data", {})

        final_dict: dict = {
            "magical_power": 0,
            "accessories": {
                "special": 0,
                "mythic": 0,
                "legendary": 0,
                "epic": 0,
                "rare": 0,
                "uncommon": 0,
                "common": 0,
            },
            "duplicates": {
                "special": [],
                "mythic": [],
                "legendary": [],
                "epic": [],
                "rare": [],
                "uncommon": [],
                "common": [],
            }
        }

        if talisman_bag == {} or talisman_bag is None:
            return final_dict

        talisman_bag = utils.process_inv(talisman_bag)

        special_count: int = talisman_bag.count("SPECIAL")
        mythic_count: int = talisman_bag.count("MYTHIC ACCESSORY")
        legendary_count: int = talisman_bag.count("LEGENDARY ACCESSORY")
        epic_count: int = talisman_bag.count("EPIC ACCESSORY")
        rare_count: int = talisman_bag.count("RARE ACCESSORY")
        uncommon_count: int = talisman_bag.count("UNCOMMON ACCESSORY")
        common_count: int = talisman_bag.count("COMMON ACCESSORY")

        return final_dict

    def get_jacob_stats(self, profile: str = "selected") -> dict:
        jacob_stats = self.get_profile_data("jacobs_contest", profile=profile)

        convenient_names: dict = {
            "INK_SACK:3": "COCOA",
            "POTATO_ITEM": "POTATO",
            "CARROT_ITEM": "CARROT",
            "NETHER_STALK": "NETHER_WART",
            "MUSHROOM_COLLECTION": "MUSHROOM"
        }
        personal_bests = {
            "PUMPKIN": 0,
            "MUSHROOM": 0,
            "CARROT": 0,
            "WHEAT": 0,
            "NETHER_WART": 0,
            "COCOA": 0,
            "POTATO": 0,
            "SUGAR_CANE": 0,
            "MELON": 0,
            "CACTUS": 0,
        }
        farming_icons: dict = {
            "PUMPKIN": "/images/farming/Pumpkin.webp",
            "MUSHROOM": "/images/farming/Mushroom.webp",
            "CARROT": "/images/farming/Carrot.webp",
            "WHEAT": '/images/farming/Wheat.webp',
            "NETHER_WART": "/images/farming/Nether_wart.webp",
            "COCOA": "/images/farming/Cocoa.webp",
            "POTATO": "/images/farming/Potato.webp",
            "SUGAR_CANE": "/images/farming/Sugar_cane.webp",
            "MELON": "/images/farming/Melon.webp",
            "CACTUS": "/images/farming/Cactus.webp",
        }
        medals_icons: dict = {
            "bronze": "/images/Brick.webp",
            "silver": "/images/Iron_ingot.webp",
            "gold": "/images/Gold_ingot.webp",
        }

        fetch_personal_bests: dict = jacob_stats.get("personal_bests", {})

        for key, value in fetch_personal_bests.items():
            # Replace names in the values list by convenient ones
            key = convenient_names.get(key, key)
            personal_bests[key] = f"{value:,}"

        medal_record: dict[str, list] = {"bronze": [], "silver": [], "gold": [], "platinum": [], "diamond": []}
        fetch_medal_record = jacob_stats.get("unique_brackets", {})

        for key, value in fetch_medal_record.items():
            # Replace names in the values list by convenient ones
            value = [convenient_names.get(category, category) for category in value]
            medal_record[key] = value


        medals_inv = jacob_stats.get("medals_inv", {})  # May return {} or None, so default output is unified as {}
        if medals_inv == {}:
            medals_inv = {"bronze": 0, "silver": 0, "gold": 0}

        # Apply number formatting
        medals_inv = {k:f"{v:,}" for k,v in medals_inv.items()}

        return {
            "medals": medal_record,
            "bests": personal_bests,
            "medals_inv": medals_inv,
            "farming_icons": farming_icons,
            "medals_icons": medals_icons
        }
