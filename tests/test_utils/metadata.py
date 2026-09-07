from copy import deepcopy

minimal_metadata_dict = {"name": "dataset name", "release": {"default": {"input": "source", "pack": "flat"}}}


def merge_hierarchy_dicts(dict_a, dict_b):
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
    return deepcopy(dict_b)
