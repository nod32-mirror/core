"""
# todo
"""

import click
from nod32_mirror._config import _config
from nod32_mirror._download import Download, download_file
from nod32_mirror._key import get_key
from nod32_mirror._parser import get_info
from nod32_mirror._tools import add_scheme
from nod32_mirror._translate import Translate
from nod32_mirror._versions import _versions

@click.group()
def cli():
    """
    Command line interface for nod32_mirror.
    """


@cli.command("update", help="Update current versions")
@click.option("--config", default="config.ini")
def update(config: str = "config.ini"):
    """
    1. Проверяем текущие ключи, если нет ни одного рабочего - выдаем ошибку
    2. Если пользователь указал надобность получить зеркала - получаем, проверяем, какой
    быстрее отдаст файл выбираем быстрейшний из них
    3. Проверяем, какие версии выбраны для зеркалирования, формируем список версий
    для зеркалирования
    4. Запускаем цикл по версиям. Для каждой версии парсим update.ver, получаем 
    список файлов и скачиваем в папку из конфигурации, сохраняем в ту же папку по пути
    {www}/eset_upd/{version}/update.ver
    """
    config = _config(config)
    t = Translate(config)
    key = get_key(config)
    versions = []
    for version in _versions:
        if config["ESET"]["MIRRORS"][version]:
            versions.append(version)

    


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
