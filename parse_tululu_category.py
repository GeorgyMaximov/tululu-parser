from bs4 import BeautifulSoup
import requests
import urllib.parse
import json
import time
import argparse
import os
from download_tululu_books import check_for_redirect, parse_book_page, download_book, download_book_image


def main():
    parser = argparse.ArgumentParser(description='Скачивание книг')
    parser.add_argument('--start_page', type=int, default=1, help='номер первой страницы')
    parser.add_argument('--end_page', type=int, default=5, help='номер последней страницы')
    parser.add_argument('--skip_images', action="store_true", help='пропустить скачивание картинок')
    parser.add_argument('--skip_txt', action="store_true", help='пропустить скачивание текстов')
    parser.add_argument('--dest_folder', default='result', help='путь к каталогу с результатами парсинга')
    args = parser.parse_args()

    os.makedirs(args.dest_folder, exist_ok=True)
    os.makedirs(f'{args.dest_folder}/books', exist_ok=True)
    os.makedirs(f'{args.dest_folder}/images', exist_ok=True)

    parsed_book_pages = []
    urls = []

    for page in range(args.start_page, args.end_page):
        url = f'https://tululu.org/l55/{page}/'
        try:
            response = requests.get(url)
            check_for_redirect(response)
        except requests.HTTPError:
            print('Такой страницы не существует')
        except requests.ConnectionError:
            print('Отсутствует соединение')
            time.sleep(10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        for book in soup.select('table.d_book'):
            url = urllib.parse.urljoin(url, book.find('a')['href'])
            urls.append(url)

    for url in urls:
        try:
            book_id = url.split('/')[-2][1:]
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            parsed_book_page = parse_book_page(soup, book_id)
            parsed_book_pages.append(parsed_book_page)
            if not args.skip_txt:
                download_book(book_id, parsed_book_page['title'], args.dest_folder)
            if not args.skip_images:
                download_book_image(parsed_book_page['image_url'], args.dest_folder)
        except requests.HTTPError:
            print('Такой книги не существует')
        except requests.ConnectionError:
            print('Отсутствует соединение')
            time.sleep(10)

    with open(os.path.join(args.dest_folder, 'books_info.json'), 'w', encoding='utf-8') as file:
        json.dump(parsed_book_pages, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
