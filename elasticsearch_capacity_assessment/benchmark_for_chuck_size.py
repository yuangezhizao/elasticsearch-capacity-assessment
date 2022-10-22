#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2022/5/11 16:48:17
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2022 yuangezhizao <root@yuangezhizao.cn>
"""

import asyncio
import time

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from elasticsearch_capacity_assessment.data_history_generator import generate_data_history_each_document

ALL_COUNT = 40 * 10000

all_data = [generate_data_history_each_document() for i in range(ALL_COUNT)]
print('all_data generated')


def task(chunk_size: int):
    es = AsyncElasticsearch(
        hosts=[
            {'host': 'es-node-1', 'port': 9200, 'scheme': 'http'},
            {'host': 'es-node-2', 'port': 9200, 'scheme': 'http'},
            {'host': 'es-node-3', 'port': 9200, 'scheme': 'http'}
        ],
        basic_auth=('username', 'password'),
        request_timeout=180
    )
    _now = lambda: time.time()

    async def main():
        await async_bulk(
            es,
            all_data,
            chunk_size=chunk_size,
            max_chunk_bytes=15 * 1024 * 1024
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    print('Task finish at：', _now())


if __name__ == '__main__':
    _now = lambda: time.time()
    start = _now()
    print('start')

    task(chunk_size=3200)

    print('execute_cost_time：', _now() - start)

# https://www.elastic.co/guide/en/elasticsearch/reference/8.1/tune-for-indexing-speed.html#_use_bulk_requests
# 1 shards & 0 replicas
# ALL_COUNT chunk_size execute_cost_time indexing_rate(from_kibana)
# 100_000 100 27.79s
# 100_000 200 22.79s
# 100_000 400 20.08s
# 100_000 800 18.77s
# 100_000 1600 18.07s
# 100_000 3200 17.72s *
# 100_000 6400 16.77s
# 100_000 12800 16.84s
# 100_000 25600 16.93s
# 100_000 51200 16.45s
# 100_000 102400 16.74s

# 200_000 100 53.57s 3.6k/s
# 200_000 200 47.31s 4.2k/s
# 200_000 400 39.49s 5.1k/s
# 200_000 800 37.21s 5.3k/s
# 200_000 1600 36.07s 5.6k/s
# 200_000 3200 34.63s 6.0k/s *
# 200_000 6400 33.87s 6.1k/s
# 200_000 12800 34.21s 5.8k/s
# 200_000 25600 33.95s 6.4k/s
# 200_000 51200 33.39s 5.9k/s
# 200_000 102400 33.51s 5.8k/s

# 400_000 100 109.62s 3.6k/s
# 400_000 200 90.71s 4.3k/s
# 400_000 400 78.59s 5.1k/s
# 400_000 800 73.46s 5.2k/s
# 400_000 1600 73.12s 5.6k/s
# 400_000 3200 70.13s 5.6k/s *
# 400_000 6400 67.43s 5.7k/s
# 400_000 12800 67.14s 5.7k/s
# 400_000 25600 67.41s 5.7k/s
# 400_000 51200 68.53s 5.8k/s
# 400_000 102400 68.89s 5.5k/s

# 2 shards & 0 replicas
# 400_000 100 89.07s 4.5k/s
# 400_000 200 71.81s 5.6k/s
# 400_000 400 57.58s 6.9k/s
# 400_000 800 52.36s 7.5k/s
# 400_000 1600 50.01s 8.0k/s
# 400_000 3200 46.44s 8.5k/s *
# 400_000 6400 45.17s 8.6k/s
# 400_000 12800 44.15s 8.7k/s
# 400_000 25600 43.74s 8.6k/s
# 400_000 51200 44.48s 8.5k/s

# 3 shards & 0 replicas
# 400_000 100 78.31s 5.1k/s
# 400_000 200 63.01s 6.2k/s
# 400_000 400 50.44s 7.9k/s
# 400_000 800 45.17s 8.7k/s
# 400_000 1600 42.5s 9.5k/s
# 400_000 3200 40.0s 9.2k/s *
# 400_000 6400 37.75s 9.8k/s
# 400_000 12800 37.35s 9.7k/s
# 400_000 25600 37.12s 9.2k/s
# 400_000 51200 37.45s 9.4k/s
