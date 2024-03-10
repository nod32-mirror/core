import httpx
from configobj import ConfigObj

def get_mirrors(client: httpx.Client, config: ConfigObj) -> list:
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
        print(mirror)
    return mirrors