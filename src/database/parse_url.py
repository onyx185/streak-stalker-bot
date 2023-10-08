import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def parse_hashtags(msg: str) -> list:
    tags = re.findall(r'#\w+', msg)
    return tags


def parse_urls(msg):
    urls = re.findall(r"https?://\S+", msg)
    return urls

def find_social_media(url: str) -> str:
    url_obj = urlparse(url)

    if 'linkedin' in url_obj.hostname:
        return 'linkedin'
    elif 'instagram' in url_obj.hostname:
        return 'instagram'
    elif 'twitter' in url_obj.hostname:
        return 'twitter'
    elif 'facebook' in url_obj.hostname:
        return 'facebook'

    return "none"

def parse_linkdein_url(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')

    tab_title = soup.title.string
    data = {}

    try:
        data['name'] = tab_title.split('on')[0].strip()
    except IndexError:
        data['name'] = "None"

    data['hashtags'] = parse_hashtags(tab_title)

    return data



