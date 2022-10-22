#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2022/5/11 15:25:05
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2022 yuangezhizao <root@yuangezhizao.cn>
"""

import datetime
import random

COLLECTOR_IP = '1.1.1.1'


def generate_random_ip():
    """ 0.0.0.0 ~ 255.255.255.255

    :return:
    """
    return f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'


def generate_random_prefix_mask():
    """ 1 ~ 32

    :return:
    """
    return random.randint(1, 32)


def combine_prefix_str(random_prefix_ip: str, random_prefix_mask: int):
    """ 0.0.0.0/1 ~ 255.255.255.255/32

    :param random_prefix_ip:
    :param random_prefix_mask:
    :return:
    """
    return f'{random_prefix_ip}/{random_prefix_mask}'


def generate_random_rd():
    """ 0:0 ~ 65535:65535

    :return:
    """
    return f'{random.randint(0, 65535)}:{random.randint(0, 65535)}'


def combine_rd_prefix(random_rd, random_prefix_str):
    """ 0:0_0.0.0.0/1 ~ 65535:65535_255.255.255.255/32

    :param random_rd:
    :param random_prefix_str:
    :return:
    """
    return f'{random_rd}_{random_prefix_str}'


def generate_random_attr_2():
    """ each 0 ~ 65535 for count 1 ~ 5

    :return:
    """
    return [str(random.randint(0, 65535)) for _ in range(random.randint(1, 5))]


def generate_data_history_each_document():
    """

    :return:
    """
    random_prefix_ip = generate_random_ip()
    random_prefix_mask = generate_random_prefix_mask()
    random_prefix_str = combine_prefix_str(random_prefix_ip=random_prefix_ip, random_prefix_mask=random_prefix_mask)

    random_rd = generate_random_rd()
    random_rd_prefix = combine_rd_prefix(random_rd=random_rd, random_prefix_str=random_prefix_str)

    random_nexthop = generate_random_ip()

    random_attr_as_number_list = generate_random_attr_2()

    date = datetime.datetime.now().isoformat()

    _each_document = {
        'prefix': {
            'mask': random_prefix_mask,
            'str': random_prefix_str,
            'act': 2
        },
        'rd': random_rd,
        'rd_prefix': random_rd_prefix,
        'label': [
            25
        ],
        'upc': 9,
        'nexthop': {
            'rd': '0:0',
            'str': random_nexthop
        },
        'flag_L': 'pre',
        'client_ip': '2.2.2.2',
        'peer_ip': '3.3.3.3',
        'collector_ip': COLLECTOR_IP,
        'collector_port': '50000',
        'upt': 1652088624.1696358,
        'attr': {
            '1': 0,
            '2': {
                'len': len(random_attr_as_number_list),
                'str': ' '.join(random_attr_as_number_list),
                'ori': random_attr_as_number_list[0],
                'dir': random_attr_as_number_list[-1],
                '2': random_attr_as_number_list
            },
            '5': 100,
            '16': {
                'info': {
                    'route-target': '2:2',
                    'color': '101'
                },
                '16': [
                    'route-target:2:2',
                    'color:101'
                ]
            },
            '8': {
                'str': '',
                '8': None
            }
        },
        'date': date
    }
    return {
        '_index': 'data_2.2.2.2_3.3.3.3_history',
        'doc': _each_document
    }


if __name__ == '__main__':
    import json

    each_document = generate_data_history_each_document()
    print(len(str(each_document)))
    print(json.dumps(each_document))
