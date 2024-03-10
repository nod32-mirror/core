from configobj import ConfigObj
from nod32_mirror._versions import versions

def get_version_info(
    version: str,
    platforms: None | list[str] = None,
):
    print(version, platforms)
