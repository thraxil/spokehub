# utility functions for scraping instagram hashtag page
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from datetime import datetime
from django.utils.encoding import smart_str


def get_script(text):
    soup = BeautifulSoup(text, "lxml")
    for s in soup('script'):
        contents = s.string
        if not contents:
            continue
        if contents.startswith('window._sharedData'):
            return contents
    return None


def parse_json(script):
    # there's an assignment and a semicolon to get rid of
    blob = script[len('window._sharedData = '):-1]
    return json.loads(smart_str(blob))


def entries(d):
    top = d['entry_data']['TagPage'][0]
    if 'graphql' in top.keys():
        graphql = d['entry_data']['TagPage'][0]['graphql']
        return graphql['hashtag']['edge_hashtag_to_media']['edges']
    return d['entry_data']['TagPage'][0]['tag']['media']['nodes']


def user_page_entries(d):
    return d['entry_data']['ProfilePage'][0][
        'graphql']['user']['edge_owner_to_timeline_media']['edges']


def owner(d):
    return d['entry_data']['PostPage'][0]['graphql'][
        'shortcode_media']['owner']


def clean_url(url):
    """ remove the 'ig_cache_key' param """
    o = urlsplit(url)
    return "{scheme}://{netloc}{path}".format(
        scheme=o[0], netloc=o[1], path=o[2],
    )


class Entry(object):
    def __init__(self, d, graphql=False):
        if graphql:
            edges = d['edge_media_to_caption']['edges']
            if len(edges) > 0:
                self.caption = edges[0]['node']['text']
            else:
                self.caption = ""
            self.code = d['shortcode']
            self.date = datetime.fromtimestamp(int(d['taken_at_timestamp']))
            self.display_src = d['display_url']
        else:
            self.caption = d.get('caption', '')
            self.code = d['code']
            self.date = datetime.fromtimestamp(int(d['date']))
            self.display_src = d['display_src']
        self.id = d['id']
        self.is_video = d['is_video']
        self.owner = d['owner']['id']
        self.thumbnail_src = d['thumbnail_src']
        self._username = None
        self._fullname = None
        self.type = "image"

    def url(self):
        return "https://www.instagram.com/p/{}/".format(self.code)

    def clean_display_src(self):
        return clean_url(self.display_src)

    def clean_thumbnail_src(self):
        return clean_url(self.thumbnail_src)

    def populate_owner(self):
        r = requests.get(self.url())
        script = get_script(r.text)
        d = parse_json(script)
        owner_data = owner(d)
        self._username = owner_data['username']
        self._fullname = owner_data['full_name']

    def username(self):
        if self._username is None:
            self.populate_owner()
        return self._username

    def fullname(self):
        if self._fullname is None:
            self.populate_owner()
        return self._fullname
