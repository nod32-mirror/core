"""
Localization module for nod32_mirror
"""

import json
import os
from configobj import ConfigObj


class Translate:
    # pylint: disable=too-few-public-methods
    """
    A class for generating translations from a JSON language pack.

    This class is initialized with a ConfigObj configuration object and a
    language code. It then loads the JSON language pack from disk using the
    language code and provides a function for retrieving translations from
    the loaded JSON language pack.
    """

    def __init__(self, config: ConfigObj) -> None:
        """
        Initializes the class with the provided config object.

        Args:
            config (ConfigObj): The configuration object.

        Returns:
            None
        """
        self.config = config
        self.language = config["SCRIPT"]["language"]
        with open(
            os.path.join(
                os.path.dirname(__file__), "langpacks", f"{self.language}.json"
            ),
            encoding="utf-8",
        ) as f:
            self.langpack = json.load(f)

    def __call__(self, key: str) -> str:
        """
        A function which returns translation from langpack.
        Parameters:
            key (str): The key to look up in the 'languages' dictionary.
        Returns:
            str: The value associated with the given key.
        """
        keys = key.split(".")
        result = self.langpack
        for k in keys:
            result = result[k]
        return result
