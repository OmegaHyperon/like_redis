# -*- coding: utf-8 -*-

""" -------------------------------------------------------
    Like REDIS
    Обработчик HTTP-запросов


------------------------------------------------------- """

import json
import traceback
from singleton_decorator import singleton
from typing import Any, Union
from aiohttp import web


@singleton
class HTTPProcessor(object):
    def __init__(self, params, logger, storage):
        self._params = params
        self._logger = logger

        # It must have read(), set(), remove(), dump()
        self._storage_obj = storage

    def _save_log(self, msg: str, type: str = 'info'):
        """
            Сохранение сообщения в лог
        """

        l_msg = '{}: {}'.format(self.__class__.__name__, msg)

        if self._logger is not None:
            if type.lower() == 'info':
                self._logger.info(l_msg)
            else:
                self._logger.error(l_msg)
        else:
            print(l_msg)

        return

    async def read(self, query: web.Request) -> web.Response:
        """
            Обработчик команды чтения параметра
        """

        key = query.match_info.get('name')
        self._save_log(f'Read: {key}')
        value = self._storage_obj.get(key)
        resp = {'key': key, 'value': value}

        return web.json_response(text=json.dumps(resp))

    async def set(self, query: web.Request) -> web.Response:
        """
            Обработчик команды записи значения параметра
        """

        key = query.match_info.get('name')
        value = None
        if query.body_exists:
            value = await query.text()
        self._save_log(f'Set: {key}={value}')
        self._storage_obj.set(key, value)

        resp = {'result': 'OK', 'msg': None}

        return web.json_response(text=json.dumps(resp))

    async def remove(self, query: web.Request) -> web.Response:
        key = query.match_info.get('name')
        self._save_log(f'Remove: {key}')
        self._storage_obj.remove(key)

        resp = {'result': 'OK', 'msg': None}

        return web.json_response(text=json.dumps(resp))

    async def dump(self, query: web.Request) -> web.Response:
        """
            Обработчик команды выдачи содержимого хранилища
        """

        resp: dict = self._storage_obj.dump()
        resp = {
            "version": self._params['version'],
            "capacity": len(resp),
            "data": resp
        }

        return web.json_response(text=json.dumps(resp, indent=4))

    async def restart(self, query: web.Request) -> web.Response:
        """
            Обработчик команды перезапуска сервиса
        """

        self._save_log('Got RESTART')

        set_config_func = self._params.get('set_param_func', None)
        if set_config_func is not None:
            set_config_func('is_started', False)
        else:
            raise SystemExit

        resp = {'result': 'OK', 'msg': None}

        return web.json_response(text=json.dumps(resp))

