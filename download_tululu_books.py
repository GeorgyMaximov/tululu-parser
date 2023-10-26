import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import urllib.parse
import argparse
import time


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_page(soup, book_id):
    title = soup.select_one('h1').text.split('::')[0].strip()
    author = soup.select_one('h1').text.split('::')[1].strip()
    genres = [genre.text for genre in soup.select_one('span.d_book a')]
    image_url = urllib.parse.urljoin(f'https://tululu.org/b{book_id}/', soup.select_one('.bookimage img')['src'])
    comments = [comment.select_one('span').text for comment in soup.select('.texts')]
    parsed_book_page = {
        'title': title,
        'author': author,
        'genres': genres,
        'image_url': image_url,
        'comments': comments
    }
    return parsed_book_page


def download_book(book_id, book_title, dest_folder):
    url = f'https://tululu.org/txt.php'
    params = {'id': book_id}
    response = requests.get(url, params)
    check_for_redirect(response)
    response.raise_for_status()
    filename = os.path.join(dest_folder, 'books', f'{book_id}. {sanitize_filename(book_title)}.txt')
    with open(filename, 'wb') as file:
        file.write(response.content)


def download_book_image(image_url, dest_folder):
    response = requests.get(image_url)
    check_for_redirect(response)
    response.raise_for_status()
    filename = os.path.join(dest_folder, 'images', urllib.parse.urlsplit(image_url)[2].split("/")[-1])
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    parser = argparse.ArgumentParser(description='Скачивание книг')
    parser.add_argument('--dest_folder', default='result', help='путь к каталогу с результатами парсинга')
    parser.add_argument('--start_id', type=int, default=1, help='ID первой книги')
    parser.add_argument('--end_id', type=int, default=11, help='ID последней книги')
    args = parser.parse_args()
    os.makedirs(args.dest_folder, exist_ok=True)
    os.makedirs(f'{args.dest_folder}/books', exist_ok=True)
    os.makedirs(f'{args.dest_folder}/images', exist_ok=True)
    for book_id in range(args.start_id, args.end_id):
        url = f'https://tululu.org/b{book_id}/'
        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            parsed_book_page = parse_book_page(soup, book_id)
            download_book(book_id, parsed_book_page['title'], args.dest_folder)
            download_book_image(parsed_book_page['image_url'], args.dest_folder)
        except requests.HTTPError:
            print('Такой книги не существует')
        except requests.ConnectionError:
            print('Отсутствует соединение')
            time.sleep(10)


if __name__ == '__main__':
    main()