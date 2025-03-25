from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime


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


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')

rendered_page = template.render(
    text_age=f'Уже {get_year_word()} с вами'
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
