from django.shortcuts import render


def list_view(request):
    gifs = ['http://gifs.elijahcaine.me/dojo.gif']
    return render(request, 'index.html', {'gifs': gifs})
