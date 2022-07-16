import os

from page_loader import download
from page_loader.download import make_output_html
from page_loader.download import make_change
import pathlib
import tempfile
from bs4 import BeautifulSoup


def test_download():
    with tempfile.TemporaryDirectory() as temp_dir_name:
        os.mkdir(temp_dir_name + '/ru-hexlet-io-courses_files')
        file_path = download('https://ru.hexlet.io/courses', temp_dir_name)
        print(file_path)
        assert file_path == temp_dir_name + '/ru-hexlet-io-courses.html'
        with open(file_path, 'r') as test_file:
            temp1 = test_file.read()
            assert temp1


def test_make_output_html():
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

