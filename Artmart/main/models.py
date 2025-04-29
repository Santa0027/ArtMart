from django.db import models
from django.contrib.auth.models import User  # for review system
from django.urls import reverse

class PendingUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Store raw password temporarily
    is_approved = models.BooleanField(default=False)  # Pending approval
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username





# -----------------------
# Artist Model
# -----------------------
class Artish(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=100)
    stage_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    profile_image = models.ImageField(upload_to='artish/profile/', blank=True, null=True)
    bio = models.TextField(blank=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    portfolio_website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('artist_profile', args=[str(self.id)])

    def __str__(self):
        return self.name


# -----------------------
# Category Model
# -----------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category/images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# -----------------------
# Artwork / Product Model
# -----------------------
class Artwork(models.Model):
    STYLE_CHOICES = [
        ('abstract', 'Abstract'),
        ('realism', 'Realism'),
        ('surrealism', 'Surrealism'),
        ('modern', 'Modern'),
        ('traditional', 'Traditional'),
        ('pop', 'Pop Art'),
    ]

    MEDIUM_CHOICES = [
        ('oil', 'Oil'),
        ('acrylic', 'Acrylic'),
        ('watercolor', 'Watercolor'),
        ('digital', 'Digital'),
        ('ink', 'Ink'),
        ('mixed', 'Mixed Media'),
    ]

    title = models.CharField(max_length=150)
    artish = models.ForeignKey(Artish, on_delete=models.CASCADE, related_name='artworks')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='artworks')

    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='artworks/cover/', blank=True, null=True)

    style = models.CharField(max_length=100, choices=STYLE_CHOICES, blank=True, null=True)
    medium = models.CharField(max_length=100, choices=MEDIUM_CHOICES, blank=True, null=True)
    year_created = models.PositiveIntegerField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)

    width = models.DecimalField(max_digits=6, decimal_places=2, help_text="in inches", blank=True, null=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, help_text="in inches", blank=True, null=True)

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return reverse('artwork_detail', args=[str(self.id)])

    def __str__(self):
        return self.title


# -----------------------
# Artwork Multiple Images
# -----------------------
class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='artworks/gallery/')

    def __str__(self):
        return f"Image for {self.artwork.title}"


# -----------------------
# Optional: Reviews
# -----------------------
class Review(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.artwork.title}"
