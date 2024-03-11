from urllib.parse import urljoin
import random
import datetime
from configobj import ConfigObj
import httpx
from nod32_mirror._tools import add_scheme
from nod32_mirror._parser import get_info
from nod32_mirror._versions import _versions


def get_mirrors(client: httpx.Client) -> list[str]:
    """
    Get the list of mirrors from the server.

    Args:
        client (httpx.Client): The client to use.

    Returns:
        list: The list of mirrors.
    """
    response = client.get("eset_upd/business/latest/dll/update.ver")
    index = ConfigObj(response.text.splitlines())
    mirrors = []
    for mirror in index["SERVERS"]["list"]:
        mirrors.append(mirror.split("//")[1])
    return mirrors


def get_fastest_mirror(client: httpx.Client, mirrors: list[str]) -> str:
    """
    Get the fastest mirror from the list of mirrors.

    Args:
        client (httpx.Client): The client to use.
        mirrors (list): The list of mirrors.

    Returns:
        str: The fastest mirror.
    """
    files = get_info(random.choice(list(_versions)), client)["files"]
    mirrors_speeds = {mirror: datetime.timedelta() for mirror in mirrors}

    for _ in range(5):
        file = random.choice(files)
        for mirror in mirrors:
            print("Testing mirror", mirror)
            request = client.get(urljoin(add_scheme(mirror), file))
            print(f"Mirror: {mirror}, elapsed: {request.elapsed}")
            mirrors_speeds[mirror] += request.elapsed
    # return min(mirrors_speeds, key=mirrors_speeds.get).mirrors_speeds
    raise NotImplementedError
