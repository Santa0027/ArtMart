from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Artish, Artwork, Category
from django.db.models import Q
from .forms import ContactForm
from django.shortcuts import render, redirect

def get_filtered_artworks(request, artist=None):
    selected_categories = request.GET.getlist('category')
    sort_order = request.GET.get('sort')  # 'asc' or 'desc'

    # Start with all artworks
    artworks = Artwork.objects.all()

    # Filter by artist if artist is passed
    if artist:
        artworks = artworks.filter(artish=artist)

    # Filter by selected categories
    if selected_categories:
        artworks = artworks.filter(category__id__in=selected_categories)

    # Sort by artist name if sorting is requested
    if sort_order == 'asc':
        artworks = artworks.order_by('artish__name')
    elif sort_order == 'desc':
        artworks = artworks.order_by('-artish__name')

    return artworks, selected_categories



# Home page view
def main(request):
    artists = Artish.objects.all()
    artworks = Artwork.objects.all()
    categories = Category.objects.all()[:5]
    context = {
        'categories': categories,
        'artists': artists,
        'artworks': artworks
    }
    return render(request, 'main/main.html', context)

def shop(request):
    artworks, selected_categories = get_filtered_artworks(request)
    categories_list = Category.objects.all()
    
    paginator = Paginator(artworks, 6)  # Show 6 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'selected_categories': selected_categories,
        'Categorylist': categories_list,
        
    }
    return render(request, 'main/shop.html', context)

def get_artwork_by_artist(request, artist_id):
    # Fetch artworks by artist
    artworks = Artwork.objects.filter(artish__id=artist_id)
    
    # Get all categories for the category filter
    categories_list = Category.objects.all()

    # Paginator setup for artworks
    paginator = Paginator(artworks, 6)  # Show 6 artworks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'artworks': artworks,
        'Categorylist': categories_list,
        'page_obj': page_obj,
    }

    return render(request, 'main/shop.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # handle form data (send email or save to DB)
            print(form.cleaned_data)
            return redirect('contact')  # after submit
    else:
        form = ContactForm()
    
    return render(request, 'main/contact.html', {'form': form})

def get_artwork_by_category(request, category_id):  
    # Fetch artworks by category
    artworks = Artwork.objects.filter(category__id=category_id)
    
    # Get all categories for the category filter
    categories_list = Category.objects.all()

    # Paginator setup for artworks
    paginator = Paginator(artworks, 6)  # Show 6 artworks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'artworks': artworks,
        'Categorylist': categories_list,
        'page_obj': page_obj,
    }

    return render(request, 'main/shop.html', context)

# Artist profile view (can be extended to use artist_id later)
def artist_profile(request, id):
    # Fetch the artist by ID
    artist = get_object_or_404(Artish, id=id)

    # Get artworks associated with the artist
    artworks, selected_categories = get_filtered_artworks(request, artist)

    # Get all categories for the category filter
    categories_list = Category.objects.all()

    # Paginator setup for artworks
    paginator = Paginator(artworks, 6)  # Show 6 artworks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare the context with all the model elements
    context = {
        'artist': artist,  # Artist details
        'artworks': artworks,  # All artworks by this artist
        'selected_categories': selected_categories,  # Selected categories for filtering
        'Categorylist': categories_list,  # All categories for the category filter
        'page_obj': page_obj,  # Paginated artworks
    }

    return render(request, 'main/artist_profile.html', context)






# Artwork detail view
def artwork_detail(request, id):
    artwork = get_object_or_404(Artwork, id=id)
    
    return render(request, 'main/artwork_detail.html', {'artwork': artwork})







# Search view

def search(request):
    query = request.GET.get('q', '')
    selected_categories = request.GET.getlist('category')  # Handles multiple checkboxes

    artwork_results = Artwork.objects.all()

    if query:
        # Search in both artwork title and artist name
        artwork_results = artwork_results.filter(
            Q(title__icontains=query) |
            Q(artish__name__icontains=query)
        )

    if selected_categories:
        artwork_results = artwork_results.filter(category__id__in=selected_categories).distinct()

    paginator = Paginator(artwork_results, 6)  # Adjust number per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # For the sidebar
    category_list = Category.objects.all()

    # Optional: search for artist separately (e.g., for artist bio section)
    artist_result = Artish.objects.filter(name__icontains=query).first() if query else None

    context = {
        'artwork_results': page_obj.object_list,
        'page_obj': page_obj,
        'Categorylist': category_list,
        'selected_categories': selected_categories,
        'artist_result': artist_result,
    }

    return render(request, 'main/search_results.html', context)

def artist(request):
    artists = Artish.objects.all()
    paginator = Paginator(artists, 5)  # Fix: use `artists`, not `artist`
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'artist': page_obj.object_list,  # Optional: only current page's artists
    }
    return render(request, "main/artist.html", context)


def artists_list(request):
    # Fetch all artists (or filter as needed)
    artists = Artish.objects.all()[:5]
    categories = Category.objects.all()[:5]
    
    context = {
        'artist': artists,
        'categories': categories,
    }
    
    return render(request, 'nav.html', context)