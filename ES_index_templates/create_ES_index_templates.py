#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2022/5/18 10:33:18
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2022 yuangezhizao <root@yuangezhizao.cn>
"""

from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts=[
        {'host': 'es-node-1', 'port': 9200, 'scheme': 'http'},
        {'host': 'es-node-2', 'port': 9200, 'scheme': 'http'},
        {'host': 'es-node-3', 'port': 9200, 'scheme': 'http'}
    ],
    basic_auth=('username', 'password')
)


def delete_index_template():
    res_del = es.indices.delete_index_template(
        name='data-history'
    )
    if res_del.get('acknowledged'):
        print('es delete_index_template successful')


def create_index_template():
    res_put = es.indices.put_index_template(
        name='data-history',
        create=True,
        index_patterns=[
            "data_*_history"
        ],
        template={
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 0,
                "refresh_interval": "60s",
                "index.translog.durability": "async",
                "index.translog.sync_interval": "60s",
                "index.translog.flush_threshold_size": "1024mb",
                "index.max_result_window": 2147483647,
                "index.sort": {
                    "field": [
                        "upt",
                        "rd_prefix",
                        "nexthop.str",
                        "attr.2.str"
                    ],
                    "order": [
                        "desc",
                        "desc",
                        "desc",
                        "desc"
                    ]
                }
            },
            "mappings": {
                "dynamic": "false",
                "properties": {
                    "rd": {
                        "type": "keyword"
                    },
                    "prefix": {
                        "properties": {
                            "mask": {
                                "type": "integer"
                            },
                            "str": {
                                "type": "keyword"
                            },
                            "act": {
                                "type": "integer"
                            }
                        }
                    },
                    "rd_prefix": {
                        "type": "keyword"
                    },
                    "nexthop": {
                        "properties": {
                            "rd": {
                                "type": "keyword"
                            },
                            "str": {
                                "type": "keyword"
                            }
                        }
                    },
                    "label": {
                        "type": "long"
                    },
                    "client_ip": {
                        "type": "keyword"
                    },
                    "peer_ip": {
                        "type": "keyword"
                    },
                    "upt": {
                        "type": "double"
                    },
                    "upc": {
                        "type": "long"
                    },
                    "date": {
                        "type": "date",
                        "format": "basic_date_time||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||epoch_millis"
                    },
                    "attr": {
                        "properties": {
                            "1": {
                                "type": "integer"
                            },
                            "2": {
                                "properties": {
                                    "len": {
                                        "type": "integer"
                                    },
                                    "str": {
                                        "type": "keyword"
                                    },
                                    "ori": {
                                        "type": "keyword"
                                    },
                                    "dir": {
                                        "type": "keyword"
                                    },
                                    "2": {
                                        "type": "long"
                                    }
                                }
                            },
                            "5": {
                                "type": "integer"
                            },
                            "8": {
                                "properties": {
                                    "str": {
                                        "type": "keyword"
                                    },
                                    "8": {
                                        "type": "keyword"
                                    }
                                }
                            },
                            "9": {
                                "type": "keyword"
                            },
                            "10": {
                                "type": "keyword"
                            },
                            "16": {
                                "properties": {
                                    "info": {
                                        "properties": {
                                            "route-target": {
                                                "type": "keyword"
                                            },
                                            "color": {
                                                "type": "long"
                                            }
                                        }
                                    },
                                    "16": {
                                        "type": "keyword"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    )
    if res_put.get('acknowledged'):
        print('es put_index_template successful')


if __name__ == '__main__':
    # 1. Delete old index_template
    # delete_index_template()

    # 2. Create new index_template
    create_index_template()
