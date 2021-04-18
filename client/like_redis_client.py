# -*- coding: utf-8 -*-

""" -------------------------------------------------------
    Client for Like-REDIS server

def _handle_request(self, method, request, requested_url):
        # Handle proxy requests.
        requested_url = requested_url or "/"
        headers = request.headers.copy()
        headers["Host"] = request.host
        headers["X-Real-Ip"] = request.remote
        headers["X-Forwarded-For"] = request.remote
        headers["X-Forwarded-Proto"] = request.scheme
        post_data = await request.read()
        async with aiohttp.request(
            method,
            self.proxy_url + requested_url,
            params=request.query,
            data=post_data,
            headers=headers,
        ) as resp:
            content = await resp.read()
            headers = resp.headers.copy()
            return aiohttp.web.Response(
                body=content, status=resp.status, headers=headers
            ) 


------------------------------------------------------- """

import json
import traceback
from singleton_decorator import singleton
from typing import Any, Union, Tuple
from aiohttp import web
from abc import ABCMeta, abstractmethod
import aiohttp


class SimpleLogger(object):
    """
        Класс для логгирования действий клиента
        Демонстрация интерфейса методов
        Предполагается использование logging
    """
    @abstractmethod
    def info(self, msg: str):
        raise NotImplementedError()

    @abstractmethod
    def error(self, msg: str):
        raise NotImplementedError()


class LikeRedisClient(object):
    def __init__(self, host: str, port: int, timeout: int, logger: SimpleLogger):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._logger = logger
        self._url_mask = 'http://{}:{}/{}/{}'

    def _save_log(self, msg: str, msg_type: str = 'info') -> None:
        """
            Сохраняем сообщение в лог при наличии логгера
        """

        if self._logger is not None:
            if msg_type == 'error':
                self._logger.error(msg)
            else:
                self._logger.info(msg)

        return

    async def _request(self, url: str, method: str, data: Any) -> Tuple:
        """
            Реализация команды set для сервера like_redis
            :result: (status: bool, data: dict)
        """

        res_status: bool = False
        res_data: Any = None

        try:
            async with aiohttp.ClientSession() as session:
                timeout = aiohttp.ClientTimeout(total=self._timeout)

                if method.upper() == 'GET':
                    async with session.get(url, timeout=timeout) as resp:
                        status = resp.status
                        data = await resp.text()

                elif method.upper() == 'POST':
                    async with session.post(url, data=data, timeout=timeout) as resp:
                        status = resp.status
                        data = await resp.text()

                elif method.upper() == 'DELETE':
                    async with session.delete(url, timeout=timeout) as resp:
                        status = resp.status
                        data = await resp.text()

                else:
                    self._save_log(f'Unknown method: {method}')

            if 200 <= status <= 299:
                res_status = True
                res_data = json.loads(data)
            else:
                res_status = False
                res_data = None

        except Exception as e:
            self._save_log('There is an error in LikeRedisClient, url={}, method={}: {}\n{}'.format(
                url, method, e, traceback.format_exc()
            ))

        return res_status, res_data

    async def read(self, key: str) -> Any:
        """
            Реализация команды read
            :result: (status: bool, value: Any)
        """

        resp_value: Any = None

        url: str = self._url_mask.format(self._host, self._port, 'key', key)
        resp: Tuple = await self._request(url=url, method='GET', data=None)
        if resp[0] and resp[1] is not None:
            resp_value = resp[1].get('value')

        return resp[0], resp_value

    async def set(self, key: str, value: str) -> bool:
        """
            Реализация команды set для сервера like_redis
            :result: (status: bool, data: dict)
        """

        url: str = self._url_mask.format(self._host, self._port, 'key', key)
        resp: Tuple = await self._request(url=url, method='POST', data=value)

        return resp

    async def remove(self, key: str) -> bool:
        """
            Реализация команды remove для сервера like_redis
            :result: (status: bool, data: dict)
        """

        url: str = self._url_mask.format(self._host, self._port, 'key', key)
        resp: Tuple = await self._request(url=url, method='DELETE', data=None)

        return resp


if __name__ == '__main__':
    print('Stop!')
