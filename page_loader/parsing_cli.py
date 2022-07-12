import argparse


def parsing_cli():
    parser = argparse.ArgumentParser(
        description='Saves the page by url.'
    )
    parser.add_argument('-o', '--output', help='set path of output')
    parser.add_argument('URL')

    args = parser.parse_args()
    return args
