#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Combot 爬取任务
import os
from datetime import datetime

import requests
import time
import schedule

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from spider.src.utils.languageUtil import LanguageUtil
from spider.src.utils.hanlpUtil import HanlpUtil


class UpdateRoomTags:
    def __init__(self, index_name, page_size):
        # 初始化 Elasticsearch 客户端
        es_host_url = os.getenv('ES_HOST_URL')
        es_username = os.getenv('ES_USERNAME')
        es_password = os.getenv('ES_PASSWORD')
        print(es_host_url)
        self.es = Elasticsearch(
            hosts=[es_host_url],  # 替换为你的 Elasticsearch 地址
            http_auth=(es_username, es_password)  # 如果需要身份验证
        )
        self.index_name = index_name
        self.languageUtil = LanguageUtil()
        self.hanlpUtil = HanlpUtil()
        self.page_size = page_size

    def fetch_all_documents(self, scroll="30m"):
        # 初始化滚动查询
        result = self.es.search(
            index=self.index_name,
            scroll=scroll,
            size=self.page_size,  # 每页文档数
            body={
                "query": {
                    "bool": {
                        "must": [
                            # {"match_all": {}}
                            {"exists": {"field": "jhiDesc"}}
                        ],
                        "must_not": [
                            {"exists": {"field": "tags"}}  # 查询没有 tags 字段的文档
                        ]
                    }
                }
            }
        )

        # 获取首次查询结果
        scroll_id = result["_scroll_id"]
        hits = result["hits"]["hits"]

        while hits:
            print(f"fetch_all_documents, hits.size={len(hits)}")
            for doc in hits:
                yield doc  # 返回文档

            # 滚动获取下一批数据
            result = self.es.scroll(scroll_id=scroll_id, scroll=scroll)
            scroll_id = result["_scroll_id"]
            hits = result["hits"]["hits"]

        # 清除 scroll
        self.es.clear_scroll(scroll_id=scroll_id)

    def bulk_update(self):
        index_count = 0
        actions = []
        for doc in self.fetch_all_documents():
            doc_id = doc["_id"]
            source = doc["_source"]

            try:
                desc = ""
                if 'jhiDesc' in source:
                    desc = source['jhiDesc']
                else:
                    print(f"warning bulk_update, doc_id={doc_id}, jhiDesc is null")

                room_desc = f"{source['userName']}. {source['standardName']}. {desc}. "
                source["lang"] = self.languageUtil.detect_language(room_desc)

                tags, pos_tags = self.hanlpUtil.extract_keywords_with_pos(room_desc, source["lang"])
                source["tags"] = " ".join(tags)

            except Exception as error:
                print(f"Error bulk_update, doc_id={doc_id}: {error}")


            # 构造 bulk 动作
            actions.append({
                "_op_type": "update",
                "_index": self.index_name,
                "_id": doc_id,
                "doc": source
            })

            # 每 page_size 条提交一次
            if len(actions) >= self.page_size:
                bulk(self.es, actions)
                actions = []
                index_count += self.page_size
                print(f"bulk success, index_count={index_count}")

        # 提交剩余的动作
        if actions:
            bulk(self.es, actions)



index_name = 'room.v2'
if __name__ == "__main__":
    print(f"Starting UpdateRoomTags task, start_time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    crawler = UpdateRoomTags(index_name, 200)
    crawler.bulk_update()

    print(f"Finished UpdateRoomTags task, end_time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

