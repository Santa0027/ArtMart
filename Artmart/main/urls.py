from django.urls import path,include
from .views import main,search

urlpatterns=[
    path('',main,name='main' ),
    path('search/',search, name='search_results'),
    # path('art/',artwork, name='artwork'),
]