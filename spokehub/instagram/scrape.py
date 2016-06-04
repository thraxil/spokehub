# utility functions for scraping instagram hashtag page
import json
import requests
from BeautifulSoup import BeautifulSoup
from urlparse import urlsplit
from datetime import datetime
from django.utils.encoding import smart_str


def get_script(text):
    soup = BeautifulSoup(text)
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
    return d['entry_data']['TagPage'][0]['tag']['media']['nodes']


def owner(d):
    return d['entry_data']['PostPage'][0]['media']['owner']


def clean_url(url):
    """ remove the 'ig_cache_key' param """
    o = urlsplit(url)
    return "{scheme}://{netloc}{path}".format(
        scheme=o[0], netloc=o[1], path=o[2],
    )


class Entry(object):
    def __init__(self, d):
        self.caption = d['caption']
        self.code = d['code']
        self.comments = d['comments']
        self.date = datetime.fromtimestamp(int(d['date']))
        self.dimensions = d['dimensions']
        self.display_src = d['display_src']
        self.id = d['id']
        self.is_video = d['is_video']
        self.likes = d['likes']
        self.owner = d['owner']['id']
        self.thumbnail_src = d['thumbnail_src']
        self._username = None
        self._fullname = None

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
