import subprocess
import requests
from bs4 import BeautifulSoup
import os
import argparse

BASE_URL = "https://www.pbs.org/wgbh/frontline/films/"

def get_num_pages(base_url):
    result_content = requests.get(base_url).text
    soup = BeautifulSoup(result_content, features='lxml')
    pagination_elems = soup.find_all("div", {"class": "pagination__page"})
    return len(pagination_elems) - 2

def get_season_and_episode(film_url):
    result_content = requests.get(film_url).text
    soup = BeautifulSoup(result_content, features='lxml')
    header_elem = soup.find(id="film-season-episode")
    season, episode = header_elem.text.replace("Season ", "").replace(" Episode ", "").split(":")
    return season, episode

def get_film_links(base_url):
    num_pages = get_num_pages(base_url)
    for page in range(0, num_pages + 1):
        result_content = requests.get(f"{base_url}page/{page}").text
        soup = BeautifulSoup(result_content, features='lxml')
        film_blocks = soup.find_all("div", {"class": "list__item"})
        for film_block in film_blocks:
            try:
                url_item = film_block.find_all("a", {"class": "black-playhead-outer"})[0]
            except IndexError:
                continue
            url = url_item['href']
            title = url_item.text
            season, episode = get_season_and_episode(url)
            
            yield (
                title,
                url,
                season,
                episode
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('root_dir', metavar='root_dir', type=str, help='root dir where to store videos')
    args = parser.parse_args()
    errors_file = open('errors.log', 'w')
    film_links = get_film_links(BASE_URL)
    for title, url, season, episode in film_links:
        season_folder = os.path.join(args.root_dir, "Season " + season)
        output_file_name = f"{season_folder}/Frontline - S{season}E{episode:0>2} - {title}.mp4"
        print(season, episode, title, output_file_name, url)
        if not os.path.exists(season_folder):
            os.makedirs(season_folder)
        command = ["youtube-dl", "-o", output_file_name, url]
        result = subprocess.run(command)
        try:
            result.check_returncode()
        except:
            errors_file.write(f'ERROR: {season} {episode} {title} {url}')
    errors_file.close()
