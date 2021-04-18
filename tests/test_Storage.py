import os
import sys
sys.path.append('../src/')

import json
import asyncio
import aiohttp
import pytest

from class_Storage import Storage


def test_snapshot():
    """
        Проверяем запись хранилища на диск
    """
    params = {"snapshot_dir": "../dump/"}
    key, value = 'aaa', 'value_of_aaa'
    storage = Storage(params=params, logger=None, tpe=None)

    storage.set(key=key, value=value)
    storage.snapshot()

    f_name = '../dump/like_redis.json'
    f_exists: bool = os.path.exists(f_name)
    f_size = os.stat(f_name).st_size

    assert f_exists is True
    assert f_size == 23
