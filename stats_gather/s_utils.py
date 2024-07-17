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
    skill_xp = int(xp.replace(",", ""))

    for i, lvl in enumerate(skill_table):
        if skill_xp > sum(skill_table[0:i]):
            continue
        else:
            return i - 1

    return len(skill_table)
