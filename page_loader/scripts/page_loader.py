#!/usr/bin/python2
import sys

from page_loader.parsing_cli import parsing_cli
from page_loader import download
from page_loader.download import logger


def main():
    args = parsing_cli()
    try:
        file_path = download(args.URL, args.output)
        print('\n', file_path)
    except Exception as e:
        logger.debug(e)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
