"""
TODO
"""

import httpx
from nod32_mirror._tools import add_scheme

def generate_client(config: dict) -> httpx.Client:
    """
    A function to generate a client based on the provided config.

    Args:
        config (dict): A dictionary containing the config.

    Returns:
        httpx.Client: A client object.
    """
    client = httpx.Client(
        auth=(config["ESET"]["MIRRORS"]["username"], config["ESET"]["MIRRORS"]["password"]),
        base_url=config["ESET"]["MIRRORS"]["mirror"],
    )
    return client
