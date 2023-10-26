# Парсер книг с сайта tululu.org

Программа скачивает книги и картинки книг с сайта [tululu.org](https://tululu.org)

## Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

## Как запустить

### download_tululu_books.py

Скачивает все книги по порядку.

```
python download_tululu_books.py --start_id 1 --end_id 10
```

Аргумент `--start_id` отвечает за ID первой скачанной книги, аргумент `--end_id` отвечает за ID последней скачанной книги.

Запуск программы без аргументов:

```
python download_tululu_books.py
```

### parse_tululu_category.py

Скачивает только научную фантастику.

```
python parse_tululu_category.py --start_page 5 --end_page 10 --skip_txt --skip_images --dest_folder a
```

Аргумент `--start_page` отвечает за номер первой скачанной страницы, `--end_page` отвечает за номер последней страницы.

Аргумент `--skip_txt` отвечает за пропуск книг, `--skip_images` отвечает за пропуск картинок.

Аргумент `--dest_folder` отвечает за название папки, в которую будут скачиваться книги, картинки и информация о книгах.

Запуск программы без аргументов:

```
python parse_tululu_category.py
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
