import requests
from bs4 import BeautifulSoup as bs


def all_dishes_by_page(page: int) -> list:
    """
    Returns:
        list: Список с блюдами вида [ tuple1, tuple2, ... ]
        
        tuple состоит из (href, img_src, tags: list)
        Пример:
        (
            '/recepty/vypechka-deserty/brauni-brownie-20955', 
            'https://eda.ru/img/eda/c180x180/s1.eda.ru/StaticContent/Photos/120131082911/130725174021/p_O.jpg', 
            ['Выпечка и десерты', 'Американская кухня']
        )
    """
    
    # Результирующий список всех блюд
    all_dishes_on_page = []
    
    # Проходимся по всем страниц на сайте
        
    # Шаблон URL имени
    PAGE_URL = f'https://eda.ru/recepty?page={page}'
    
    # Делаем запрос на сервер и сохраняем ответ
    req = requests.get(PAGE_URL, timeout=5)
    
    # Берем контент из ответа 
    html_content = req.text
    
    # Создаем парсер
    parser = bs(html_content, "html.parser")
    
    # Ищем тег, отвечающий за блюдо. В emotion-m0u77r всегда находится блюдо
    all_dishes_raw_content = parser.find_all("div", class_="emotion-m0u77r")
    
    # Выделяем в каждом блюде ссылку на подробную страницу блюда, ссылку на превью изображения и теги
    for dish_content in all_dishes_raw_content:
        if dish_content:
            href = dish_content.a['href']
            img_src = dish_content.img['src']
            
            raw_tags = dish_content.find_all('span', class_='emotion-ld5tpo')
            tags = [x.text for x in raw_tags]
            
            all_dishes_on_page.append((href, img_src, tags))
    
    return all_dishes_on_page
    

def dish_full_content_parser(href: str) -> dict:
    dish_info = {}
    
    # Шаблон URL блюда
    DISH_URL = "https://eda.ru" + href
    
    # Делаем запрос на сервер и сохраняем ответ
    req = requests.get(DISH_URL, timeout=5)
    
    # Берем контент из ответа 
    html_content = req.text
    
    # Создаем парсер
    parser = bs(html_content, "html.parser")
    
    # Ищем тег, отвечающий за заголовок страницы, и добавляем полученный контент в результирующий словарь
    # По такому же принципу далее азполняем словарь. 
    title = parser.select("h1", class_="emotion-gl52ge")
    dish_info['name'] = title[0].text.replace(u'\xa0', u' ')
    
    # Число порций
    portions = parser.find("span", class_="emotion-17j44go")
    if portions:
        dish_info['portions'] = int(portions.text[-1])
    else:
        print(f'Empty portions for {href}\n', portions)
        dish_info['portions'] = 4
    
    # Время приготовления
    preparing_time = parser.find("div", class_="emotion-my9yfq")
    if preparing_time:
        dish_info['preparing_time'] = preparing_time.text
    else:
        print(f'Empty preparing_time for {href}\n', preparing_time)
        dish_info['preparing_time'] = '40 минут'
    
    # Описание блюда
    description = parser.find("span", class_="emotion-1x1q7i2")
    if description:
        dish_info['description'] = description.text.replace(u'\xa0', u' ')
    else:
        print(f'Empty description for {href}\t', description)
        dish_info['description'] = "Нет описания"
    
    # Энергетическая ценность: { калории, белки, жиры, углеводы }
    energy_value = parser.find_all("div", class_="emotion-8fp9e2")
    if energy_value:
        dish_info['calories'] = int(energy_value[0].text)
        dish_info['proteins'] = int(energy_value[1].text)
        dish_info['fats'] = int(energy_value[2].text)
        dish_info['carbohydates'] = int(energy_value[3].text)
    else:
        print(f'Empty energy_value for {href}\t', energy_value)
        dish_info['calories'] = 500
        dish_info['proteins'] = 30
        dish_info['fats'] = 50
        dish_info['carbohydates'] = 100
    
    # Ингредиенты. Собираем его имя и количество. Образуем словарь вида { 'ingredients_name': 'ingredients_value' }
    ingredients_name = parser.find_all("span", class_="emotion-1g8buaa")
    ingredients_value = parser.find_all("span", class_="emotion-15im4d2")
    dish_info['ingredients'] = {}
    for index in range(len(ingredients_name)):
        dish_info['ingredients'][ingredients_name[index].text] = ingredients_value[index].text
    
    # Пошаговое приготовление блюда. Образуем список вида [ '1 описание шага', '2 описание шага', ... ]
    recipe = parser.find_all("div", class_="emotion-19fjypw")
    if recipe:
        dish_info['recipe'] = [value.text.replace(u'\xa0', u' ')[1:] for value in recipe]
    else:
        recipe = parser.find_all("div", class_="emotion-ip3ree")
        if recipe:
            dish_info['recipe'] = [value.text.replace(u'\xa0', u' ')[1:] for value in recipe]
        else:
            print(f'Empty recipe for {href}\t', recipe)
            dish_info['recipe'] = 'Нет рецепта'
    
    return dish_info

if __name__ == '__main__':
    all_dishes = all_dishes_by_page(1)

    href, img, tags = all_dishes[0]
    dish_info = dish_full_content_parser(href)
    dish_info['img_src'] = img
    dish_info['tags'] = tags
    
    print(dish_info)
    # for key, value in dish_info.items():
    #     print(f"{key}: {value}", end="\n\n")
