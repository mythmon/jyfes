import html5lib
import requests
from django.shortcuts import render


GIF_SOURCE = 'http://gifs.elijahcaine.me/'


def list_view(request):
    return render(request, 'index.html', {
        'gifs': get_gifs(),
    })


def get_gifs():
    req = requests.get(GIF_SOURCE)
    doc = html5lib.parse(req.text, namespaceHTMLElements=False)

    # Hackey, fragile way to pull all the links off a Apache index page.
    urls = [
        GIF_SOURCE + '/' + tr[1][0].get('href')
        for tr in doc.find('body').find('table').find('tbody')[2:]
        if len(tr) > 1
    ]

    return urls
