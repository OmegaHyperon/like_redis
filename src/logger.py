# -*- coding: utf-8 -*-

""" -------------------------------------------------------
    Like REDIS
    Утилита для логгирования


------------------------------------------------------- """
import datetime
import os
import sys
import traceback
from typing import Any, Union, Type
import logging


class Logger(object):
    logger = None

    def __init__(self, params):
        self._params = params

        Logger.logger = logging.getLogger(self._params['process_name'])
        Logger.logger.setLevel(logging.INFO)
        Logger.logger.addHandler(self._local_handler())
        if self._params['log_console']:
            Logger.logger.addHandler(self._console_handler())

    @classmethod
    def info(cls, msg):
        if Logger.logger is not None:
            Logger.logger.info(msg)
        else:
            print(msg)

    @classmethod
    def error(cls, msg):
        if Logger.logger is not None:
            Logger.logger.error(msg)
        else:
            print(msg)

    def _get_formatter(self) -> logging.Formatter:
        """
            Формат вывода лога
        """
        points = ['%(asctime)s', '%(message)s']
        separator = ' '
        log_format = separator.join(points)
        dt_format = r'%Y-%m-%d %H:%M:%S'

        return logging.Formatter(log_format, dt_format)

    def _console_handler(self) -> logging.StreamHandler:
        """
            Отображение лога в консоль
        """

        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(self._get_formatter())

        return h

    def _local_handler(self) -> logging.FileHandler:
        """
            Сохранение лога в локальный файл
        """

        dt_str: str = str(datetime.datetime.today().date())
        file_name: str = ''.join([self._params['process_name'], '_', dt_str, '.log'])
        full_path: str = os.path.join(self._params['log_dir'], file_name)

        h = logging.FileHandler(full_path)
        h.setFormatter(self._get_formatter())

        return h
