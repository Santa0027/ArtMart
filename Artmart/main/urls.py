from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import search,artwork_detail,shop,main

urlpatterns=[
    path('',main,name='main'),
    path('shop',shop,name='shop' ),
    path('search/',search, name='search_results'),
    path('artwork/<int:id>/',artwork_detail, name='artwork_detail'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)