import argparse
import collections
import datetime
import pandas

from settings import DATA_FILE

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

DATA_OF_FOUNDATION = datetime.datetime(year=1920, month=1, day=1, hour=0)

today = datetime.date.today()
winery_age = today.year - DATA_OF_FOUNDATION.year


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default=DATA_FILE)
    return parser


parser = createParser()
namespace = parser.parse_args()


if namespace.filename:
    excel_data_products = pandas.read_excel(namespace.filename)
else:
    excel_data_products = pandas.read_excel(DATA_FILE)

products = excel_data_products.to_dict(orient='record')

products_by_category = collections.defaultdict(list)


for wine in products:
    category = wine['Категория']
    products_by_category[category].append(wine)


rendered_page = template.render(
    years=winery_age,
    alcohol=products_by_category,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
