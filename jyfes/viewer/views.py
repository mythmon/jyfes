import html5lib
import requests
import urllib.parse
from django.conf import settings
from django.shortcuts import render

from jyfes.lib.memoize import memoize


def list_view(request):
    return render(request, 'index.html', {
        'gifs': get_gifs(),
    })


class Gif(object):

    def __init__(self, url, title):
        self.url = url
        self.title = title

    @classmethod
    def from_url(cls, url):
        _, title = url.rsplit('/', 1)
        title = urllib.parse.unquote(title).rstrip('.gif')
        return cls(url, title)


@memoize(settings.SOURCE_CACHE_TIMEOUT)
def get_gifs():
    req = requests.get(settings.GIF_SOURCE)
    doc = html5lib.parse(req.text, namespaceHTMLElements=False)

    # Hackey, fragile way to pull all the links off a Apache index page.
    urls = [
        settings.GIF_SOURCE + '/' + tr[1][0].get('href')
        for tr in doc.find('body').find('table').find('tbody')[2:]
        if len(tr) > 1
    ]

    gifs = [Gif.from_url(url) for url in urls]

    return gifs
