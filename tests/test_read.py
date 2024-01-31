import unittest

import readenv

from .utils import load


class LoadTestCase(unittest.TestCase):
    def test_unload(self) -> None:
        self.assertRaises(KeyError, readenv.bool, "__ENV_FOR_READENV_TEST_CASE__")
        with load():
            self.assertEqual(readenv.bool("__ENV_FOR_READENV_TEST_CASE__"), True)
        self.assertRaises(KeyError, readenv.bool, "__ENV_FOR_READENV_TEST_CASE__")


if __name__ == "__main__":
    unittest.main()
