import unittest, sys, os

module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("../../.env")
from athena.glossary import glossary_mgr


class TestLocaleManager(unittest.TestCase):
    """
    Local manager delivers localization supports for prompt and application messages
    """

    def test_glossary_local_manager(self):
        """
        should support setting new locale among supported locales
        """
        assert glossary_mgr.get_locale() == "en"
        newLoc = glossary_mgr.set_locale("es")
        assert newLoc == "es"
        assert glossary_mgr.get_locale() == "es"
        newLoc = glossary_mgr.set_locale("po")
        assert newLoc == None

    def test_all_supported(self):
        resp=glossary_mgr.get_supported_locales()   
        assert resp == ['en', 'fr', 'es']

    def test_creating_glossary(self):
        """
        after creating some phrases / sentences we can retrieve them from the glossary.
        """
        g = glossary_mgr.build_get_glossary("./src/athena/config/glossary.json")
        g.add_phrases(
            "NoClaims",
            {"fr": "Pas de sinistre pour ce client", "en": "No claims for this client"},
        )
        g.add_phrases(
            "ClaimNotFound",
            {
                "fr": "Sinistre $claim_id non trouvé pour le client $client_id",
                "en": "Claim $claim_id not found for client $client_id",
            },
        )
        resp = g.get_phrase("ClaimNotFound","fr")
        assert resp is not None
        resp = g.get_phrase("Bonjour","fr")
        print(resp)
        assert resp.find("phrase for Bonjour") >= 0
        resp = g.get_phrase("NoClaims")
        assert resp.find("claims for") > 0

if __name__ == '__main__':
    unittest.main()