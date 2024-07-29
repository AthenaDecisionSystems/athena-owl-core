import unittest
import sys
import os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from dotenv import load_dotenv
load_dotenv()


class TestImportThing(unittest.TestCase):

    def test_first_stuff(self):
        """
        Intent of the test
        """
        print("\n\n >>> test_first_stuff\n")
        pass


if __name__ == '__main__':
    unittest.main()
    