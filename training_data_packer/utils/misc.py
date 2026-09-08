import hashlib
from collections.abc import Callable
from copy import deepcopy

from iso639 import Lang
from loguru import logger


def hash_factory(hash_algo: str) -> Callable[[str], str]:
    match hash_algo.lower():
        case "sha256":
            return lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest()
        case "sha256-32":
            return lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest()[:32]
        case _:
            logger.error(f"Unknown hash algorithm {hash_algo}")
            raise ValueError(f"Unknown hash algorithm {hash_algo}")


def lang_to_name(lang: str) -> str:
    """
    Retrieves the full language name corresponding to the provided language code or locale string.
    The input string is processed by splitting on underscores to isolate the primary language
    identifier, which is then used to retrieve the associated name attribute from the Lang
    enumeration or class.

    :param lang: The language code or locale string to process, typically containing the primary
                 language identifier and optionally a region tag separated by an underscore.
    :return: The descriptive name of the language corresponding to the primary code extracted from
             the input.
    """
    return Lang(lang.split("_")[0]).name


def merge_hierarchy_dicts(dict_a, dict_b):
    """
    Recursively merges two dictionaries, `dict_a` and `dict_b`, by combining their keys and values.
    `dict_a`has precedence over `dict_b`.

    Parameters:
    dict_a: dict
        The first dictionary to merge.

    dict_b: dict
        The second dictionary to merge.

    Returns:
    dict
        A new dictionary containing the merged result of `dict_a` and `dict_b`.

    Raises:
    TypeError
        If either `dict_a` or `dict_b` is not a dictionary.
    """
    if isinstance(dict_a, dict) and isinstance(dict_b, dict):
        a_and_b = set(dict_a).intersection(dict_b)
        every_key = set(dict_a).union(dict_b)
        result = {
            k: merge_hierarchy_dicts(dict_a[k], dict_b[k])
            if k in a_and_b
            else deepcopy(dict_a[k] if k in dict_a else dict_b[k])
            for k in every_key
        }
        return result
    if dict_a is None:
        return deepcopy(dict_b)
    return deepcopy(dict_a)
