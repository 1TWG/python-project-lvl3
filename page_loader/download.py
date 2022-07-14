import requests
import os
from bs4 import BeautifulSoup
import re


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
        'html'
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
    img_link_array = soup.find_all('img')
    download_img(list(img_link_array), url_string, output_path)
    with open(result, 'w') as out_file:
        out_file.write(response.text)
    return result


def download_img(img_array, url_string, output_path):
    regex = r"(?<=src=\")(?!http).{1,}(?=\")"
    img_urls = []
    domain_regex = r"http\w{0,}:\/\/\S{1,}?\/"
    domain = re.findall(domain_regex, url_string)[0]
    img_array = find_local_file(img_array, regex)
    for i in img_array:
        if i[0] == '/':
            temp = domain + i[1:]
        else:
            temp = domain + i
        img_urls.append(temp)
    name_of_output_dir = make_name(url_string, '_files')
    make_dir_and_img(name_of_output_dir, img_urls, output_path)


def make_dir_and_img(name_of_output_dir, img_urls, output_path):
    for i in img_urls:
        img_path = output_path + '/' + name_of_output_dir + '/' + get_img_name(i)
        print(img_path)
        response = requests.get(i)
        try:
            response.raise_for_status()
        except:
            continue
        response.raise_for_status()
        #with open(img_path, 'wb') as out_file:
        #    out_file.write(response.content)



def get_img_name(img_url):
    return img_url.split('/')[-1]


def find_local_file(img_array, regex):
    img_array = [re.findall(regex, str(i))[0] for i in img_array if re.findall(regex, str(i))]
    return img_array
