# -*- coding: utf-8 -*-

""" -------------------------------------------------------
    Like REDIS

    Функции:
Добавить ключ/обновить значение ключа
Уничтожить ключ и его значение

------------------------------------------------------- """

import asyncio
import traceback
from aiohttp import web
from concurrent.futures import ThreadPoolExecutor

from class_Config import Config
from logger import Logger
from class_HTTPProcessor import HTTPProcessor
from class_Storage import Storage


async def restart_loop(http_server) -> None:
    """
        Остановка сервиса
    """

    while Config().is_started:
        await asyncio.sleep(1)

    await asyncio.sleep(2)

    await http_server.shutdown()
    await http_server.cleanup()

    return


def init_print() -> None:
    """
        Печать шапки лог-файла
    """

    Logger.info('')
    Logger.info('System started.')

    return


def init_manager(params):
    """
        Инициализация всех ключевых объектов
    """
    loop = asyncio.get_event_loop()
    tpe = ThreadPoolExecutor(max_workers=10)

    lgr = Logger(params=params)

    storage = Storage(params=params, logger=lgr, tpe=tpe)
    loop.create_task(storage.loop_snapshot())
    Config().add_subscriber(storage)
    storage.snapshot_load()

    HTTPProcessor(params=params, logger=lgr, storage=storage)

    http_server = web.Application()
    http_server.router.add_route('GET',      '/key/{name}',   HTTPProcessor().read)
    http_server.router.add_route('POST',     '/key/{name}',   HTTPProcessor().set)
    http_server.router.add_route('DELETE',   '/key/{name}',   HTTPProcessor().remove)
    http_server.router.add_route('GET',      '/dump',         HTTPProcessor().dump)
    http_server.router.add_route('GET',      '/restart',      HTTPProcessor().restart)

    return http_server


def main(params):
    loop = asyncio.get_event_loop()

    http_server = init_manager(params)
    init_print()

    try:
        loop.create_task(web._run_app(http_server, host=params['bind_addr'], port=params['bind_port']))
        loop.run_until_complete(restart_loop(http_server))
        loop.stop()

    except Exception as e:
        Logger.error('Error on start of the server: {}\n{}'.format(e, traceback.format_exc()))

    return


if __name__ == '__main__':
    main(Config().export_params())


