#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Tgstat 爬取任务
import time
from datetime import datetime

import requests
import schedule
from bs4 import BeautifulSoup
from spider.src.models.room_v2 import (
    INSERT_ROOM_QUERY,
    CHECK_ROOM_EXISTS_QUERY,
    prepare_room_data
)
from spider.src.utils.pgHelper import PgHelper
from spider.src.utils import Utils


class TgstatAutoCrawler:


    def __init__(self):
        self.db = PgHelper()
        self.batch_size = 100  # Define a batch size
        self.items_batch = []  # Initialize a list to store items

    def fetch_telegram_data(self, referer, page):
        try:
            url = referer
            offset = page * 30

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': '_ym_uid=1730286410476853704; _ym_d=1730286410; b-user-id=f4a28c25-9bdd-50e3-9c67-af51d3258a2a; _gid=GA1.2.1254556552.1736513221; _ym_isad=2; tgstat_sirk=9b0j1f8obc4r7khck48e9l61f8; tgstat_idrk=ef6b8955a5dec020b7ad38248cf87bd8d201dcfcd111f0fb26c7e1a48fde6388a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22tgstat_idrk%22%3Bi%3A1%3Bs%3A52%3A%22%5B9040599%2C%22DM7uR-OrAG5QpG3L5rEMS5eFjfDja4Gi%22%2C2592000%5D%22%3B%7D; _tgstat_csrk=6648b0a894ed3415bae56aebabbf32599407a9d8ac5b1b7c8a95ff3226bc42d7a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22_tgstat_csrk%22%3Bi%3A1%3Bs%3A32%3A%226g0PEZk_RPWPGST-5ItRwxE1I8WoJ0kF%22%3B%7D; tgstat_settings=e97919bde43a9dd86b8fffa4a9ddecf56bfd045798153ef7c2f3b1e137ef8bfda%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22tgstat_settings%22%3Bi%3A1%3Bs%3A19%3A%22%7B%22fp%22%3A%22_H5rhNJEcb%22%7D%22%3B%7D; _ga=GA1.1.1136855142.1730286408; _ga_ZEKJ7V8PH3=GS1.1.1736513221.15.1.1736513725.0.0.0',
                'Origin': 'https://tgstat.com',
                'Referer': 'https://tgstat.com/channels/search',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            data = {
                '_tgstat_csrk': 'cspIwgl2njETtx8ls5vyMm8AfInhIGjwEEzf7KDbf_1ErXiSTCz1bkHnSHX0yKYfWkkI25ZYLcFZdIiD6usUuw==',
                'view': 'list',
                'sort': 'participants',
                'q': '',
                'inAbout': '0',
                'categories': '',
                'countries': '',
                'languages': '',
                'languages[]': '12',
                'channelType': '',
                'age': '0-120',
                'err': '0-100',
                'er': '0',
                'male': '0',
                'female': '0',
                'participantsCountFrom': '',
                'participantsCountTo': '',
                'avgReachFrom': '',
                'avgReachTo': '',
                'avgReach24From': '',
                'avgReach24To': '',
                'ciFrom': '',
                'ciTo': '',
                'isVerified': '0',
                'isRknVerified': '0',
                'isStoriesAvailable': '0',
                'noRedLabel': '1',
                'noScam': '1',
                'noDead': '1',
                'page': page,
                'offset': offset,
            }

            response = requests.post(url, headers=headers, data=data)
            # print(response.status_code)
            if response.status_code == 200:
                responseData = response.json()
                # print(responseData)
                html_str = responseData.get('html', '')
                nextPage = responseData['nextPage'] if 'nextPage' in responseData else None
                # print(f'nextPage = {nextPage}')

                soup = BeautifulSoup(html_str, "html.parser")
                cards = soup.find_all("div", class_="card")
                # Extract data
                for card in cards:
                    # Extract fields based on table structure
                    data_src = card.find('a', class_='js-btn-favorite')['data-src']
                    print(data_src)
                    if '@' in data_src:
                        room_id = data_src.split('@')[1].split('/')[0]
                    else:
                        # 处理没有 @ 符号的情况
                        room_id = data_src.split('/')[3]
                    print(room_id)
                    link = f"https://t.me/{room_id}" if room_id else None  # Remove '@' from username

                    name = card.find('div', class_='text-truncate font-16 text-dark mt-n1').text.strip()
                    jhi_desc = card.find('span', class_='border rounded bg-light px-1').text.strip()
                    member_cnt = card.find('div', class_='text-truncate font-14 text-dark mt-n1').text.strip().split()[0].replace(',', '')

                    # Default values
                    status = "NEW"
                    lang = None

                    # Store the room data
                    item = {
                        "room_id": room_id,
                        "link": link,
                        "name": name,
                        "jhi_desc": jhi_desc,
                        "member_cnt": member_cnt,
                        "msg_cnt": None,  # Not available in current HTML
                        "type": None,  # Not available in current HTML
                        "status": status,
                        "collected_at": None,
                        "lang": lang,
                        "tags": None,
                        "extra": None,  # Not available in current HTML
                        "icon": None
                    }
                    self.process_item(item)

                return nextPage != None and nextPage > page
            else:
                print(f"Error: {response.status_code}")
                return False
        except Exception as error:
            print(f"Error fetch_telegram_data, page={page}: {error}")
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
        data = self.items_to_sequence(items)
        self.db.execute_batch_insert(INSERT_ROOM_QUERY, data)

    def items_to_sequence(self, items):
        sequence_list = [
            (
                item["room_id"],
                item["link"],
                item["name"],
                item["jhi_desc"],
                item["member_cnt"],
                item["msg_cnt"],
                item["type"],
                item["status"],
                item["collected_at"],
                item["lang"],
                item["tags"],
                item["extra"]
            )
            for item in items
        ]
        return sequence_list


    def crawl_all_pages(self, url):
        config = Utils.getConfig()
        print(config)
        page = config['tgstat']['page']
        while True:
            print(f"Fetching url {url}, page {page}")
            has_more_data = self.fetch_telegram_data(referer=url, page=page)
            if not has_more_data:
                break
            page += 1
            time.sleep(5)  # Wait for 5 seconds between requests

        # Process any remaining items in the batch
        if self.items_batch:
            self.process_batch()



    def daily_task(self):
        print(f"Starting daily tgstat crawl task, start_time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        url = 'https://tgstat.com/channels/search'
        self.crawl_all_pages(url)

        print(f"Finished daily tgstat crawl task, end_time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def close(self):
        self.db.close()

def run_daily_task():
    crawler = TgstatAutoCrawler()
    crawler.daily_task()
    crawler.close()



DEFAULT_LIST_ROWS = 100
if __name__ == "__main__":
    # schedule.every().day.at("02:00").do(run_daily_task)  # Run daily at 2 AM
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)  # Check every minute

    run_daily_task()