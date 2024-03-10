"""
Tools for nod32_mirror module
"""

from urllib.parse import urlparse, urlunparse

def add_protocol(url: str, protocol: str = "https") -> str:
    """
    Takes a URL as input and returns the corresponding HTTPS URL.
    Args:
        url (str): the input URL.
    Returns:
        str: the corresponding HTTPS URL.
    """
    return urlunparse(urlparse(url)._replace(scheme=protocol))
