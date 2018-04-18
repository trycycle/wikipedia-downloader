#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Yusuke Yamamoto
# Email: yusuke@hontolab.org
# URL: http://hontolab.org/
# Licence: MIT License
import os
import datetime
import requests
from tqdm import tqdm

DOMAIN = "https://dumps.wikimedia.org"


class WikipediaDownloader(object):

    def __init__(self, data_dir="."):
        self.data_dir = data_dir


    def download_latest_wikipedia_dump(self, lang="ja"):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_dir = os.path.join(self.data_dir, lang, now)
        os.makedirs(save_dir)

        with open("list.dat") as f:
            for line in f:
                _filename = line.strip()
                filename = "{0}wiki-latest-{1}".format(lang, _filename)
                self.__download(filename, save_dir, lang)


    def __download(self, filename, save_dir, lang):
        url = "{domain}/{lang}wiki/latest/{filename}".format(domain=DOMAIN,
                                                             lang=lang,
                                                             filename=filename)
        save_file_path = os.path.join(save_dir, filename)
        print(url)

        file_size = int(requests.head(url).headers["content-length"])
        response = requests.get(url, stream=True)
        with tqdm(total=file_size, unit="B", unit_scale=True) as pbar:
            with open(save_file_path, 'wb') as save_file:
                for chunk in response.iter_content(chunk_size=1024):
                    save_file.write(chunk)
                    pbar.update(len(chunk))
