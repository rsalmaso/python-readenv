import unittest

import readenv

from .utils import load


class LoadTestCase(unittest.TestCase):
    def test_unload(self) -> None:
        self.assertRaises(KeyError, readenv.bool, "__ENV_FOR_READENV_TEST_CASE__")
        with load():
            self.assertEqual(readenv.bool("__ENV_FOR_READENV_TEST_CASE__"), True)
        self.assertRaises(KeyError, readenv.bool, "__ENV_FOR_READENV_TEST_CASE__")


class CastTestCase(unittest.TestCase):
    def test_int(self) -> None:
        with load():
            self.assertEqual(readenv.int("INT_ENV"), 1)

    def test_bool(self) -> None:
        with load():
            self.assertEqual(readenv.bool("TRUE_ENV_1"), True)
            self.assertEqual(readenv.bool("TRUE_ENV_2"), True)
            self.assertEqual(readenv.bool("TRUE_ENV_3"), True)
            self.assertEqual(readenv.bool("TRUE_ENV_4"), True)
            self.assertEqual(readenv.bool("TRUE_ENV_5"), True)
            self.assertRaises(ValueError, readenv.bool, "TRUE_ENV_FAIL")
            self.assertEqual(readenv.bool("FALSE_ENV_1"), False)
            self.assertEqual(readenv.bool("FALSE_ENV_2"), False)
            self.assertEqual(readenv.bool("FALSE_ENV_3"), False)
            self.assertEqual(readenv.bool("FALSE_ENV_4"), False)
            self.assertEqual(readenv.bool("FALSE_ENV_5"), False)
            self.assertRaises(ValueError, readenv.bool, "FALSE_ENV_FAIL")

    def test_float(self) -> None:
        with load():
            self.assertEqual(readenv.float("FLOAT_ENV_1"), 0.5)
            self.assertEqual(readenv.float("FLOAT_ENV_2"), 0.5)
            self.assertEqual(readenv.float("FLOAT_ENV_3"), 3.0)
            self.assertEqual(readenv.float("FLOAT_ENV_4"), 3e2)

    def test_list(self) -> None:
        with load():
            self.assertEqual(readenv.list("LIST_ENV_1"), [])
            self.assertEqual(readenv.list("LIST_ENV_1", cast=int), [])
            self.assertEqual(readenv.list("LIST_ENV_2"), ["42"])
            self.assertEqual(readenv.list("LIST_ENV_2", cast=int), [42])
            self.assertEqual(readenv.list("LIST_ENV_3"), ["42"])
            self.assertEqual(readenv.list("LIST_ENV_3", cast=int), [42])
            self.assertEqual(readenv.list("LIST_ENV_4"), ["42", "43"])
            self.assertEqual(readenv.list("LIST_ENV_4", cast=int), [42, 43])

    def test_tuple(self) -> None:
        with load():
            self.assertEqual(readenv.tuple("TUPLE_ENV_1"), ())
            self.assertEqual(readenv.tuple("TUPLE_ENV_1", cast=int), ())
            self.assertEqual(readenv.tuple("TUPLE_ENV_2"), ("42",))
            self.assertEqual(readenv.tuple("TUPLE_ENV_2", cast=int), (42,))
            self.assertEqual(readenv.tuple("TUPLE_ENV_3"), ("42",))
            self.assertEqual(readenv.tuple("TUPLE_ENV_3", cast=int), (42,))
            self.assertEqual(readenv.tuple("TUPLE_ENV_4"), ("42", "43"))
            self.assertEqual(readenv.tuple("TUPLE_ENV_4", cast=int), (42, 43))

    def test_dict(self) -> None:
        with load():
            self.assertEqual(readenv.dict("DICT_ENV_1"), {})
            self.assertEqual(readenv.dict("DICT_ENV_2"), {"question": "unknown", "answer": "42"})
            self.assertRaises(ValueError, readenv.dict, "INVALID_DICT_ENV_1")

    def test_json(self) -> None:
        with load():
            self.assertEqual(readenv.json("JSON_ENV_1"), {})
            self.assertEqual(readenv.json("JSON_ENV_2"), {"question": "unknown", "answer": 42})
            self.assertEqual(readenv.json("JSON_ENV_3"), {"question": "unknown", "answer": 42})


if __name__ == "__main__":
    unittest.main()
