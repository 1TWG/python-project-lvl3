import requests
import os
import re
import shutil
from bs4 import BeautifulSoup


def download(url_string, output_path):
    if not output_path:
        output_path = os.getcwd()
    response = requests.get(url_string)
    response.raise_for_status()
    name_of_output_file = output_path + '/' + make_name(url_string, '.html')
    name_of_output_dir = output_path + '/' + make_name(url_string, '_files')
    soup = BeautifulSoup(response.text, 'html.parser')
    change_images = make_change(soup, name_of_output_dir, url_string)
    output_html = make_output_html(soup, change_images)
    make_dir_and_img(name_of_output_dir, change_images)
    with open(name_of_output_file, 'w') as out_file:
        out_file.write(output_html)
    return name_of_output_file


def make_change(soup, name_of_output_dir, url_string):
    domain_regex = r"http\w{0,}:\/\/\S{1,}?\/"
    domain = re.findall(domain_regex, url_string)[0]
    img_array = make_download_array(soup, 'img')
    change_img = {i: [name_of_output_dir + '/' + make_name(domain + i, '.png'),
                      domain + i] for i in img_array}
    return change_img


def make_name(url_string, extension):
    result_name = ''
    for i in url_string:
        if i.isalnum():
            result_name += i
        else:
            result_name += ' '
    result_name = result_name.split()
    remove_array = [
        'https',
        'html',
        'png',
        'jpg',
        'svg'
    ]
    for i in remove_array:
        if i in result_name:
            result_name.remove(i)
    result_name = '-'.join(result_name) + extension
    return result_name


def make_download_array(soup, tag):
    img_array = list(soup.find_all(tag))
    regex = r"(?<=src=\")(?!http).{1,}(?=\")"
    img_array = [re.findall(regex, str(i))[0] for i in img_array
                 if re.findall(regex, str(i))]
    return img_array


def make_output_html(soup, change_images):
    output_html = str(soup)
    for i in change_images:
        output_html = output_html.replace(i, change_images[i][0])
    return BeautifulSoup(output_html, 'html.parser').prettify()


def make_dir_and_img(name_of_output_dir, change_images):
    try:
        os.mkdir(name_of_output_dir)
    except FileExistsError:
        shutil.rmtree(name_of_output_dir)
    os.mkdir(name_of_output_dir)
    for i in change_images:
        response = requests.get(change_images[i][1])
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            continue
        response.raise_for_status()
        img_path = change_images[i][0]
        with open(img_path, 'wb') as out_file:
            out_file.write(response.content)
