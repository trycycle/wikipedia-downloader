#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Yusuke Yamamoto
# Email: yusuke@hontolab.org
# URL: http://hontolab.org/
# Licence: MIT License

""" Wikipediaのコンテンツをダウンロードもしくはパースするためのコマンド
"""
import click
from downloader import WikipediaDownloader
from importer import WikipediaContentImporter

LANGUAGES = ['ja', 'en', 'de', 'fr', 'zh', 'pl', 'pt', 'it', 'ru', 'es']


@click.group()
def cmd():
    pass

@cmd.command()
@click.argument('data_dir', type=str, default=".")
@click.option('--lang', type=click.Choice(LANGUAGES), default="ja", help="target language for Wikipedia. Default value is 'ja'.")
def download(lang, data_dir):
    """ This script downloads Wikipedia data dump files. You can download the files listed in target.dat into the directory DATA_DIR.
    """
    w = WikipediaDownloader(data_dir=data_dir)
    w.download_latest_wikipedia_dump(lang)


@cmd.command()
@click.argument('file_path')
@click.option('--extract_count', type=int, default=None, help="number of articles of which XML content will be imported. If not specified, all articiles will be imported.")
@click.option('--db_host', default="localhost", help="MySQL host name (default: localhost).")
@click.option('--db_port', default=3306, help="MySQL port number (default: 3306).")
@click.option('--db_name', default="ja_wikipedia", help="MySQL database name. Dafault value is ja_wikipedia.")
@click.option('--db_user', default="ja_wikipedia", help="MySQL user name (default: ja_wikipedia).")
@click.option('--db_passwd', default="ja_wikipedia", help="MySQL user password (default: ja_wikipedia).")
@click.option('--db_charset', default="utf8", help="character code on MySQL (default: utf8).")
def import_page_article_xml(file_path, extract_count, db_host, db_port, db_name, db_user, db_passwd, db_charset):
    """ This script parses a page article XML file on FILE_PATH and import it into a MySQL database.
    """
    w = WikipediaContentImporter(db_host, db_port, db_name,
                                 db_user, db_passwd, db_charset)
    w.import_page_article_xml_serially(file_path, extract_count)


def main():
    cmd()


if __name__ == '__main__':
    main()
