import requests
import os
from bs4 import BeautifulSoup
import re


def make_name_to_html(url_string):
    result_name = ''
    for i in url_string:
        if i.isalnum():
            result_name += i
        else:
            result_name += ' '
    result_name = result_name.split()
    remove_array = [
        'https',
        'html'
    ]
    for i in remove_array:
        if i in result_name:
            result_name.remove(i)
    result_name = '-'.join(result_name) + '.html'
    return result_name


def download(url_string, output_path):
    if not output_path:
        output_path = os.getcwd()
    response = requests.get(url_string)
    response.raise_for_status()
    name_of_output_file = make_name_to_html(url_string)
    result = output_path + '/' + name_of_output_file
    soup = BeautifulSoup(response.text, 'html.parser')
    img_link_array = soup.find_all('img')
    download_img(list(img_link_array))
    with open(result, 'w') as out_file:
        out_file.write(response.text)
    return result


def download_img(img_array):
    regex = r"(?<=src=\")(?!http).{1,}(?=\")"
    matches = []
    for i in img_array:
        matches.extend(re.findall(regex, str(i)))
    print(matches)
