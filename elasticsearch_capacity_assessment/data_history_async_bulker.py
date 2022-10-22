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
# import random
import time

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from elasticsearch_capacity_assessment.data_history_generator import generate_data_history_each_document

ALL_COUNT = 70 * 10000
PROCESS_COUNT = 32
PER_PROCESS_COUNT = ALL_COUNT / PROCESS_COUNT
# PER_PROCESS_COUNT = 10000 * 1  # no more than 30
# ALL_COUNT = PROCESS_COUNT * PER_PROCESS_COUNT
all_data = [generate_data_history_each_document() for i in range(ALL_COUNT)]
print('all_data generated')


def task(process_number):
    start_number = int(PER_PROCESS_COUNT * process_number)
    end_number = int(PER_PROCESS_COUNT * (process_number + 1))
    per_process_data = all_data[start_number: end_number]
    print(f'process_number: {process_number}, from {start_number} to {end_number}')

    es = AsyncElasticsearch(
        hosts=[
            {'host': 'es-node-1', 'port': 9200, 'scheme': 'http'},
            {'host': 'es-node-2', 'port': 9200, 'scheme': 'http'},
            {'host': 'es-node-3', 'port': 9200, 'scheme': 'http'}
        ],
        basic_auth=('username', 'password')
        # request_timeout=180
    )
    _now = lambda: time.time()

    async def main():
        await async_bulk(
            es,
            per_process_data,
            chunk_size=3200,
            # max_chunk_bytes=15 * 1024 * 1024
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # time.sleep(random.randint(1, 10))
    print('Task finish at：', _now())


if __name__ == '__main__':
    _now = lambda: time.time()
    start = _now()
    print('start')

    running_p = []
    for i in range(PROCESS_COUNT):
        p = multiprocessing.Process(target=task, args=(i,))
        p.start()
        running_p.append(p)

    for p in running_p:
        p.join()

    print('All tasks finish：', _now() - start)
