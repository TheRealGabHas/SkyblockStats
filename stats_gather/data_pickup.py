import sys
import datetime
import json
import uuid as lib_uuid

import requests

import stats_gather.consts
import stats_gather.s_utils as utils
import stats_gather.consts as consts
from stats_gather.consts import (SKILLS, SLAYER_XP_REQUIREMENTS, SLAYER_MAX_BOSS_TIER, SLAYER_BOSS_ICONS, TIMECHARMS,
                                 RANKS_COLOR, LEVELS_COLOR)


with open("stats_gather/credentials.json", "r") as file:
    header = json.load(file)
    if header.get("API-Key") is None:
        sys.exit(1)


class Profile:

    def __init__(self, uuid: str):
        self.data = None
        self.uuid: str = uuid
        self.rank: str = "None"
        self.rank_color: str = "0xfff"
        self.skyblock_profiles: list = []

    def gather_rank(self):
        rank_data = requests.get(f"https://api.hypixel.net/v2/player?uuid={self.uuid}", headers=header).json()
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

    def gather_stats(self) -> bool:
        _data = requests.get(f"https://api.hypixel.net/skyblock/profiles?uuid={self.uuid}", headers=header).json()

        if _data['success']:
            self.data = _data

        return _data['success']

    def get_stats(self) -> dict:
        return self.data

    def get_selected_profile(self) -> dict | None:
        """
        Fetch the selected profile and returns the associated datas (JSON dict)
        :return: JSON dictionary containing the profile data
        """
        if self.data is None:
            return {}
        if self.data.get('profiles') is None:
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
        if self.data.get('profiles') is None:
            return profile_list

        for profile in self.data['profiles']:
            profile_list.append({
                "uuid": profile['profile_id'],
                "name": profile['cute_name'],
                "selected": profile['selected'],
                "game_mode": profile.get('game_mode', 'normal')  # This field is only defined if custom game mode
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
            return self.get_selected_profile().get(searched_field)
        for _profile in self.get_stats()['profiles']:
            if _profile['cute_name'].lower() == profile.lower():
                if _profile['members'][self.uuid.replace("-", "")]:
                    return _profile['members'][self.uuid.replace("-", "")].get(searched_field)

    def get_leveling_data(self, profile: str = "selected") -> dict:
        xp_data: dict = {}

        global_level = self.get_profile_data("leveling", profile=profile)['experience']
        level_color = 0xbebebe

        for level, color in LEVELS_COLOR.items():
            if global_level*0.01 > level:
                level_color = color
            else:
                break

        xp_data['Global'] = {
            "xp": global_level,
            "icon_path": "/images/Skyblock_Levels.webp",
            "color": f"#{level_color:06x}"
        }

        for skill in SKILLS:
            key = skill.lower().capitalize()
            value = self.get_profile_data(f'experience_skill_{skill.lower()}', profile=profile)

            if value is None:
                value = 0

            if key == "Social2":
                skill_table = consts.SOCIAL_XP_REQUIREMENTS
            elif key == "Runecrafting":
                skill_table = consts.RUNECRAFTING_XP_REQUIREMENTS
            else:
                skill_table = consts.SKILLS_XP_REQUIREMENTS

            xp_data[key] = {
                "xp": f"{round(value):,}",
                "icon_path": f"/images/{key}.webp"
            }

            if key != "Global":
                xp_data[key]['level'] = utils.get_level_from_xp(f"{round(value):,}", skill_table=skill_table)

        # TODO: Take the Taming and Runecrafting level cap into account

        return xp_data

    def get_slayer_data(self, profile: str = "selected") -> dict:
        searched_field: str = "slayer_bosses"
        sl_data = self.get_profile_data(searched_field, profile=profile)

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
                        return f"{level:,} EXP"

        # Formatting the data
        final_dict: dict = {}

        for boss in sl_data:
            if (c := sl_data[boss].get('xp')) is not None:
                current_xp = f"{c:,}"
                next_level_xp = find_next_xp_req(boss, xp=int(c))
            else:
                current_xp = "0"
                next_level_xp = find_next_xp_req(boss, xp=0)

            boss_kills = []
            for i in range(5):
                if (v := sl_data[boss].get(f'boss_kills_tier_{i}')) is not None:
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

        trophies = global_rift.get('gallery', {}).get('secured_trophies')
        souls = global_rift.get('enigma', {}).get('found_souls', [])
        lonely = global_rift.get('village_plaza', {}).get('lonely', {}).get('seconds_sitting')
        montezuma = global_rift.get('dead_cats', {})
        burger = global_rift.get('castle', {}).get('grubber_stacks', 0)

        current_motes = int(self.get_profile_data('motes_purse', profile=profile))

        stats = self.get_profile_data('stats', profile=profile)
        lifetime_motes = int(stats.get('rift_lifetime_motes_earned', 0))
        orb_picked = int(stats.get('rift_motes_orb_pickup', 0))

        missing_trophies = []
        found_trophies = []

        if trophies is None:
            rift_data['trophies'] = []
        else:
            # (Timecharm name, unlocked at visit)
            for trophy in trophies:
                trophy['icon_path'] = f"/images/rift/{trophy['type']}.png"
                trophy['type'] = " ".join(word.capitalize() for word in trophy['type'].replace("_", " ").split())
                del trophy['timestamp']
                found_trophies.append(trophy)

        rift_data['trophies'] = found_trophies

        for trophy in TIMECHARMS:
            if trophy not in (tr['type'] for tr in rift_data['trophies']):
                missing_trophies.append({
                    "type": trophy,
                    "icon_path": f"/images/rift/{" ".join(word.lower() for word in trophy.replace("_", " ").split())}.png"
                })

        rift_data['missing_trophies'] = missing_trophies

        # Number of found Enigma souls
        rift_data['souls'] = len(souls)

        # Amount of time spent sitting alone (minutes, seconds)
        if lonely is None:
            rift_data['time_sitting'] = (0, 0)
        else:
            rift_data['time_sitting'] = int(lonely / 60), lonely % 60

        # Amount of Montezuma soul fragments found
        rift_data['montezuma'] = len(montezuma.get('found_cats', []))

        rift_data['burger'] = burger

        rift_data['motes'] = f"{current_motes:,}"
        rift_data['lifetime_motes'] = f"{lifetime_motes:,}"
        rift_data['orbs'] = f"{orb_picked:,}"

        return rift_data

    def get_misc_stats(self, profile: str = "selected"):
        join_date = self.get_profile_data("first_join", profile=profile)
        soulflow = self.get_profile_data("soulflow", profile=profile)
        fishing_treasures = self.get_profile_data("fishing_treasure_caught", profile=profile)
        fairy_souls = self.get_profile_data("fairy_souls_collected", profile=profile)
        coin_purse = self.get_profile_data("coin_purse", profile=profile)
        bank_level = self.get_profile_data("personal_bank_upgrade", profile=profile)

        first_join = datetime.datetime.fromtimestamp(int(join_date / 1000)).strftime('%Y-%m-%d %H:%M:%S')

        if soulflow is None:
            soulflow = 0

        if coin_purse is None:
            coin_purse = 0

        final_dict: dict = {
            "First Join": first_join,
            "Soulflow": f"{soulflow:,.0f}",
            "Fished Treasures": f"{fishing_treasures:,.0f}",
            "Fairy Souls": fairy_souls,
            "Purse": f"{coin_purse:,.2f} coins",
            "Personal Bank Upgrade": bank_level
        }

        return final_dict

    def get_trophy_stats(self, profile: str = "selected"):
        trophy_stats = self.get_profile_data("trophy_fish", profile=profile)

        # The player never fished trophy
        if trophy_stats is None:
            return None

        if trophy_stats.get('total_caught', 0) < 1:
            return None

        fishes = list(trophy_stats.keys())
        for misc_item in stats_gather.consts.TROPHY_MISC:
            fishes.remove(misc_item) if misc_item in fishes else ()
        fishes.sort()

        fishes = {_key: trophy_stats[_key] for _key in fishes}

        # Check if the reward level is at least 1
        if len(trophy_stats.get('rewards', [])) == 0:
            reward_tier = "No claimed reward"
        elif (s := trophy_stats.get('rewards', [0])[-1]) > 0:
            reward_tier = consts.TROPHY_REWARDS[s-1]
        else:
            reward_tier = "No claimed reward"

        reward_icons: dict = {
            "Bronze Hunter Reward": "/images/Leather_Tunic.webp",
            "Silver Hunter Reward": "/images/Iron_Chestplate.webp",
            "Gold Hunter Reward": "/images/Gold_Chestplate.webp",
            "Diamond Hunter Reward": "/images/Diamond_Chestplate.webp",
        }

        total_caught = f"{trophy_stats['total_caught']:,.0f}"
        misc_trophy_stats = {
            "Claimed reward": {
                "name": reward_tier,
                "icon_path": reward_icons[reward_tier]
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

            current_fish["icon_path"] = f"/images/{label}_bronze.webp"
            fish_record.append(current_fish)

        print(misc_trophy_stats)
        return fish_record, misc_trophy_stats

    def get_chocolate_factory_stats(self, profile: str = "selected"):
        cf = self.get_profile_data("events", profile=profile)

        # If the player has no chocolate factory
        if cf is None:
            return {}

        # Fetch the chocolate factory statistics
        cf = cf.get("easter")

        # Fetch the level of every rabbit employee (0 = not unlocked)
        default_state: dict = {
            "level": 0,
            "rank": "Not unlocked",
            "color": "#9e9e9e",
            "icon_path": "/images/Barrier.webp",
        }

        employees = {
            'rabbit_bro': 0,
            'rabbit_cousin': 0,
            'rabbit_sis': 0,
            'rabbit_father': 0,
            'rabbit_grandma': 0,
            'rabbit_uncle': 0,
            'rabbit_dog': 0,
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
            collection[str(rabbit_name).replace("_", " ").capitalize()] = quantity

        if collection.get("Collected eggs") is not None:
            del collection["Collected eggs"]
        if collection.get("Collected locations") is not None:
            del collection["Collected locations"]

        # Fetch the chocolate factory upgrades level
        upgrades: dict = {
            "barn": cf.get("rabbit_barn_capacity_level", 0),
            "click": cf.get("click_upgrades", 0),
            "tower": cf.get("time_tower", {}).get("level", 0),
            "shrine": cf.get("rabbit_rarity_upgrades", 0),
            "jackrabbit": cf.get("chocolate_multiplier_upgrades", 0),
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
        }
        misc["shop_milestone"] = utils.get_shop_milestone(misc["shop_spent"])
        misc["chocolate_bar_counter"] = f"{misc["chocolate_bar_counter"]:,.0f}"
        misc['shop_spent'] = f"{misc["shop_spent"]:,.0f}"

        return {
            "employees": employees,
            "collection": collection,
            "upgrades": upgrades,
            "chocolate": chocolate,
            "misc": misc,
        }
