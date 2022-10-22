#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2022/5/11 16:48:17
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2022 yuangezhizao <root@yuangezhizao.cn>
"""

import asyncio
import multiprocessing
import random
import time

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from elasticsearch_capacity_assessment.data_history_generator import generate_data_history_each_document


def task():
    es = AsyncElasticsearch(
        hosts=[
            {'host': 'es-node-1', 'port': 9200, 'scheme': 'http'},
            {'host': 'es-node-2', 'port': 9200, 'scheme': 'http'},
            {'host': 'es-node-3', 'port': 9200, 'scheme': 'http'}
        ],
        basic_auth=('username', 'password')
    )
    _now = lambda: time.time()

    async def gendata():
        numbers = 10000 * 200
        for i in range(numbers):
            yield generate_data_history_each_document()

    async def main():
        await async_bulk(
            es,
            gendata(),
            chunk_size=3200,
            # max_chunk_bytes=15 * 1024 * 1024,
            request_timeout=120
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    time.sleep(random.randint(1, 10))
    print('task finish at：', _now())


if __name__ == '__main__':
    _now = lambda: time.time()
    start = _now()

    running_p = []
    for i in range(32):
        p = multiprocessing.Process(target=task)
        p.start()
        running_p.append(p)

    for p in running_p:
        p.join()

    print('All tasks finish：', _now())

# System CPU 32 Core & Each Process: 50 * 10000

# Refer: <rm>

# "Total Shards 44,946.6 /s, Primary Shards 44,946.6 /s" based on "1 Primary Shard, 0 Replica Shard" & "16 Process"

# "Total Shards 54,747.3 /s, Primary Shards 54,747.3 /s" based on "1 Primary Shard, 0 Replica Shard" & "32 Process"

# "Total Shards 54,219.9 /s, Primary Shards 26,891.9 /s" based on "1 Primary Shard, 1 Replica Shard" & "16 Process"

# "Total Shards 67,971.7 /s, Primary Shards 34,145.6 /s" based on "1 Primary Shard, 1 Replica Shard" & "32 Process"
