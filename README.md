# PBS Frontline Downloader

This is script that lets you download all PBS Frontline Films available at https://www.pbs.org/wgbh/frontline/films/

## System Requirements

- ffmpeg:
    - `sudo apt install ffmpeg`
- youtube-dl:
    - `sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl`
    - `sudo chmod a+rx /usr/local/bin/youtube-dl`

## Python Requirements

- pip:
    - `pip install requests lxml bs4`
- conda:
    - `conda install requests lxml bs4`

## Run

`python3 pbs_downloader.py`