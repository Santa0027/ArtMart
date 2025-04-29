from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Artish, Artwork, Category
from django.db.models import Q
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required



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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return render(request, 'main/login.html', {
                'login_error': 'Username and password are required.'
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:  # Ensure the user account is active
                login(request, user)
                return redirect('my_account')  # or wherever you want to send after login
            else:
                return render(request, 'main/login.html', {
                    'login_error': 'Your account is inactive. Please contact support.'
                })
        else:
            return render(request, 'main/login.html', {
                'login_error': 'Invalid username or password.'
            })
    else:
        return render(request, 'main/login.html')


# Registration View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'main/register.html', {
                'register_error': 'Username already exists.'
            })
        if User.objects.filter(email=email).exists():
            return render(request, 'main/register.html', {
                'register_error': 'Email already registered.'
            })

        # Create user with is_active=False
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # Mark user as inactive until approved
        user.save()

        return render(request, 'main/register.html', {
            'register_success': 'Registration submitted. Wait for admin approval.'
        })
    else:
        return render(request, 'main/register.html')
# User's Account Page
def my_account(request):
    return render(request, 'main/account.html')
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
            # Extract data
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Create email content
            subject = f"New Contact Form Submission from {first_name}"
            message_body = f"Name: {first_name}\nEmail: {email}\n\nMessage:\n{message}"

            # Send email
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,  # From email
                [settings.CONTACT_RECEIVER_EMAIL],  # To email (you)
                fail_silently=False,
            )

            return redirect('contact')  # After submit
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