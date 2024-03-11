"""
Retrieve information about ESET NOD32 versions.
"""

from configobj import ConfigObj
import httpx
from nod32_mirror._versions import _versions


def get_info(version: str, client: httpx.Client = httpx.Client):
    """
    A function to retrieve information based on the provided version and client.

    Args:
        version (str): The version for which information is to be retrieved.
        client (httpx.Client, optional): The HTTP client to use for making requests.

    Returns:
        dict: A dictionary containing the version and a list of files.
    """
    index = ConfigObj(client.get(_versions[version]["index"]).text.splitlines())
    files = []
    versionid = 0
    for section in index.sections:
        current = index[section]

        if current.get("file"):
            files.append(current["file"])

        if current.get("versionid") and (int(current.get("versionid"))) > versionid:
            versionid = int(current["versionid"])
    return {"version": versionid, "files": files, "name": _versions[version]["name"]}
