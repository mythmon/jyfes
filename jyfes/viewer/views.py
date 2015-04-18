import html5lib
import requests
from django.conf import settings
from django.shortcuts import render

from jyfes.lib.memoize import memoize


def list_view(request):
    return render(request, 'index.html', {
        'gifs': get_gifs(),
    })


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

    return urls
