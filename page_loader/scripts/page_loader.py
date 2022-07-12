#!/usr/bin/python2
from page_loader.parsing_cli import parsing_cli
from page_loader import download


def main():
    args = parsing_cli()
    file_path = download(args.URL, args.output)
    print(file_path)


if __name__ == '__main__':
    main()
