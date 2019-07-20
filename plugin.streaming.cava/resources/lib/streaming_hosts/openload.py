from bs4 import BeautifulSoup
import re
import json
import requests

def __get_embedded_openload_url(url):
    """
    url example:
    https://openloads.co/c2/m2ZUtv0ylvY/filename.mp4

    """

    url = url.replace(' ', '')
    embed_url = "https://openload.co/embed/{0}"

    try:
        media_id = url.split('/')[4]
        r = requests.get(embed_url.format(media_id))
        if (r.status_code == 200):
                return embed_url.format(media_id)
    except:
        return False

def __rapidcrypt_scraper(url):
    try:
        url = url.replace(' ', '')
        s = requests.Session()
        r = s.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            openload_tag = soup.find('a', href=True).get('href')
            return openload_tag
    except:
            return False

def get_openload(url):
    openload_url = __rapidcrypt_scraper(url)
    if openload_url:
        embedded_openload_url = __get_embedded_openload_url(openload_url)

    return embedded_openload_url