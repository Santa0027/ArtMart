import os

from .models import Artish, Category
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404



def header_artists(request):
    artists = Artish.objects.all()[:6]  # Limit for mega menu
    return {'header_artists': artists}