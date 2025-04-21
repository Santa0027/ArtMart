from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Artish, Artwork, ArtworkImage,Category
from django.core.paginator import Paginator

# Create your views here.
# # Create your views here.


def main(request):
    
    
    selected_categories = request.GET.getlist('category')
    sort_order = request.GET.get('sort')  # 'asc' or 'desc'
    artworks = Artwork.objects.all()
    
    if selected_categories:
        artworks = artworks.filter(category__id__in=selected_categories)

    # if sort_order == 'asc':
    #     artworks = Artwork.objects.all().order_by('artish__name')
    # elif sort_order == 'desc':
    #     artworks = Artwork.objects.all().order_by('-artish__name')
    # else:
    #     artworks = Artwork.objects.all().order_by('-id')  # default sorting (latest first)


    categories_list = Category.objects.all()
    paginator = Paginator(artworks, 6)  # Show 10 artworks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'selected_categories': selected_categories,
        'request': request,
        'Categorylist':categories_list,
        'page_obj': page_obj,
    }
    return render(request, 'main/main.html', context)



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




# def artwork(request):
#     first_10_artworks = Artwork.objects.all()[:10]
#     context = {
#         'artworks': first_10_artworks,
#     }
#     print(f"Context being passed to the template: {context}")
#     return render(request, 'main/main.html', context)
