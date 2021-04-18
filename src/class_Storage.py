# -*- coding: utf-8 -*-

""" -------------------------------------------------------
    Like REDIS
    Хранилище значений


------------------------------------------------------- """
import asyncio
import os
import sys
import traceback
from singleton_decorator import singleton
import configparser
import argparse
from typing import Any, Union
import copy
import json


@singleton
class Storage(object):
    def __init__(self, params, logger, tpe):
        self._params = params
        self._logger = logger
        self._tpe = tpe
        self._storage: dict = dict()

        self._statistic = {
            "reads": 0,
            "changes": 0,
        }

    def _save_log(self, msg: str, msg_type: str = 'info'):
        """
            Сохранение сообщения в лог
        """

        l_msg = '{}: {}'.format(self.__class__.__name__, msg)

        if self._logger is not None:
            if msg_type.lower() == 'info':
                self._logger.info(l_msg)
            else:
                self._logger.error(l_msg)
        else:
            print(l_msg)

        return

    def set(self, key: str, value: Any) -> None:
        """
            Установить значение параметра в хранилище
        """
        self._storage[key] = value
        self._statistic["changes"] += 1

        return

    def get(self, key: str) -> Any:
        """
            Получить значение параметра из хранилища
        """

        self._statistic["reads"] += 1
        return self._storage.get(key)

    def remove(self, key: str) -> None:
        """
            Удалить значение параметра из хранилища
        """

        if key in self._storage:
            self._storage.pop(key, None)

        return

    def dump(self) -> dict:
        """
            Отдать все значения хранилища в JSON-формате
        """

        return self._storage

    def snapshot_save(self) -> None:
        """
            Сохранить все значения хранилища из памяти на диск
        """

        try:
            data_copy = copy.deepcopy(self._storage)

            path = os.path.join(self._params['snapshot_dir'], "like_redis.json")
            with open(path, "w") as h_file:
                json.dump(data_copy, h_file)
                self._save_log('Data were saved on disk: {}'.format(path))

        except Exception as e:
            self._save_log('Error in save of snapshot procedure: {}\n{}'.format(e, traceback.format_exc()))

        return

    def snapshot_load(self) -> None:
        """
            Загрузить все значения хранилища с диска в память
        """

        try:
            path = os.path.join(self._params['snapshot_dir'], "like_redis.json")
            with open(path, "r") as h_file:
                self._storage = json.load(h_file)
                self._save_log('Data were load from disk: {}'.format(path))

        except Exception as e:
            self._save_log('Error in load of snapshot procedure: {}\n{}'.format(e, traceback.format_exc()))

        return

    async def loop_snapshot(self):
        """
            Периодическох сохранение хранилища на диск
        """
        if int(self._params['snapshot_period']) > 0:
            while self._params['is_started']:
                i = 0
                while i < int(self._params['snapshot_period']) and self._params['is_started']:
                    await asyncio.sleep(1)
                    i += 1

                await asyncio.get_event_loop().run_in_executor(self._tpe, self.snapshot_save)

        return

    def on_config_change(self, event):
        self._params = event['settings']

        return



