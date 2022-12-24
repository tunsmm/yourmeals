import requests
import time
import traceback

from pymongo import MongoClient
from envparse import Env
from tqdm import tqdm

from dish_parser import all_dishes_by_page, dish_full_content_parser


env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/yourmeals")


def create_records() -> dict:
    mongo_client = client["yourmeals"]
    
    # For not going to the base every iteration
    dishes_on_mongo = mongo_client.dishes3.find({})
    names_of_dishes_mongo = set([dish['name'] for dish in dishes_on_mongo])
    
    total_pages = 10094
    page = 3866
    m_dupl = tqdm(desc="Duplicates")
    m_new = tqdm(desc="New dishes")
    m_pages = tqdm(desc="Pages")
    m_pages.update(page - 1)
    while page <= total_pages:
        try:
            all_dishes = all_dishes_by_page(page)
            time.sleep(2)
        except requests.exceptions.Timeout:
            print(f"page {page} - error Timeout. Try again")
            time.sleep(300)        
            continue
        except (ValueError, KeyError, TimeoutError, TypeError, AttributeError, IndexError) as e:
            print(f"\npage {page} - UNEXPECTED ERROR")
            print(traceback.format_exc(),)
            page += 1
            continue
        
        for name, href, img in all_dishes:
            if name in names_of_dishes_mongo:
                m_dupl.update(1)
                continue
            # three attempts to parse one dish
            for i in range(3):
                try:
                    dish_info = dish_full_content_parser(href)
                    dish_info['img_src'] = img
                    mongo_client.dishes3.insert_one(dish_info)
                    names_of_dishes_mongo.add(name)
                    m_new.update(1)
                    break
                except requests.exceptions.Timeout:
                    print("Timeout on dish: ", (name, href, ))
                    time.sleep(300)
                except (ValueError, KeyError, TimeoutError, TypeError, AttributeError, IndexError) as e:
                    print((name, href, ), traceback.format_exc(),)
                    break
                except Exception as e:
                    print((name, href, ), traceback.format_exc(),)
                    break
                
        m_pages.update(1)
        page += 1
    
    return {"Success": True}


if __name__ == "__main__":
    client = MongoClient(MONGODB_URL)
    print(create_records())
