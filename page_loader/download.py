import requests
import logging
import os
import re
import shutil
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='[%(asctime)s: %(levelname)s] %(message)s')


def download(url_string, output_path):
    if not output_path:
        output_path = os.getcwd()
    if not os.path.exists(output_path):
        logger.error('This folder does not exist')
        raise FileExistsError
    response = requests.get(url_string)
    try:
        response.raise_for_status()
    except Exception:
        logger.error(f'No connection '
                     f'to {url_string}')
        logger.debug(f'exception requests.exceptions.HTTPError '
                     f'to {url_string}')
        raise KnownError
    response.raise_for_status()
    name_of_output_file = output_path + '/' + make_name(url_string)
    soup = BeautifulSoup(response.text, 'html.parser')
    change_obj = make_change(soup, make_name(url_string, True), url_string)
    output_html = make_output_html(response.text, change_obj)
    make_dir_and_img(output_path, make_name(url_string, True), change_obj)
    with open(name_of_output_file, 'w') as out_file:
        out_file.write(output_html.prettify())
    return name_of_output_file


def make_change(soup, name_of_output_dir, url_string):
    domain_regex = r"http\w{0,}:\/\/\S{1,}?\/"
    domain = re.findall(domain_regex, url_string)[0]
    img_array = make_download_array(soup, 'img', domain)
    link_array = make_download_array(soup, 'link', domain)
    script_array = make_download_array(soup, 'script', domain)
    change_array = img_array + link_array + script_array
    change_obj = {}
    for i in change_array:
        download_url = (domain + i).replace('//', '/').replace(':/', '://')
        change_obj[i] = [name_of_output_dir + '/' + make_name(domain + i),
                         download_url]
    return change_obj


def make_download_array(soup, tag, domain):
    array = list(soup.find_all(tag))
    if tag == 'img' or tag == 'script':
        array = [i.get('src').replace(domain, '') for i in array
                 if (i.get('src') and ('htt' not in str(i.get('src'))
                                       .replace(domain, '')))]
    else:
        array = [i.get('href').replace(domain, '') for i in array
                 if ('http' not in i.get('href').replace(domain, ''))]
    return array


def make_name(url_string, dir=False):
    result_name = ''
    for i in url_string:
        if i.isalnum():
            result_name += i
        else:
            result_name += ' '
    result_name = result_name.replace('svg', 'png')
    result_name_array = result_name.split()
    schem = [x for x in result_name_array if 'http' in x][0]
    result_name_array.remove(schem)
    if result_name_array[-1] not in 'html, css, jpg, png, svg, js':
        result_name_array.append('html')
    if dir:
        result_name = '-'.join(result_name_array[:-1]) + '_files'
    else:
        result_name = '-'.join(result_name_array[:-1]) + \
                      '.' + \
                      result_name_array[-1]
    return result_name


def make_output_html(soup, change_obj):
    output_html = str(soup)
    for i in change_obj:
        output_html = output_html.replace(change_obj[i][1], change_obj[i][0]) \
            .replace(i, change_obj[i][0])
    return BeautifulSoup(output_html, 'html.parser')


def make_dir_and_img(output_path, dir_name, change_obj):
    try:
        os.mkdir(output_path + '/' + dir_name)
    except FileExistsError:
        logger.debug('exception FileExistsError')
        shutil.rmtree(output_path + '/' + dir_name)
        os.mkdir(output_path + '/' + dir_name)
    bar = IncrementalBar(
        'Loading',
        fill='@',
        suffix='%(percent)d%%',
        max=len(change_obj)
    )
    for i in change_obj:
        bar.next()
        response = requests.get(change_obj[i][1])
        try:
            response.raise_for_status()
        except Exception:
            logger.error(f'No connection '
                         f'to {change_obj[i][1]}')
            logger.debug(f'exception requests.exceptions.HTTPError '
                         f'to {change_obj[i][1]}')
            continue
        response.raise_for_status()
        obj_path = output_path + '/' + change_obj[i][0]
        with open(obj_path, 'wb') as out_file:
            out_file.write(response.content)


class KnownError(Exception):
    pass
