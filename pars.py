import requests
from bs4 import BeautifulSoup
import csv
import subprocess

URL = 'https://www.ozon.ru/search/'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.234', 'accept':'*/*'}
HOST = 'https://www.ozon.ru'
STRINGS = 20 # 1 string this is 4 objects
FILE = 'Ozon.csv'

def get_html(url, params = None):
	r = requests.get(url, headers = HEADERS, params = params)
	r.encoding = 'UTF-8'
	return r

def get_content(html):

	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_ = 'a0c4')
	objects = []

	for item in items:
		objects.append({
			'title' : item.find('a', class_= 'a2g0 tile-hover-target').get_text(strip = True).replace(',', ''),
			'link' : HOST + item.find('a', class_ = 'a2g0 tile-hover-target').get('href'),
			'price' : item.find('span', class_ = 'a0y4').get_text(strip = True).replace('&thinsp;', '')})
	return objects

def save_in_file(items, path):
	with open(path, 'w', newline = '') as file:
		writer = csv.writer(file, delimiter = ';')
		writer.writerow(['Название', 'Ссылка', 'Цена'])
		for item in items:
			writer.writerow([item['title'], item['link'], item['price']])

def parse():

	html = get_html(URL)
	if html.status_code == 200:
		objects = []
		print('Подготовка к парсину...')
		for page in range(1, STRINGS+1):
			print(f'	Строка {page} обрабатывается, всего {STRINGS}...')
			html = get_html(URL, params = {'from_global' : 'true','text' : 'карты+таро','page' : page})
			objects.extend(get_content(html.text))
		print('Запись объектов в csv файл...')
		save_in_file(objects, FILE)
		print(f'Парсинг завершен, получено {len(objects)} объектов')
		subprocess.call(['libreoffice Ozon.csv'], shell = True)
	else:
		print('Error')

parse()