# -*- coding: utf-8 -*-

""" -------------------------------------------------------
    Example of using of client for like-Redis server


------------------------------------------------------- """

import sys
sys.path.append('../client/')
import asyncio

from like_redis_client import LikeRedisClient


async def writing(lrc: LikeRedisClient, count: int = 10):
    print('Writing:')
    for i in range(count):
        print(f'key{i}', await lrc.set(f'key{i}', f'value{i}'))


async def reading(lrc: LikeRedisClient, count: int = 10):
    print('Reading: ')
    for i in range(count+5):
        print(f'key{i}', await lrc.read(f'key{i}'))


async def removing(lrc: LikeRedisClient, count: int = 10):
    print('Removing: ')
    for i in range(count-5):
        print(f'key{i}', await lrc.remove(f'key{i}'))


lrc = LikeRedisClient(host='127.0.0.1', port=8900, timeout=100, logger=None)
count = 10

loop = asyncio.get_event_loop()

writing_task = loop.create_task(writing(lrc=lrc, count=count))
loop.run_until_complete(writing_task)

reading_task = loop.create_task(reading(lrc=lrc, count=count))
loop.run_until_complete(reading_task)

removing_task = loop.create_task(removing(lrc=lrc, count=count))
loop.run_until_complete(removing_task)

loop.close()