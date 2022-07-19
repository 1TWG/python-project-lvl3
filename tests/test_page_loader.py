import pytest
from page_loader.download import KnownError

from page_loader import download
from page_loader.download import make_output_html
from page_loader.download import make_change
from page_loader.download import make_name
import pathlib
import tempfile
from bs4 import BeautifulSoup


def test_download():
    with tempfile.TemporaryDirectory() as temp_dir_name:
        file_path = download('https://ru.hexlet.io/courses', temp_dir_name)
        assert file_path == temp_dir_name + '/ru-hexlet-io-courses.html'
        with open(file_path, 'r') as test_file:
            temp1 = test_file.read()
            assert temp1


def test_make_output_html_images():
    path_file_before = 'tests/fixtures/before_ru-hexlet-io-courses.html'
    path_file_after = 'tests/fixtures/after_ru-hexlet-io-courses.html'
    with open(path_file_before, 'r') as before_file, \
            open(path_file_after, 'r') as after_file:
        after_soup = BeautifulSoup(after_file.read(), 'html.parser')
        before_soup = BeautifulSoup(before_file.read(), 'html.parser')
        change_images = make_change(before_soup, 'ru-hexlet-io-courses_files', 'https://ru.hexlet.io/courses')
        output_html = make_output_html(before_soup, change_images)
        assert after_soup.title == before_soup.title
        assert after_soup.prettify() == output_html


def test_make_output_html_files():
    path_file_before = 'tests/fixtures/before_files_ru-hexlet-io-courses.html'
    path_file_after = 'tests/fixtures/after_files_ru-hexlet-io-courses.html'
    with open(path_file_before, 'r') as before_file, \
            open(path_file_after, 'r') as after_file:
        after_soup = BeautifulSoup(after_file.read(), 'html.parser')
        before_soup = BeautifulSoup(before_file.read(), 'html.parser')
        change_images = make_change(before_soup, 'ru-hexlet-io-courses_files', 'https://ru.hexlet.io/courses')
        output_html = make_output_html(before_soup, change_images)
        assert after_soup.title == before_soup.title
        assert after_soup.prettify() == output_html


def test_make_name():
    test_names = ['snipp-ru-demo-76-index.html',
                  'snipp-ru-logo.png',
                  'snipp-ru-demo-76-Yamaha-1.png',
                  'snipp-ru-demo-76-Yamaha-2.png',
                  'snipp-ru-style.css']
    test_urls = ['https://snipp.ru/demo/76/index.html',
                 'https://snipp.ru/logo.png',
                 'https://snipp.ru//demo/76/Yamaha-1.jpg',
                 'https://snipp.ru//demo/76/Yamaha-2.svg',
                 'https://snipp.ru/style.css']
    resul_names = [make_name(i) for i in test_urls]
    assert resul_names == test_names
    assert 'snipp-ru-demo-76-index_files' == make_name('https://snipp.ru/demo/76/index.html', True)


def test_unknow_dir():
    with pytest.raises(KnownError):
        download('https://ru.hexlet.io/courses', '891877987/DASD48S7D')


def test_unknow_url():
    with pytest.raises(KnownError):
        with tempfile.TemporaryDirectory() as temp_dir_name:
            download('https://ru.hexlet.io/4154610615dasd', temp_dir_name)