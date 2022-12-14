import time

import requests
from pymongo import MongoClient
from envparse import Env

from dish_parser import all_dishes_by_page, dish_full_content_parser


env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/yourmeals")


def create_records() -> dict:
    mongo_client = client["yourmeals"]
    
    total_pages = 714
    page = 0
    while page <= total_pages:
        try:
            all_dishes = all_dishes_by_page(page)
            time.sleep(10)
        except requests.exceptions.Timeout:
            print(f"page {page} - error Timeout. Try again")
            time.sleep(600)        
            continue
        
        for href, img, tags in all_dishes:
            while True:
                try:
                    dish_info = dish_full_content_parser(href)
                    dish_info['img_src'] = img
                    dish_info['tags'] = tags
                    mongo_client.dishes.insert_one(dish_info)
                    time.sleep(10)
                    break
                except requests.exceptions.Timeout:
                    print("error: ", (href, img, tags))
                    time.sleep(600)
                
        print(f"page {page} done")
        page += 1
    
    return {"Success": True}


if __name__ == "__main__":
    client = MongoClient(MONGODB_URL)
    print(create_records())
