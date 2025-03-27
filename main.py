from environs import Env
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas
import collections
import argparse


def get_year_word():
    year = calculating_age_company()
    if year % 100 in (11, 12, 13, 14):
        return f'{year} лет'
    last_digit = year % 10
    if last_digit == 1:
        return f'{year} год'
    if 2 <= last_digit <= 4:
        return f'{year} года'
    return f'{year} лет'


def calculating_age_company():
    get_startet = 1920
    difference = datetime.now().year - get_startet
    return difference


def main():
    env = Env()
    env.read_env()
    excel_path = env.str('EXCEL_PATH', default='table_of_property_wine.xlsx')

    parser = argparse.ArgumentParser(description='Введите путь до файла, либо же название файла, если он уже находится в директории скрипта')
    parser.add_argument('--path', default=excel_path, help='Путь')
    args = parser.parse_args()

    excel_data_wine2 = pandas.read_excel(args.path).fillna('')

    wines_dict = collections.defaultdict(list)

    for _, row in excel_data_wine2.iterrows():
        category = row['Категория']
        wine_data = {
            'Картинка': row['Картинка'],
            'Категория': row['Категория'],
            'Название': row['Название'],
            'Сорт': row['Сорт'],
            'Цена': row['Цена'],
            'Акция': row['Акция']
        }
        wines_dict[category].append(wine_data)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        age_text=f'Уже {get_year_word()} с вами',
        wines_dict=wines_dict
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
