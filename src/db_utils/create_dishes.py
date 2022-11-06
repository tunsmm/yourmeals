import time

import requests
from pymongo import MongoClient
from envparse import Env

from parser import all_dishes_by_page, dish_full_content_parser

env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://194.67.113.68:27017/yourmeals")


def create_records() -> dict:
    mongo_client = client["yourmeals"]
    
    total_pages = 714
    href_errors = []
    page = 91
    while page <= total_pages:
        try:
            all_dishes = all_dishes_by_page(page)
            time.sleep(30)
        except requests.exceptions.Timeout:
            print(f"page {page} - error Timeout. Try again")
            time.sleep(600)        
            continue
        
        dish_num = 0
        for href, img, tags in all_dishes:
            dish_num += 1
            try:
                dish_info = dish_full_content_parser(href)
                dish_info['img_src'] = img
                dish_info['tags'] = tags
                mongo_client.dishes.insert_one(dish_info)
                time.sleep(8)
            except requests.exceptions.Timeout:
                print("-"*5, f"new href error for dish {dish_num}", "-"*5)
                href_errors.append((href, img, tags))
                print((href, img, tags))
                time.sleep(600)
                dish_info = dish_full_content_parser(href)
                dish_info['img_src'] = img
                dish_info['tags'] = tags
                mongo_client.dishes.insert_one(dish_info)
                time.sleep(30)
                
        print(f"page {page} done")
        page += 1
    
    return {"Success": True, "Errors": href_errors}


if __name__ == "__main__":
    client = MongoClient(MONGODB_URL)
    print(create_records())
