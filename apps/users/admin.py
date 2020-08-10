from django.contrib import admin

from apps.users.models import CustomUser

from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone', 'secret_key', 'date_joined', 'is_active', 'confirm')
    readonly_fields = ('date_joined',)
    list_display_links = ('email', 'phone', 'secret_key',)
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'phone')}),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions', 'confirm'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
