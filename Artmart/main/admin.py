from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Artish, Category, Artwork, ArtworkImage, Review


# Inline for multiple images inside Artwork
class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 1


@admin.register(Artish)
class ArtishAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'gender', 'created_at', 'edit_link']
    search_fields = ['name', 'email', 'stage_name']
    list_filter = ['gender', 'created_at']

    def edit_link(self, obj):
        url = reverse("admin:main_artish_change", args=[obj.id])
        return format_html('<a class="button" href="{}">✏️ Edit</a>', url)

    edit_link.short_description = 'Edit'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'edit_link']
    list_editable = ['is_active']
    search_fields = ['name']
    list_filter = ['is_active']
    readonly_fields = ['created_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'image', 'is_active')
        }),
        ("Timestamps", {
            'fields': ('created_at',)
        }),
    )

    def edit_link(self, obj):
        url = reverse("admin:main_category_change", args=[obj.id])
        return format_html('<a class="button" href="{}">✏️ Edit</a>', url)

    edit_link.short_description = 'Edit'


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'artish', 'category', 'price', 'stock', 'is_available', 'edit_link']
    # list_editable = ['price', 'stock', 'is_available']
    search_fields = ['title', 'artish__name']
    list_filter = ['category', 'style', 'medium', 'is_available']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ArtworkImageInline]

    fieldsets = (
        ("Basic Info", {
            'fields': ('title', 'artish', 'category', 'description', 'image')
        }),
        ("Artwork Details", {
            'fields': ('style', 'medium', 'year_created', 'width', 'height')
        }),
        ("Pricing & Stock", {
            'fields': ('price', 'discount_price', 'stock', 'is_available')
        }),
        ("Performance", {
            'fields': ('views', 'likes')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def edit_link(self, obj):
        url = reverse("admin:main_artwork_change", args=[obj.id])
        return format_html('<a class="button" href="{}">✏️ Edit</a>', url)

    edit_link.short_description = 'Edit'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['artwork', 'user', 'rating', 'created_at', 'edit_link']
    search_fields = ['artwork__title', 'user__username']
    list_filter = ['rating', 'created_at']
    readonly_fields = ['created_at']

    def edit_link(self, obj):
        url = reverse("admin:main_review_change", args=[obj.id])
        return format_html('<a class="button" href="{}">✏️ Edit</a>', url)

    edit_link.short_description = 'Edit'
    # 