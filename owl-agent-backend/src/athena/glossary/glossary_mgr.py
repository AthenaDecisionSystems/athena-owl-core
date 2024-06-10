"""
Copyright 2024 Athena Decision Systems
@author Harley Davis
"""

from typing import Callable, Dict, List
import json
"""
A Locale Manager
"""

CURRENT_LOCALE = "en"
SUPPORTED_LOCALES = ["en", "fr", "es"]
DEFAULT_LOCALE = "en"

def get_locale() -> str:
    """Get the current locale for the assistant.

    Returns:
        str: The current locale for the assistant.
    """
    return CURRENT_LOCALE


def set_locale(locale: str) -> str:
    """Set the current locale for the assistant.

    Args:
        locale (str): The new locale for the assistant.

    Returns:
        str: The new locale for the assistant.
    """
    if locale not in SUPPORTED_LOCALES:
        return None
    global CURRENT_LOCALE
    CURRENT_LOCALE = locale
    return CURRENT_LOCALE

def get_supported_locales() -> List[str]:
    """Get the supported locales for the assistant.

    Returns:
        List[str]: The supported locales for the assistant.
    """
    return SUPPORTED_LOCALES

# -------------------------- Glossary mgt -------------------------------------------

class Glossary:
    _instance = None
    
    def save_glossary(cls, path: str = "glossary.json"):
        """Save the entire glossary in external file."""
        with open(path, "w", encoding="utf-8") as of:
            json.dump(cls._GLOSSARY, of, indent=4, ensure_ascii=False)
        return path


    def load_glossary(cls, path: str):
        """Reads the glossary from a file."""
        with open(path, "r", encoding="utf-8") as f:
            cls._GLOSSARY = json.load(f)
        return path


    def add_phrase(cls, msg: str, locale: str, translation: str):
        """Adds a new phrase to the glossary.

        Args:
            msg (str): The name of the message.
            translation (str): The translation of the phrase.
            lang (str): The language of the translation. Defaults to "en".
        """
        entry = cls._GLOSSARY.get(msg, None)
        if entry == None:
            entry = dict()
            cls._GLOSSARY[msg] = entry
        entry[locale] = translation
        return msg


    def add_phrases(cls, msg: str, translations: Dict[str, str]):
        """Adds a new phrase to the glossary.

        Args:
            msg (str): The name of the message.
            translations (Dict[str, str]): The translations of the phrase.   Each entry is a language code and the translation.
        """
        entry = cls._GLOSSARY.get(msg, None)
        if entry == None:
            entry = dict()
            cls._GLOSSARY[msg] = entry
        for lang, translation in translations.items():
            entry[lang] = translation
        return msg


    def get_phrase(cls, msg: str, locale: str = CURRENT_LOCALE) -> str:
        """Gets the message translation from the message name and locale.
        If the message is not found, it returns a message indicating that the message is not found.
        If there is no translation in the current locale, the translation in the default locale is returned.

        Args:
            msg (str): The message type.
            locale (str): The locale of the message. Defaults to "en".
        """
        gentry = cls._GLOSSARY.get(msg, None)
        if gentry == None:
            return f"No phrase for {msg}"
        else:
            res = gentry.get(locale, gentry.get(DEFAULT_LOCALE, None))
            if res == None:
                return f"No phrase for {msg} in {locale}"
            else:
                return res


def build_get_glossary(path:str ) -> Glossary:
    if Glossary._instance is None:
        Glossary._instance = Glossary()
        Glossary._instance.load_glossary(path)
    return Glossary._instance