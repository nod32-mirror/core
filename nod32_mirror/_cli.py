"""
# todo
"""

import sys
import os
import click
import httpx
from loguru import logger
from nod32_mirror._config import _config
from nod32_mirror._download import download_file, multiple_download
from nod32_mirror._key import get_key
from nod32_mirror._parser import get_info
from nod32_mirror._tools import add_scheme
# from nod32_mirror._translate import Translate
from nod32_mirror._versions import _versions


@click.group()
def cli():
    """
    Command line interface for nod32_mirror.
    """


@cli.command("update", help="Update current versions")
@click.option("--config", default="config.ini", help="Config file path")
@click.option("--debug", is_flag=True, default=False, help="Debug mode")
def update(config, debug):
    config = _config(config)
    logger.remove()
    if config["SCRIPT"]["LOGGING"]["stdout"]:
        logger.add(sys.stdout, level=("DEBUG" if debug else "INFO"))
    if config["SCRIPT"]["LOGGING"]["file"]:
        logger.add(
            config["SCRIPT"]["LOGGING"]["file"],
            level=("DEBUG" if debug else "INFO"),
        )
    # t = Translate(config)
    key = get_key(config)
    logger.info(f"Found valid key: {key[0]}")
    versions = []
    for version in _versions:
        if config["ESET"]["VERSIONS"][version]:
            versions.append(version)
    logger.info(f"Versions for mirrorring: {", ".join(versions)}")
    client = httpx.Client(
        auth=key,
        base_url=add_scheme(config["ESET"]["MIRRORS"]["mirror"]),
        transport=httpx.HTTPTransport(retries=5),
        timeout=httpx.Timeout(5, read=None),
    )
    for version in versions:
        info = get_info(version, client)
        logger.info(f"Mirroring version {version}...")
        d = multiple_download(
            urls=info["files"],
            client=client,
            target_dir=config["SCRIPT"]["DIRECTORIES"]["www"],
            max_workers=config["SCRIPT"]["CONNECTION"]["threads"],
        )
        download_file(
            url=_versions[version]["index"],
            client=client,
            target_path=os.path.join(
                config["SCRIPT"]["DIRECTORIES"]["www"],
                "eset_upd",
                version,
                "update.ver",
            ),
        )
        logger.info(f"Downloaded {d[0]} files, skipped {d[1]} files")
        logger.success(f"Version {version} mirrored")


@cli.command("current", help="Show current versions")
def current():
    """
    Show current versions
    """
    print("Current action")


@cli.command("check", help="Check updates for current versions")
def check():
    """
    Check updates for current versions
    """
    print("Check action")
