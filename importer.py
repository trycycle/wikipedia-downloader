#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Yusuke Yamamoto
# Email: yusuke@hontolab.org
# URL: http://hontolab.org/
# Licence: MIT License

""" Wikipedia本文データXMLをMySQLデータベースにインポートするためのクラス
"""
import MySQLdb
import xml.etree.ElementTree as ET
from tqdm import tqdm

NAMESPACE = "{http://www.mediawiki.org/xml/export-0.10/}"


class WikipediaContentImporter(object):

    def __init__(self, host='localhost', port=3306, db='jawiki',
                 user='root', passwd='passwd', charset='utf8'):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset


    def __open_mysql_connection(self):
        self.connect = MySQLdb.connect(host=self.host,
                                       port=self.port,
                                       user=self.user,
                                       passwd=self.passwd,
                                       db=self.db, charset=self.charset)
        self.cursor = self.connect.cursor()


    def __close_mysql_connection(self):
        self.cursor.close()
        self.connect.close()


    def __insert_revision_record(self, page_id, rev_id):
        try:
            sql = "INSERT INTO {db}.revision (rev_id, rev_page, rev_text_id) VALUES (%s, %s, %s)".format(db=self.db)
            self.cursor.execute(sql, (rev_id, page_id, rev_id))
            self.connect.commit()
        except MySQLdb.IntegrityError:
            sql = "UPDATE {db}.revision SET rev_id = %s, rev_text_id = %s WHERE rev_page = %s".format(db=self.db)
            self.cursor.execute(sql, (rev_id, rev_id, page_id))
            self.connect.commit()


    def __insert_text_record(self, rev_id, content):
        try:
            sql = "INSERT INTO {db}.text (old_id, old_text, old_flags) VALUES (%s, %s, 'utf-8')".format(db=self.db)
            self.cursor.execute(sql, (rev_id, content))
            self.connect.commit()
        except MySQLdb.IntegrityError:
            sql = "UPDATE {db}.text SET old_text = %s WHERE old_id = %s".format(db=self.db)
            self.cursor.execute(sql, (content, rev_id))
            self.connect.commit()


    def __init_tables(self):
        sql = "TRUNCATE TABLE {db}.revision".format(db=self.db)
        self.cursor.execute(sql)
        self.connect.commit()

        sql = "TRUNCATE TABLE {db}.text".format(db=self.db)
        self.cursor.execute(sql)
        self.connect.commit()


    def __get_ns_value(self, xml_element):
        return int(xml_element.find("./{}ns".format(NAMESPACE)).text)


    def __get_page_id_value(self, xml_element):
        return int(xml_element.find("./{}id".format(NAMESPACE)).text)


    def __get_revision_id_value(self, xml_element):
        return int(xml_element.find("./{}revision/{}id".format(NAMESPACE, NAMESPACE)).text)


    def __get_text_value(self, xml_element):
        return xml_element.find("./{}revision/{}text".format(NAMESPACE, NAMESPACE)).text


    def __get_title_value(self, xml_element):
        return xml_element.find("./{}title".format(NAMESPACE)).text


    def import_page_article_xml_serially(self, file_path, extract_count=None, init_table=True):
        self.__open_mysql_connection()

        if init_table:
            # revisionテーブル, textテーブルを初期化する
            self.__init_tables()

        if not extract_count:
            sql = "SELECT COUNT(*) FROM {db}.page".format(db=self.db)
            self.cursor.execute(sql)
            extract_count = self.cursor.fetchone()[0]

        context = ET.iterparse(file_path, events=('start', 'end'))
        context = iter(context)
        _, root = next(context)

        progress_bar = tqdm(total=extract_count)
        itercount = 1
        for event, elem in context:
            if event == "end" and elem.tag == "{}page".format(NAMESPACE):
                ns = self.__get_ns_value(elem)
                if ns == 0:
                    page_id = self.__get_page_id_value(elem)
                    rev_id = self.__get_revision_id_value(elem)
                    text = self.__get_text_value(elem)
                    title = self.__get_title_value(elem)

                    # Insert data into MySQL tables
                    self.__insert_revision_record(page_id, rev_id)
                    self.__insert_text_record(rev_id, text)

                    if itercount >= extract_count:
                        break
                    else:
                        itercount += 1
                        progress_bar.update(1)

            # Free memory
            root.clear()

        # Close MySQL database connection
        self.__close_mysql_connection()

        # Close progress bar
        progress_bar.close()



if __name__ == '__main__':
    import fire
    #fire.Fire(WikipediaContentImporter)
    #python importer.py --db='ja_wikipedia' "data/ja_wikipedia.xml" --user='ja_wikipedia' --passwd='ja_wikipedia' import_article_xml_serially --file_path="data/ja_wikipedia.xml" --init_table=True
