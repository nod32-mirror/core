"""
Tools for nod32_mirror module
"""

from urllib.parse import urlparse, urlunparse


def add_scheme(url: str, scheme: str = "https") -> str:
    """
    Add the specified scheme to the given URL if it doesn't already have a scheme.
    Parameters:
    - url: a string representing the URL
    - scheme: a string representing the scheme to be added to the URL
    Returns:
    - a string representing the URL with the added scheme
    """
    return (
        urlunparse((scheme, *urlparse(url)[1:])).replace(
            f"{scheme}:///", f"{scheme}://"
        )
        if not urlparse(url).scheme
        else url
    )
