"""
Config initializator
"""

import os
from configobj import ConfigObj
from configobj.validate import Validator
from nod32_mirror._tools import create_files

def _config(path: os.path = "config.ini") -> ConfigObj:
    """
    Initialize a ConfigParser with the specified path.

    Args:
        path (str): the path to the directory

    Returns:
        ConfigParser object
    """
    config = ConfigObj(
        path,
        configspec=os.path.join(os.path.dirname(__file__), "configspec.conf"),
        raise_errors=True,
    )
    result = config.validate(Validator(), copy=True)
    if result is not True:
        raise ValueError(f"Configuration validation failed: {result}")
    config.write()
    service_path = os.path.join(".", "service")
    create_files([os.path.join(service_path, "keys.valid")])
    return config
