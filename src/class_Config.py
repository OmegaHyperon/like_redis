# -*- coding: utf-8 -*-

""" -------------------------------------------------------
    Like REDIS
    Работа с конфигурацией проекта

    Пример файла:
[LOG]
dir = ./logs/
console = 1

[SERVER]
bind_addr = 127.0.0.1
bind_port = 8900

[SNAPSHOT]
dir = ./dump/
period = 600

------------------------------------------------------- """
import datetime
import os
import traceback
from singleton_decorator import singleton
import configparser
import argparse
from typing import Any, Union


@singleton
class Config(object):
    def __init__(self):
        self._settings: dict = dict()
        self._subscribers: list = list()                        # For events of changes of the storage
        self._sys_env_var: str = 'LIKE_REDIS'
        self._ext_data_path: str = './logs/like_redis.ini'      # Path to the ini-file
        self._arg: Union[argparse.ArgumentParser, None] = None

        # Magic parameters
        self.set('version', '1.0.1')
        self.set('start_dt', datetime.datetime.now())
        self.set('set_param_func', self.set)
        self.set('is_started', True)
        self.set('process_name', 'like_redis')

        self._process_cli_args()
        self._load_ext_data()

    @property
    def is_started(self):
        """
            Only for manager
        """
        return self._settings['is_started']

    def set(self, key: str, value: Any):
        self._settings[key] = value
        self.fire_on_config_change(key)

        return

    def get(self, key: str):
        return self._settings.get(key)

    def export_params(self) -> dict:
        """
            Вернуть все значения конфига
        """

        return self._settings

    def add_subscriber(self, subscriber: object) -> None:
        """
            Добавить подписчика на события изменения параметров
        """

        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

        return

    def remove_subscriber(self, subscriber: object) -> None:
        """
            Удалить подписчика на события изменения параметров
        """

        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

        return

    def fire_on_config_change(self, changed_key: str):
        """
            Сообщаем подписчикам об изменении конфига
        """

        event = {
            "settings": self._settings,
            "change": changed_key
        }

        for item in self._subscribers:
            if hasattr(item, 'on_config_change'):
                try:
                    item.on_config_change(event)
                except Exception as e:
                    print('Error in fire_on_config_change: {}\n{}'.format(e, traceback.format_exc()))

        return

    def _process_cli_args(self) -> None:
        """
            Обработка консольных команд
        """

        arg = argparse.ArgumentParser()
        arg.add_argument('-c', '--conf', dest='conf', nargs='?', default='./like_redis.ini', help='Path to the INI-file')
        self._arg = arg.parse_args()
        self._ext_data_path = self._arg.conf

        return

    def _load_ext_data(self) -> None:
        """
            Загружаем данные из ini-файла
        """

        if self._sys_env_var in os.environ:
            self._ext_data_path = os.environ[self._sys_env_var]

        if not os.path.exists(self._ext_data_path):
            print('INI-file {} is not found. Stop the process.'.format(self._ext_data_path))
            raise SystemExit
        else:
            print('INI-file: {}'.format(self._ext_data_path))

        try:
            cnf = configparser.ConfigParser()
            cnf.read(self._ext_data_path)

            self._settings['log_dir']           = str(cnf.get("LOG", "dir"))                if cnf.has_option("LOG", "dir")             else './logs/like_redis.log'
            self._settings['log_console']       = bool(cnf.get("LOG", "console") == '1')    if cnf.has_option("LOG", "console")         else True

            self._settings['bind_addr']         = str(cnf.get("SERVER", "bind_addr"))       if cnf.has_option("SERVER", "bind_addr")    else '127.0.0.1'
            self._settings['bind_port']         = int(cnf.get("SERVER", "bind_port"))       if cnf.has_option("SERVER", "bind_port")    else 8900

            self._settings['snapshot_dir']      = str(cnf.get("SNAPSHOT", "dir"))           if cnf.has_option("SNAPSHOT", "dir")        else './dump/'
            self._settings['snapshot_period']   = int(cnf.get("SNAPSHOT", "period"))        if cnf.has_option("SNAPSHOT", "period")     else 600

        except Exception as e:
            print('Error in INI-file: {}\n{}'.format(e, traceback.format_exc()))
            raise SystemExit

        return

