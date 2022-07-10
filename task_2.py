import json
import re
import requests
from bs4 import BeautifulSoup

base_url = 'https://ru.wikipedia.org'
first_page_appendix_url = '/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'


def get_animals(base_url, appendix_url):
    alphabet = {}
    while True:
        resp = requests.get(base_url + appendix_url)  # получаем страницу каталога
        soup = BeautifulSoup(resp.text, 'html.parser')  # парсим с помощью bs4
        columns = soup.find('div', 'mw-category-columns')  # выбираем div с классом mw-category-columns
        animals = columns('li')  # собираем элементы списка животных

        for animal in animals:
            animal_name = animal.a.text
            first_letter = animal_name[0]

            if first_letter.lower() == 'a':  # как только начинаются англоязычные названия, останавливаем цикл
                return alphabet
            if first_letter.lower() in 'abcdefghijklnmopqrstuvwxyz':  # среди русскоязычных названий встречаются английские
                continue  # исключаем их из списка
            if first_letter not in alphabet.keys(): # добавляем в словарь имя животного
                alphabet[first_letter] = [animal_name]
                print(f'Собираются животные на букву: {first_letter}')
            else:
                alphabet[first_letter].append(animal_name)

        try:
            next_page = soup.find_all('a', text=re.compile('Следующая страница'))[0]['href']  # получаем ссылку на следующию страницу
            appendix_url = next_page

        except:  # если страницы закончились, останавливаем цикл
            break


alphabet = get_animals(base_url, first_page_appendix_url)
with open('animals.json', 'w') as file:
    json.dump(alphabet, file, ensure_ascii=False, indent=4)

# with open('animals.txt', 'r', encoding='utf-8') as file: # сохраняем имена в json файл
#     alphabet = json.load(file)


for letter in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':  # при сортировке словаря стандартным методом на первое место выходит буква Ё
    # поэтому сортируем по алфавиту
    try:
        print(f'{letter}: {len(alphabet[letter])}')
    except:  # пропускаем букву, если на нее не начинается ни одно животное
        continue

