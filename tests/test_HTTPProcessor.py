import sys
sys.path.append('../src/')

import json
import asyncio
import aiohttp
import pytest

from class_Storage import Storage
from class_HTTPProcessor import HTTPProcessor


class Query(object):
    def __init__(self, init_dict: dict, init_text: str):
        self.match_info = init_dict
        self._text = init_text
        self.body_exists = True

    async def text(self):
        return self._text


#@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.asyncio
async def test_set_get_param():
    """
        Проверяем запись-чтение сразу на 2 объекта
    """
    params = {}
    key, value = 'aaa', 'value_of_aaa'
    storage = Storage(params=params, logger=None, tpe=None)
    http_processor = HTTPProcessor(params=params, logger=None, storage=storage)

    query = Query({'name': key}, value)

    await http_processor.set(query)
    assert storage.get(key) == value
    read_res = await http_processor.read(query)
    assert isinstance(read_res, aiohttp.web_response.Response)
    assert json.loads(read_res.text)['key'] == key
    assert json.loads(read_res.text)['value'] == value