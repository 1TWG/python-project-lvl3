import requests
import os
import re
import shutil
from bs4 import BeautifulSoup


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


def download(url_string, output_path):
    if not output_path:
        output_path = os.getcwd()
    response = requests.get(url_string)
    response.raise_for_status()
    name_of_output_file = make_name(url_string, '.html')
    result = output_path + '/' + name_of_output_file
    soup = BeautifulSoup(response.text, 'html.parser')
    img_link_array = list(soup.find_all('img'))
    regex = r"(?<=src=\")(?!http).{1,}(?=\")"
    img_array = find_local_file(img_link_array, regex)
    name_of_output_dir = make_name(url_string, '_files')
    output_html = make_output_html(soup.prettify(), img_array, name_of_output_dir)
    download_img(img_array, url_string, output_path, name_of_output_dir)
    with open(result, 'w') as out_file:
        out_file.write(output_html)
    return result


def make_output_html(input_html, img_array, name_of_output_dir):
    imgs = {i: name_of_output_dir + '/' + get_img_name(i) for i in img_array}
    output_html = str(input_html)
    for i in imgs:
        output_html = output_html.replace(i, imgs[i])
    return output_html


def download_img(img_array, url_string, output_path, name_of_output_dir):
    img_urls = []
    domain_regex = r"http\w{0,}:\/\/\S{1,}?\/"
    domain = re.findall(domain_regex, url_string)[0]
    for i in img_array:
        if i[0] == '/':
            temp = domain + i[1:]
        else:
            temp = domain + i
        img_urls.append(temp)

    make_dir_and_img(name_of_output_dir, img_urls, output_path)


def make_dir_and_img(name_of_output_dir, img_urls, output_path):
    dir_path = output_path + '/' + name_of_output_dir
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    for i in img_urls:
        response = requests.get(i)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            continue
        response.raise_for_status()
        img_path = dir_path + '/' + get_img_name(i)
        with open(img_path, 'wb') as out_file:
            out_file.write(response.content)


def get_img_name(img_url):
    temp = img_url.split('/')[-1]
    return make_name(temp, '.png')


def find_local_file(img_array, regex):
    img_array = [re.findall(regex, str(i))[0] for i in img_array
                 if re.findall(regex, str(i))]
    return img_array
