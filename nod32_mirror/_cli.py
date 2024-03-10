"""
# todo
"""

import click


@click.group()
def cli():
    """
    Command line interface for nod32_mirror.
    """


@cli.command("update", help="Update current versions")
def update():
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
    print("Update action")


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
