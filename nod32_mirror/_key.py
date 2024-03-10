"""
TODO
"""

import random
import re
import os
import httpx
from configobj import ConfigObj
from nod32_mirror._tools import add_scheme
from nod32_mirror._versions import _versions

def test_key(key: str, config: ConfigObj) -> bool:
    """
    Checks if the given key is valid.

    Args:
        key (str): The key to be checked.

    Returns:
        bool: True if the key is valid, False otherwise.
    """
    pattern = re.compile(r"((EAV|TRIAL)-[0-9]{10}):+?([a-z0-9]{10})")
    if not pattern.match(key):
        return False
    login, _, password = pattern.match(key).groups()
    client = httpx.Client(
        auth=(login, password),
        base_url=add_scheme(config["ESET"]["MIRRORS"]["mirror"]),
    )
    try:
        version = random.choice(list(_versions.keys()))
        response = client.get(f"{_versions[version]['index']}")
        response.raise_for_status()
    except httpx.HTTPStatusError:
        return False
    finally:
        client.close()
    return True

def get_key(config: ConfigObj) -> str:
    """
    Get the key from the config.

    Args:
        config (ConfigObj): The config object.

    Returns:
        str: The key.
    """
    keys_filepath = os.path.join(config["SCRIPT"]["DIRECTORIES"]["service"], "keys.valid")
    with open(keys_filepath, "r", encoding="utf-8") as f:
        keys = f.read().splitlines()
    if len(keys) == 0:
        raise ValueError("No keys found in the keys.valid file")
    for key in keys:
        if test_key(key, config):
            break
        keys.remove(key)
    with open(keys_filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(keys))
    if len(keys) == 0:
        raise ValueError("No valid keys")
    return keys[0].split(":")
