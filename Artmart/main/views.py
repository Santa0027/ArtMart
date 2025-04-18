from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Artish, Artwork, ArtworkImage



# Create your views here.


def main(request):
    return render(request,'main/main.html',)

def search(request):
    query = request.GET.get('q')
    artwork_results = []
    artish_results = []

    if query:
        artwork_results = Artwork.objects.filter(title__icontains=query)
        artish_results = Artish.objects.filter(name__icontains=query)

    return render(request, 'main/search_results.html', {
        'query': query,
        'artwork_results': artwork_results,
        'artish_results': artish_results    
    })
