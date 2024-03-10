"""
Config initializator
"""

import os
from configobj import ConfigObj
from configobj.validate import Validator


def _config(path: os.path) -> ConfigObj:
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
    return config
