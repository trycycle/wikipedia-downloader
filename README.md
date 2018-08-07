# wikipedia-downloader
Python scripts for downloading Wikipedia data dump files. You can download Wikipedia dump files listed in ```target.dat``` using ```manipulate.py```.

Also, you can parse a XML article dump file (that is, ```pages-articles.xml```) and import it into your MySQL database, using ```manipulate.py```.

# Requirements
* Python 3.X
* Python libraries
    * requests
    * click
    * tqdm

# How to use
## Download Wikipedia dump files
```
Usage: manipulate.py download [OPTIONS] [__DATA_DIR]

  This script downloads Wikipedia data dump files. You can download the
  files listed in target.dat into the directory DATA_DIR.

Options:
  --lang [ja|en|de|fr|zh|pl|pt|it|ru|es]
                                  target language for Wikipedia. Default value
                                  is 'ja'.
  --help                          Show this message and exit.
  ```

## Parse a XML articile dump file and import it into MySQL
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
