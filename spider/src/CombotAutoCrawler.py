#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Combot 爬取任务
from datetime import datetime

import requests
import time
import schedule
from spider.src.utils.pgHelper import PgHelper
from spider.src.models.room_v2 import (
    INSERT_ROOM_QUERY,
    CHECK_ROOM_EXISTS_QUERY,
    prepare_room_data
)


class CombotAutoCrawler:
    def __init__(self):
        self.db = PgHelper()
        self.default_page_size = 50
        self.batch_size = 50  # Adjust batch size based on performance requirements
        self.rooms_to_insert = []  # List to accumulate room data

    def fetch_data(self, offset=1, page_size=10):
        url = f'https://combot.org/api/chart/all?limit={page_size}&offset={offset}'

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'cookie': '_ym_uid=173028652276094243; _ym_d=1730286522; timezone=Asia/Bangkok; cf_clearance=nPKPdT0Z62e532QIqVoLWAHhArl6tSAbAafflu537FA-1730444683-1.2.1.1-Ahvdb_SGQxgv5whfqnwUAC6UpZwWo0PCzzt0BFJ3R2AWqFebbxGr3RIpf5FJveZLJCX9pPgULleFcZu95cKgGIdkhPVUETNNQcgapb2dX6dbLOrmkpusfCKrzWDM3EoVQ0lafUDKcW9f_m_gTlU2BoOBbj59EWP7047dHB8vVc11Ixo3xvjgwoQ11RfJiqgvgdCIko7ZvTsdvDH5CDaj5URp6cx66etfmBPCmvSghoGyt0bj.JDnl2qczs6ZwmdrLHvzqeu0y3nOLudV0157Z7HnAhXaRENIObfwjoIBne9V0USs.KfzkEAf96EVa8RS6zYUDL3WzQ0KYMlTudZMyROgR_kIudvIjjHlj3UZMJhIN5a5jXIKCZgFzMFNkgmUelpagIHnd7CoZF_.wFn8HA; _ym_isad=2; _ym_visorc=w',
            'priority': 'u=1, i',
            'referer': 'https://combot.org/top/telegram/groups?lng=all&page=1',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for item in data:
                self.process_item(item)
            return len(data) > 0  # Return True if there's more data to fetch
        else:
            print(f"Error: {response.status_code}")
            return False

    def map_item_to_room_v2(self, item):
        return (
            item.get('u'),  # room_id
            f"https://t.me/{item.get('u')}",  # link
            item.get('t'),  # name
            '',  # jhi_desc (description not provided in Combot data)
            item.get('s'),  # member_cnt
            None,  # msg_cnt (not provided in Combot data)
            '',  # type (assuming all are groups, adjust if needed)
            'NEW',  # status (all are NEW)
            None,  # collected_at
            item.get('l'),  # lang
            item.get('a', ''),  # tags (using 'a' field as tags)
            str({  # extra (converting dict to string)
                'popularity': item.get('p'),
                'image': item.get('i'),
                'status_change': item.get('pc'),
                'source': 'combot'
            })
        )

    def process_item(self, item):
        if isinstance(item, dict):
            room_data = self.map_item_to_room_v2(item)
            self.rooms_to_insert.append(room_data)  # Accumulate room data
            if len(self.rooms_to_insert) >= self.batch_size:
                self.process_batch()
        else:
            print(f"Unexpected item type: {type(item)}. Expected dict, got {item}")

    def process_batch(self):
        links = [item[1] for item in self.rooms_to_insert]
        existing_links = self.check_room_exists(links)

        new_items = [item for item in self.rooms_to_insert if item[1] not in existing_links]
        if new_items:
            print(f"Found new rooms: count={len(new_items)}")
            self.insert_rooms_batch(new_items)

        self.rooms_to_insert = []  # Clear the batch after processing

    def check_room_exists(self, links):
        result = self.db.execute_query(CHECK_ROOM_EXISTS_QUERY, (tuple(links),))
        if result:
            print(f"Rooms already exists: count={len(result)}")
            return set(item[0] for item in result)
        else:
            return set()

    def insert_rooms_batch(self, items):
        if items:
            print(f"Inserting {len(items)} rooms in batch")
            self.db.execute_batch_insert(INSERT_ROOM_QUERY, items)

    def crawl_all_pages(self):
        page = 0
        offset = 0
        while True:
            print(f"Fetching page {page}")
            has_more_data = self.fetch_data(offset=offset, page_size=self.default_page_size)
            if not has_more_data:
                break
            page += 1
            offset = page*self.default_page_size
            time.sleep(5)  # Wait for 5 seconds between requests

        # Process any remaining items in the batch
        if self.rooms_to_insert:
            self.process_batch()

    def daily_task(self):
        print("Starting daily Combot crawl task")
        self.crawl_all_pages()
        self.process_batch()  # Insert any remaining rooms
        print("Finished daily Combot crawl task")

    def close(self):
        self.db.close()

def run_daily_task():
    crawler = CombotAutoCrawler()
    crawler.daily_task()
    crawler.close()


if __name__ == "__main__":
    # schedule.every().day.at("02:00").do(run_daily_task)  # Run daily at 2 AM

    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)  # Check every minute

    run_daily_task()
