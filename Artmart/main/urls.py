from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import search,artwork_detail,shop,main,artist_profile,artist,contact_view,register_view,login_view,my_account
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',main,name='main'),
    path('shop',shop,name='shop' ),
    path('artist',artist,name='artist' ),
    path('contact',contact_view,name='contact'),
    path('search/',search, name='search_results'),
    path('login/',login_view, name='login'),
    path('register/',register_view, name='register'),
    path('my-account/',my_account, name='my_account'),  # for "My Account" page
    path('artwork/<int:id>/',artwork_detail, name='artwork_detail'),
    path('artist_profile/<int:id>',artist_profile,name='artist_profile')
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)