"""
Config initializator
"""

from configparser import ConfigParser
import os

def init(path: str) -> ConfigParser:
    """
    Initialize a ConfigParser with the specified path.
    
    Args:
        path (str): the path to the directory

    Returns:
        ConfigParser object
    """
    if not os.path.isdir(path):
        os.mkdir(path)

    config = ConfigParser()
    config.read(os.path.join(path, "config.ini"))
    process_config(config)
    return config

def set_default(config: ConfigParser, section, key, value) -> None:
    """
    Sets the default value for the given key in the specified section of the configuration parser.

    Args:
        config (ConfigParser): The configuration parser object.
        section (str): The section in the configuration file.
        key (str): The key for the configuration value.
        value (str): The default value to set for the key.

    Returns:
        None
    """
    if not config.has_section(section):
        config.add_section(section)

    if not config.has_option(section, key):
        config.set(section, key, value)

# pylint: disable=unused-argument
def process_config(config: ConfigParser) -> None: 
    """
    todo
    """
