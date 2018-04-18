#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Yusuke Yamamoto
# Email: yusuke@hontolab.org
# URL: http://hontolab.org/
# Licence: MIT License
import argparse
from downloader import WikipediaDownloader

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--lang", type=str, help="target language for Wikipedia. Default value is 'ja'.")
    parser.add_argument("--savedir", type=str, help="directory for saving dump files. Default value is '.'")

    # 結果を受ける
    args = parser.parse_args()

    return(args)


def main():
    args = get_args()
    lang = args.lang
    data_dir = args.savedir

    if not lang:
        lang = "ja"

    if not data_dir:
        data_dir = "."

    w = WikipediaDownloader(data_dir=data_dir)
    w.download_latest_wikipedia_dump(lang)



if __name__ == '__main__':
    main()
