import time

import requests
from pymongo import MongoClient
from envparse import Env

from parser import all_dishes_by_page, dish_full_content_parser

env = Env()


def create_records() -> dict:
    mongo_client = client["yourmeals"]
    
    total_pages = 714
    page = 647
    while page <= total_pages:
        try:
            all_dishes = all_dishes_by_page(page)
            time.sleep(15)
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
                time.sleep(10)
            except requests.exceptions.Timeout:
                print("-"*5, f"new href error for dish {dish_num}", "-"*5)
                print((href, img, tags))
                time.sleep(600)
                try:
                    dish_info = dish_full_content_parser(href)
                    dish_info['img_src'] = img
                    dish_info['tags'] = tags
                    mongo_client.dishes.insert_one(dish_info)
                    time.sleep(9)
                except requests.exceptions.Timeout:
                    print("-"*5, f"new href error for dish {dish_num}", "-"*5)
                    print((href, img, tags))
                    time.sleep(300)
                    try:
                        dish_info = dish_full_content_parser(href)
                        dish_info['img_src'] = img
                        dish_info['tags'] = tags
                        mongo_client.dishes.insert_one(dish_info)
                        time.sleep(9)
                    except requests.exceptions.Timeout:
                        print("-"*5, f"new href error for dish {dish_num}", "-"*5)
                        print((href, img, tags))
                        time.sleep(300)
                
        print(f"page {page} done")
        page += 1
    
    return {"Success": True}


if __name__ == "__main__":
    client = MongoClient(MONGODB_URL)
    print(create_records())
