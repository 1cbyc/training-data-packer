import unittest

from parameterized import parameterized

from training_data_packer.utils.misc import lang_to_name, merge_hierarchy_dicts


class TestLangToName(unittest.TestCase):
    @parameterized.expand(
        [
            [
                "basic_eng",
                "eng",
                "English",
            ],
            [
                "basic_spa",
                "spa_Latn",
                "Spanish",
            ],
            [
                "basic_fra",
                "fra_Latn",
                "French",
            ],
            [
                "basic_deu",
                "deu_Latn",
                "German",
            ],
            [
                "basic_ita",
                "ita_Latn",
                "Italian",
            ],
            [
                "locale_eng_Latn",
                "eng_Latn",
                "English",
            ],
        ]
    )
    def test_lang_to_name(self, name, lang_code, expected_name):
        result = lang_to_name(lang_code)
        self.assertEqual(expected_name, result)


class TestMergeHierarchyDicts(unittest.TestCase):
    @parameterized.expand(
        [
            [
                "empty_dicts",
                {},
                {},
                {},
            ],
            [
                "dict_a_empty",
                {},
                {"a": 1, "b": 2},
                {"a": 1, "b": 2},
            ],
            [
                "dict_b_empty",
                {"a": 1, "b": 2},
                {},
                {"a": 1, "b": 2},
            ],
            [
                "flat_merge",
                {"a": 1, "b": 2},
                {"b": 3, "c": 4},
                {"a": 1, "b": 2, "c": 4},
            ],
            [
                "nested_merge",
                {"a": {"x": 1, "y": 2}},
                {"a": {"y": 3, "z": 4}},
                {"a": {"x": 1, "y": 2, "z": 4}},
            ],
            [
                "deep_nested_merge",
                {"a": {"b": {"c": 1}}},
                {"a": {"b": {"c": 2, "d": 3}}},
                {"a": {"b": {"c": 1, "d": 3}}},
            ],
            [
                "mixed_nested",
                {"a": {"x": 1}, "b": 2},
                {"a": {"y": 3}, "c": 4},
                {"a": {"x": 1, "y": 3}, "b": 2, "c": 4},
            ],
            [
                "list_values",
                {"a": [1, 2]},
                {"a": [3, 4]},
                {"a": [1, 2]},
            ],
            [
                "dict_from_a_not_dict_from_b",
                {"a": {"x": 1}},
                {"a": None},
                {"a": {"x": 1}},
            ],
            [
                "dict_from_b_not_dict_from_a",
                {"a": None},
                {"a": {"x": 1}},
                {"a": {"x": 1}},
            ],
            [
                "complex_structure",
                {
                    "metadata": {"language": "en", "version": 1},
                    "data": {"files": ["file1.txt"]},
                },
                {
                    "metadata": {"language": "fr", "region": "EU"},
                    "data": {"files": ["file2.txt"], "count": 5},
                    "stats": {"size": 100},
                },
                {
                    "metadata": {"language": "en", "version": 1, "region": "EU"},
                    "data": {"files": ["file1.txt"], "count": 5},
                    "stats": {"size": 100},
                },
            ],
        ]
    )
    def test_merge_hierarchy_dicts(self, name, dict_a, dict_b, expected):
        result = merge_hierarchy_dicts(dict_a, dict_b)
        self.assertEqual(expected, result)

    def test_merge_hierarchy_dicts_deepcopy(self):
        dict_a = {"a": [1, 2]}
        dict_b = {}
        result = merge_hierarchy_dicts(dict_a, dict_b)
        result["a"].append(3)
        self.assertEqual(dict_a["a"], [1, 2])

    def test_merge_hierarchy_dicts_deepcopy_nested(self):
        dict_a = {"a": {"b": [1, 2]}}
        dict_b = {}
        result = merge_hierarchy_dicts(dict_a, dict_b)
        result["a"]["b"].append(3)
        self.assertEqual(dict_a["a"]["b"], [1, 2])


if __name__ == "__main__":
    unittest.main()
