import os

from page_loader import download
import pathlib, tempfile


def test_download():
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.mkdir(tmpdirname + '/ru-hexlet-io-courses_files')
        file_path = download('https://ru.hexlet.io/courses', tmpdirname)
        print(file_path)
        assert file_path == tmpdirname + '/ru-hexlet-io-courses.html'
        with open(file_path, 'r') as test_file:
            temp1 = test_file.read()
            assert temp1
