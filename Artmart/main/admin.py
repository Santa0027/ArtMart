from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Artish, Category, Artwork, ArtworkImage, Review,PendingUser
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

@admin.register(PendingUser)
class PendingUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_approved', 'created_at')
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        for user in queryset:
            if user.is_approved:
                # Check if user already exists to avoid duplicates
                if not User.objects.filter(username=user.username).exists():
                    # Create a new user, hash the password before saving
                    password = make_password(user.password)  # Hash the password
                    new_user = User.objects.create_user(
                        username=user.username,
                        email=user.email,
                        password=password
                    )
                    new_user.save()

                    # Send email notification to the newly created user
                    send_mail(
                        'Your account has been approved!',
                        f'Hello {user.username},\n\nYour account has been approved. You can now log in.',
                        'admin@example.com',  # Sender email (update this)
                        [user.email],  # Recipient email
                        fail_silently=False,
                    )

                    # After creating the user, delete the pending user from PendingUser table
                    user.delete()

                    self.message_user(request, f'User {user.username} has been approved and created successfully.', level='success')
                else:
                    self.message_user(request, f'Username {user.username} already exists.', level='error')
            else:
                self.message_user(request, f'User {user.username} is not approved yet.', level='error')

    approve_users.short_description = 'Approve selected users'
# Inline for multiple images inside Artwork
class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 1


@admin.register(Artish)
class ArtishAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','profile_image', 'phone', 'gender', 'created_at', 'edit_link']
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
    list_display = ['title', 'artish','image', 'category', 'price', 'stock', 'is_available', 'edit_link']
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