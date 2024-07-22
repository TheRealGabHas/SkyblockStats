import sys
import datetime
import json

import requests

import stats_gather.consts
import stats_gather.s_utils as utils
import stats_gather.consts as consts
from stats_gather.consts import SKILLS, SLAYER_XP_REQUIREMENTS, SLAYER_MAX_BOSS_TIER, SLAYER_BOSS_ICONS, TIMECHARMS


with open("stats_gather/credentials.json", "r") as file:
    header = json.load(file)
    if header.get("API-Key") is None:
        sys.exit(1)


class Profile:

    def __init__(self, uuid: str):
        self.data = None
        self.uuid: str = uuid
        self.rank: str = "None"
        self.skyblock_profiles: dict = {}

    def gather_rank(self):
        rank_data = requests.get(f"https://api.hypixel.net/v2/player?uuid={self.uuid}", headers=header).json()
        if rank_data is not None:
            self.rank = rank_data['player'].get('newPackageRank', "None")
            self.rank = self.rank.replace("PLUS", "+").replace("_", "")

            if rank_data['player']['stats'].get('SkyBlock', None) is not None:
                self.skyblock_profiles = rank_data['player']['stats']['SkyBlock']['profiles']

    def gather_stats(self) -> bool:
        _data = requests.get(f"https://api.hypixel.net/skyblock/profiles?uuid={self.uuid}", headers=header).json()
        # print(_data)
        # with open("temp.json", "w") as file:
        #     __import__("json").dump(_data, file)

        if _data['success']:
            self.data = _data

        return _data['success']

    def get_stats(self) -> dict:
        return self.data

    def get_selected_profile(self) -> dict | None:
        if self.data is None:
            return {}
        if self.data.get('profiles') is None:
            return {}

        for profile in self.data['profiles']:
            if profile['selected']:
                return profile['members'][self.uuid.replace("-", "")]
                # Returns queried user profile in the coop. Replacing the uuid dashes

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

        xp_data['Global'] = {
            "xp": global_level,
            "icon_path": "/images/Skyblock_Levels.webp"
        }

        for skill in SKILLS:
            key = skill.lower().capitalize()
            value = self.get_selected_profile().get(f'experience_skill_{skill.lower()}', 0)

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
                    boss_kills.append({f"Tier {i + 1}": v})
                elif SLAYER_MAX_BOSS_TIER[boss] >= i + 1:  # A boss of Tier 5 exists
                    boss_kills.append({f"Tier {i + 1}": 0})

            final_dict[boss.capitalize()] = {
                "current_level": len(sl_data[boss].get("claimed_levels", {}).keys()),  # Current level
                "xp": current_xp,
                "next_lvl_xp": next_level_xp,
                "boss_kills": boss_kills,
            }

        # Making sure every card has a least the icon  (even if the boss was never fought/ beaten)
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

        if trophies is None:
            rift_data['trophies'] = []
        else:
            # (Timecharm name, unlocked at visit)
            trophy_lst = [(trophy['type'].replace("_", " ").capitalize() + " Timecharm", trophy['visits'])
                          for trophy in trophies]
            rift_data['trophies'] = trophy_lst

        for trophy in TIMECHARMS:
            if trophy not in (tr for tr, _ in rift_data['trophies']):
                missing_trophies.append(trophy)

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
            "Bank Upgrade": bank_level
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
        elif s := trophy_stats.get('rewards', [0])[0] > 0:
            reward_tier = consts.TROPHY_REWARDS[s-1]
        else:
            reward_tier = "No claimed reward"

        total_caught = f"{trophy_stats['total_caught']:,.0f}"
        misc_trophy_stats = {
            "Claimed reward": reward_tier,
            "Trophy caught count": total_caught,
        }
        fish_record = []

        for fish in consts.TROPHY_FISH:
            label = fish.replace("_", " ").capitalize()
            current_fish = {label: {}}

            for rarity in consts.TROPHY_RARITIES:
                current_fish[label][rarity.capitalize()] = fishes.get(f"{fish}_{rarity}", "X")

            current_fish["icon_path"] = f"/images/{label}_bronze.webp"
            fish_record.append(current_fish)

        return fish_record, misc_trophy_stats
