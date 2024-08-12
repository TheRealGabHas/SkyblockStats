import stats_gather.consts as consts


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


def get_level_info_from_xp(xp: str, skill_table: list[int]):
    """
    Get the level progression for the given skill current_xp/required_xp
    :param xp: The amount of experience (a string such as "12,548,397")
    :param skill_table: A list of the required amount of experience for each level (such as [10, 50, 175, 500, ...])
    :return: A dict with the following keys : {"current_xp", "required_xp"}
    """
    skill_xp = int(xp.replace(",", ""))
    level = get_level_from_xp(xp, skill_table)

    current_xp = skill_xp - sum(skill_table[0:level]) if skill_xp > 0 else 0
    next_xp = skill_table[level + 1] if (len(skill_table) > level + 1) else 0

    return {"current_xp": current_xp, "required_xp": next_xp}


def get_context_for_profile(player: Profile, profile_name: str = "selected"):
    """
    Give the request context for a given player and a given profile name (default is the last selected profile)
    :param player: A player represented by a Profile object (already initialized, stats already gathered)
    :param profile_name: The "cute name" of the profile (like "Banana" or "Orange")
    :return: A dict containing the context with all the data for the template
    """
    # TODO: Add better error handling to prevent the usage of try/except
    try:
        slayer_data = player.get_slayer_data(profile_name)
    except Exception:
        slayer_data = None
    try:
        leveling_data = player.get_leveling_data(profile_name)
    except Exception:
        leveling_data = None
    try:
        rift_data = player.get_rift_data(profile_name)
    except Exception:
        rift_data = None
    try:
        misc_data = player.get_misc_stats(profile_name)
    except Exception:
        misc_data = None
    try:
        chocolate_data = player.get_chocolate_factory_stats(profile_name)
    except Exception:
        chocolate_data = None

    trophy_data = player.get_trophy_stats(profile_name)

    rank_data = {
        "rank": player.rank,
        "color": player.rank_color
    }

    profiles_data = player.get_profile_list()

    context: dict = {
                     "leveling_data": leveling_data, "slayer_data": slayer_data, "rift_data": rift_data,
                     "misc_data": misc_data, "trophy_data": trophy_data, "rank_data": rank_data,
                     "profiles_data": profiles_data, "chocolate_data": chocolate_data
                     }

    # Add a field if some data hasn't been correctly retrieved
    if None in context.values():
        context['api_warning'] = True

    return context


def get_barn_capacity(level: int):
    """
    Return the maximum number of slots in the Chocolate Factory barn at level X
    :param level: An integer representing the level of the barn
    :return: An integer corresponding to the barn capacity
    """

    # Default amount of slots is 20, each level adds 2 slots
    return 20 + (level - 1) * 2


def get_shop_milestone(chocolate_spent: int):
    """
    Return the Chocolate shop milestone
    :param chocolate_spent: An integer representing the total number of chocolate spent in the shop
    :return: An integer representing the shop milestone
    """
    i: int = 0

    while chocolate_spent > consts.CHOCOLATE_SHOP_MILESTONES[i]:
        i += 1
        continue

    return i


def get_rabbit_employee_data(employee_level: int) -> tuple:
    """
    :param employee_level: An integer representing the level of the rabbit employee
    :return: Title and Hex color code for the rabbit employee according to its level ("Director", 0xffffff)
    """

    # Get the employee rank
    i: int = 0
    level_list = list(consts.RABBITS_LEVEL.keys())

    while employee_level >= level_list[i]:
        if i + 1 >= len(level_list):
            break
        i += 1
        continue

    if employee_level >= 220:
        rank = consts.RABBITS_LEVEL[220]
    else:
        rank = consts.RABBITS_LEVEL[level_list[i-1]]

    return rank, f"#{consts.RABBITS_RANK_COLOR[rank]:06x}"

