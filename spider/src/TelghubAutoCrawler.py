#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Telghub 爬取任务
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


class TelghubAutoCrawler:
    pagetype = 'new'

    def __init__(self, pagetype):
        self.db = PgHelper()
        self.batch_size = 100  # Define a batch size
        self.items_batch = []  # Initialize a list to store items
        self.pagetype = pagetype

    def fetch_telghub_data(self, page=1, list_rows=10, language='zh'):
        try:
            url = f'https://www.tghub.club/api/index?pagetype={self.pagetype}&page={page}&list_rows={list_rows}&language={language}'

            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'cookie': 'i18n_redirected=en',
                'priority': 'u=1, i',
                'referer': 'https://www.tghub.club/en/new-list/1',
                'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'token': 'undefined',
                'url': '/list_page',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
            }

            response = requests.get(url, headers=headers)
            # print(response.status_code)
            if response.status_code == 200 and response.json()['code'] == 200:
                data = response.json().get('data', [])
                # print(f'data.len={len(data)}')
                # print(f'data={data}')
                if 'data' in data:
                    data = data['data']
                    if isinstance(data, list):
                        for item in data:
                            self.process_item(item)
                    else:
                        print(f"Unexpected data type: {type(data)}. Expected list, got {data}")
                return len(data) > 0  # Return True if there's more data to fetch
            else:
                print(f"Error: {response.status_code}")
                return False
        except Exception as error:
            print(f"Error fetch_telghub_data, pagetype={self.pagetype}, page={page}: {error}")
            return False



    def process_item(self, item):
        if isinstance(item, dict):
            self.items_batch.append(item)
            if len(self.items_batch) >= self.batch_size:
                self.process_batch()
        else:
            print(f"Unexpected item type: {type(item)}. Expected dict, got {item}")

    def process_batch(self):
        links = [item.get('link') for item in self.items_batch]
        existing_links = self.check_rooms_exist(links)

        new_items = [item for item in self.items_batch if item.get('link') not in existing_links]
        if new_items:
            print(f"Found new rooms: count={len(new_items)}")
            self.insert_rooms(new_items)

        self.items_batch = []  # Clear the batch after processing

    def check_rooms_exist(self, links):
        result = self.db.execute_query(CHECK_ROOM_EXISTS_QUERY, (tuple(links),))
        if result:
            print(f"Rooms already exists: count={len(result)}")
            return set(item[0] for item in result)
        else:
            return set()

    def insert_rooms(self, items):
        data = [prepare_room_data(item) for item in items]
        self.db.execute_batch_insert(INSERT_ROOM_QUERY, data)


    def crawl_all_pages(self):
        page = 2237
        while True:
            print(f"Fetching {self.pagetype} page {page}")
            has_more_data = self.fetch_telghub_data(page=page, list_rows=DEFAULT_LIST_ROWS)
            if not has_more_data:
                break
            page += 1
            time.sleep(5)  # Wait for 5 seconds between requests

        # Process any remaining items in the batch
        if self.items_batch:
            self.process_batch()

    def daily_task(self):
        print(f"Starting daily Telghub crawl task, start_time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.crawl_all_pages()
        print(f"Finished daily Telghub crawl task, end_time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def close(self):
        self.db.close()

def run_daily_task():
    for pagetype in PAGETYPE_LIST:
        crawler = TelghubAutoCrawler(pagetype)
        crawler.daily_task()
        crawler.close()



DEFAULT_LIST_ROWS = 100
# PAGETYPE_LIST = ['new','member_top']
PAGETYPE_LIST = ['member_top']
if __name__ == "__main__":
    # schedule.every().day.at("02:00").do(run_daily_task)  # Run daily at 2 AM

    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)  # Check every minute

    run_daily_task()
