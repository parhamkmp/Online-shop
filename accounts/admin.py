from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number', 'role')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional information', {
            'fields': ('phone_number', 'address', 'image_profile', 'role'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional information', {
            'fields': ('phone_number', 'address', 'image_profile', 'role'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
