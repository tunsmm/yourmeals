import requests
from bs4 import BeautifulSoup as bs

from parser.utils import norm_text


def all_dishes_by_page(page: int) -> list:
    # Результирующий список всех блюд
    all_dishes_on_page = []
        
    # Шаблон URL имени
    PAGE_URL = f'https://www.povarenok.ru/recipes/~{page}/'
    
    # Делаем запрос на сервер и сохраняем ответ
    req = requests.get(PAGE_URL, timeout=5)
    
    # Берем контент из ответа 
    html_content = req.text
    
    # Создаем парсер
    parser = bs(html_content, "html.parser")
    
    # Ищем тег, отвечающий за блюдо. В emotion-m0u77r всегда находится блюдо
    all_dishes_raw_content = parser.find_all("article", class_="item-bl")
    
    # Выделяем в каждом блюде ссылку на подробную страницу блюда, ссылку на превью изображения и теги
    for dish_content in all_dishes_raw_content:
        if dish_content:
            name = norm_text(dish_content.h2.text)
            src = dish_content.h2.a['href']
            img = dish_content.find("div", class_="m-img conima").a.img['src']
            all_dishes_on_page.append((name, src, img))
    
    return all_dishes_on_page
    

def dish_full_content_parser(href: str) -> dict:
    dish_info = {}
    
    # Шаблон URL блюда
    DISH_URL = href

    # Делаем запрос на сервер и сохраняем ответ
    req = requests.get(DISH_URL, timeout=5)

    # Берем контент из ответа 
    html_content = req.text

    # Создаем парсер
    parser = bs(html_content, "html.parser")

    title = parser.select("h1")
    dish_info['name'] = norm_text(title[0].text)

    # Описание блюда
    description = parser.find("div", itemprop="description")
    if description:
        dish_info['description'] = norm_text(description.text)
    else:
        description = parser.find("div", class_="article-text")
        if description:
            dish_info['description'] = norm_text(description.p.text)
        else:
            dish_info['description'] = "Нет описания"

    tags = parser.find_all("span", itemprop="recipeCategory")
    if tags:
        dish_info['tags'] = norm_text(tags[0].text)
    else:
        tags = parser.find("div", class_="article-breadcrumbs")
        if tags:
            dish_info['tags'] = norm_text(tags.p.span.a.text)
        else:
            # Not normal, check results
            print('No tags for: ', DISH_URL)
            return {}

    # Ингредиенты. Собираем его имя и количество. Образуем словарь вида { 'ingredients_name': 'ingredients_value' }
    dish_info['ingredients'] = {}
    ingredients = parser.find_all("li", itemprop="recipeIngredient")
    if not ingredients:
        ingredients = parser.find("div", class_="ingredients-bl").select("li")
    for i, ing in enumerate(ingredients):
        try:
            dish_info['ingredients'][norm_text(ing.a.span.text)] = norm_text(ing.select("span")[1].text)
        except IndexError:
            pass

    # Время приготовления
    preparing_time = parser.find("time", itemprop="totalTime")
    if preparing_time:
        dish_info['preparing_time'] = norm_text(preparing_time.text)
    else:
        dish_info['preparing_time'] = '40 минут'

    # Число порций
    portions = parser.find("span", itemprop="recipeYield")
    if portions:
        dish_info['portions'] = int(norm_text(portions.text))
    else:
        try:
            portions = parser.find("div", class_="ingredients-bl").select("p")[-1]
            dish_info['portions'] = int(norm_text(portions.text[-2:]))
        except (IndexError, ValueError):
            dish_info['portions'] = 4

    # Энергетическая ценность: { калории, белки, жиры, углеводы }
    energy_value = parser.find("div", itemprop="nutrition")
    if energy_value:
        dish_info['calories'] = int(float(norm_text(energy_value.find("strong", itemprop="calories").text)[:-5]))
        dish_info['proteins'] = int(float(norm_text(energy_value.find("strong", itemprop="proteinContent").text)[:-2]))
        dish_info['fats'] = int(float(norm_text(energy_value.find("strong", itemprop="fatContent").text)[:-2]))
        dish_info['carbohydates'] = int(float(norm_text(energy_value.find("strong", itemprop="carbohydrateContent").text)[:-2]))
    else:
        # Default calories
        dish_info['calories'] = 500
        dish_info['proteins'] = 30
        dish_info['fats'] = 50
        dish_info['carbohydates'] = 100

    # Пошаговое приготовление блюда. Образуем список вида [ 'описание шага', 'описание шага', ... ]
    recipe = parser.find_all("li", class_="cooking-bl")
    recipe = recipe if recipe else parser.find_all("div", class_="cooking-bl")
    if not recipe:
        # Next to video or previous to article
        recipe = parser.find("div", class_="video-bl")
        if recipe:
            recipe = recipe.find_next_sibling('div').text
        else: 
            recipe = parser.find("div", class_="article-tags").find_previous_sibling('div').text
    try: 
        if isinstance(recipe, str):
            dish_info['recipe'] = [norm_text(value) for value in recipe.split('\n')]
        else:
            dish_info['recipe'] = [norm_text(value.div.p.text) for value in recipe]
    except AttributeError:
        # Not normal, check results
        print(f'Empty recipe for {DISH_URL}\t', recipe)
        dish_info['recipe'] = 'Нет рецепта'
    
    return dish_info
