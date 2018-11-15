# Wikipedia downloader & importer
Python scripts for downloading Wikipedia data dump files. You can download Wikipedia dump files listed in `target.dat` using `manipulate.py`.

Also, you can parse a XML article dump file (that is, `pages-articles.xml`) and import it into your MySQL database, using `manipulate.py`.

# Requirements
* Python 3.X
* Python libraries
    * requests
    * mysqlclient
    * click
    * tqdm

# How to use
## Download Wikipedia dump files
1. Download all files in this repository
2. Install python libraries specified in `requirements.txt`
3. Make a directory (DATA_DIR) to download Wikipedia dump files.
4. Specifiy and confirm the files which you want to download in `target.dat`
5. Run `manipulate.py`. The following description is about how to use `manipulate.py` for downloading Wikipedia dump files. For example, if you want to download Japanese Wikipedia dump files into DATA_DIR directory, run the command `python manipulate.py download --lang ja DATA_DIR`.

```
Usage: manipulate.py download [OPTIONS] [DATA_DIR]

  This script downloads Wikipedia data dump files. You can download the
  files listed in target.dat into the directory DATA_DIR.

Options:
  --lang [ja|en|de|fr|zh|pl|pt|it|ru|es]
                                  target language for Wikipedia. Default value
                                  is 'ja'.
  --help                          Show this message and exit.
  ```

## Import Wikipedia dump files (SQL files)
Modify and run `import_sql.sh` in the `misc` directory.

## Parse a XML article dump file and import it into MySQL
1. Before running a script, download a table structure file from [here](https://github.com/wikimedia/mediawiki/blob/master/maintenance/tables.sql). Then, create tables on your MySQL database.
2. Run `manipulate.py` by following the below description. For example, image that you want to import a XML article dump file (data_dir/pages-articles.xml.bz2) into your MySQL database (hostname:localhost, port:3306, user:ja_wikipedia, password:ja_wikipedia, charset: utf8). Then, run the command `python manipulate.py import_page_article_xml --db_host localhost --db_port 3306 --db_user ja_wikipedia --db_password ja_wikipedia --db_charset utf8 data_dir/pages-articles.xml.bz2`.

```
Usage: manipulate.py import_page_article_xml [OPTIONS] FILE_PATH

  This script parses a page article XML file on FILE_PATH and import it into
  a MySQL database.

Options:
  --extract_count INTEGER  number of articles of which XML content will be
                           imported. If not specified, all articiles will be
                           imported.
  --db_host TEXT           MySQL host name (default: localhost).
  --db_port INTEGER        MySQL port number (default: 3306).
  --db_name TEXT           MySQL database name. Dafault value is ja_wikipedia.
  --db_user TEXT           MySQL user name (default: ja_wikipedia).
  --db_passwd TEXT         MySQL user password (default: ja_wikipedia).
  --db_charset TEXT        character code on MySQL (default: utf8).
  --help                   Show this message and exit.
```
