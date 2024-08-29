import unittest
import os, sys
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"

from pydantic import ValidationError

from athena.routers import dto_models


class TestDtoModel(unittest.TestCase):

    def test_default_conv_ctl_creation(self):
        try:
            cc = dto_models.ConversationControl()
            self.assertIsNotNone(cc)
            print(cc)
            assert cc.thread_id == ""
            assert cc.agent_id == ""
            assert cc.chat_history == []
            assert cc.locale == "en"
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))
            self.fail()

    def test_default_resp_creation(self):
        try:
            cc = dto_models.ResponseControl()
            assert cc.chat_history == []
            print(cc)
        except ValidationError as exc:
            print(repr(exc.errors()[0]))
            self.fail()

if __name__ == '__main__':
    unittest.main()