#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Telghub 爬取任务
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from spider.src.models.room_v2 import (
    INSERT_ROOM_QUERY,
    CHECK_ROOM_EXISTS_QUERY,
    prepare_room_data
)
from spider.src.utils.pgHelper import PgHelper


class TgramAutoCrawler:


    def __init__(self):
        self.db = PgHelper()
        self.batch_size = 100  # Define a batch size
        self.items_batch = []  # Initialize a list to store items

    def fetch_telegram_data(self, referer, page):
        try:
            url = f'{referer}&page={page}'

            headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "cookie": "csrftoken=yofqzuXJyKkT6I6GkOixdFKYwxIn2SzyS09re22EyuwoMipAYKluzYoUboJ2nVPn; _ym_uid=1730285703282764258; _ym_d=1730285703; b-user-id=0bb15b94-8319-3c20-2f22-62b94b8af0f0; _ym_isad=2; filter_lang=\"\"; _ym_visorc=w",
                "priority": "u=1, i",
                "referer": referer,
                "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            }

            response = requests.get(url, headers=headers)
            # print(response.status_code)
            if response.status_code == 200:
                html_str = response.json().get('groupsHtml', '')
                nextPage = response.json().get('nextPage', None)
                # print(f'nextPage = {nextPage}')

                soup = BeautifulSoup(html_str, "html.parser")
                card_blocks = soup.find_all("div", class_="card-block")
                # Extract data
                for block in card_blocks:
                    # Extract fields based on table structure
                    room_id = block.find("span", class_="text-success").text.strip() if block.find("span", class_="text-success") else None
                    link = f"https://t.me/{room_id[1:]}" if room_id else None  # Remove '@' from username

                    name = block.find("h3").text.strip()
                    jhi_desc = block.find("div", style=lambda x: x and "height: 65px" in x).text.strip()
                    member_cnt = int(block.find("span", class_="fa-user").parent.text.strip().replace(',', '')) if block.find("span", class_="fa-user") else None
                    lang = block.find("span", class_="text-lowercase").text.split()[-1] if block.find("span", class_="text-lowercase") else None

                    # Default values
                    status = "NEW"

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
        page = 0
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

    def get_all_topics(self):
        html_content = """
        <div id="topic-list" class="row mt-3 pb-4" style="background-color: #f7f7f7">
            <div class="col-6 col-md-4 mt-4">
                <h4><a href="/topic/26/culture">Culture</a></h4>
                <a href="/topic/22/culture/books">Books</a>
                <span class="text-muted">∘</span>
                <a href="/topic/25/culture/music">Music</a>
            </div>
            <div class="col-6 col-md-4 mt-4">
                <h4><a href="/topic/1/it">IT</a></h4>
                <a href="/topic/8/it/comsec">Computer Security</a>
                <span class="text-muted">∘</span>
                <a href="/topic/29/it/cryptocurrency">Cryptocurrency</a>
                <span class="text-muted">∘</span>
                <a href="/topic/51/it/crypto-mining">Cryptocurrency Mining</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/4/it/data-science">Data Science</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/7/it/database">Databases</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/12/it/electronics">Electronics</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/31/it/general">General</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/13/it/job">Jobs</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/11/it/management">Management</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/6/it/os">Operating Systems</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/5/it/seo-marketing">SEO/SMM/Marketing</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/2/it/dev">Software Development</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/3/it/sysadmin">SysAdmin &amp; DevOps</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/14/it/unsorted">Unsorted</a>
                
                
            </div>
        
            <div class="col-6 col-md-4 mt-4">
                <h4><a href="/topic/30/misc">Misc</a></h4>
                
                <a href="/topic/18/misc/adult">Adult</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/24/misc/auto">Auto</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/16/misc/finance">Finance</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/20/misc/local">Geo &amp; Local</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/17/misc/sport">Sport</a>
                
                
            </div>
        
            <div class="col-6 col-md-4 mt-4">
                <h4><a href="/topic/27/science">Science &amp; Education</a></h4>
                
                <a href="/topic/15/science/maths">Mathematics</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/19/science/medicine">Medicine</a>
                <span class="text-muted">∘</span>
                
                <a href="/topic/28/science/philosophy">Philosphy</a>
                
                
            </div>
        
            <div class="col-6 col-md-4 mt-4">
                <h4><a href="/topic/23/unsorted">Unsorted</a></h4>
                
            </div>
        </div>
        """

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 提取所有 <a> 标签的 href 属性值
        topics = [a['href'] for a in soup.find_all('a', href=True)]
        return topics

    def daily_task(self):
        print(f"Starting daily Tgram crawl task, start_time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        host = 'https://tgram.io'
        topics = ['/']
        topics.extend(self.get_all_topics())
        print(topics)
        # https://tgram.io/?lang=&page={page}
        for topic in topics:
            url = host + topic + '?lang='
            self.crawl_all_pages(url)

        print(f"Finished daily Tgram crawl task, end_time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def close(self):
        self.db.close()

def run_daily_task():
    crawler = TgramAutoCrawler()
    crawler.daily_task()
    crawler.close()



DEFAULT_LIST_ROWS = 100
if __name__ == "__main__":
    # schedule.every().day.at("02:00").do(run_daily_task)  # Run daily at 2 AM

    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)  # Check every minute

    run_daily_task()
