type Profile = object  # Figurehead for the class defined in data_pickup.py


def order_dict(_dict: dict, key_order: list):
    """
    Return the given dictionary with keys ordered following the `key_order` argument.
    :param _dict: Initial dictionary
    :param key_order: The new key order
    :return: Ordered dictionary
    """
    new_dict = {}

    for key in key_order:
        new_dict[key] = _dict.get(key)

    return new_dict


def get_level_from_xp(xp: str, skill_table: list[int]) -> int:
    """
    Return the player level given an EXP amount and a skill leveling table
    :param xp: The amount of experience (a string such as "12,548,397")
    :param skill_table: A list of the required amount of experience for each level (such as [10, 50, 175, 500, ...])
    :return: An integer corresponding to the player level
    """
    skill_xp = int(xp.replace(",", ""))

    for i, lvl in enumerate(skill_table):
        if skill_xp > sum(skill_table[0:i]):
            continue
        else:
            return i - 1

    return len(skill_table)


def get_context_for_profile(player: Profile, profile_name: str = "selected"):
    """
    Give the request context for a given player and a given profile name (default is the last selected profile)
    :param player: A player represented by a Profile object (already initialized, stats already gathered)
    :param profile_name: The "cute name" of the profile (like "Banana" or "Orange")
    :return: A dict containing the context with all the data for the template
    """
    # TODO: Add better error handling to prevent the usage of try/except
    try:
        slayer_data = player.get_slayer_data()
    except Exception:
        slayer_data = None
    try:
        leveling_data = player.get_leveling_data()
    except Exception:
        leveling_data = None
    try:
        rift_data = player.get_rift_data()
    except Exception:
        rift_data = None
    try:
        misc_data = player.get_misc_stats()
    except Exception:
        misc_data = None

    trophy_data = player.get_trophy_stats()

    rank_data = {
        "rank": player.rank,
        "color": player.rank_color
    }

    profiles_data = player.get_profile_list()

    context: dict = {
                     "leveling_data": leveling_data, "slayer_data": slayer_data, "rift_data": rift_data,
                     "misc_data": misc_data, "trophy_data": trophy_data, "rank_data": rank_data,
                     "profiles_data": profiles_data
                     }

    return context
