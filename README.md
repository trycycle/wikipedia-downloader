# wikipedia-downloader
Python scripts for downloading Wikipedia data dump files. You can download Wikipedia dump files listed in ```target.dat``` using ```download.py```.

# Requirements
* Python 3.X
* Python libraries
    * requests
    * tqdm

# How to use
```
usage: download.py [-h] [--lang LANG] [--savedir SAVEDIR]

optional arguments:
  -h, --help         show this help message and exit
  --lang LANG        target language for Wikipedia. Default value is 'ja'.
  --savedir SAVEDIR  directory for saving dump files. Default value is '.'
 ```
