from django.contrib import admin
from .models import User, Profile, FailedLoginAttempt
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):

    list_display = ('email', 'id', 'first_name', 'last_name', 'phone', 'is_staff',  'is_superuser', 'is_locked', 'is_active')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_active', 'is_superuser', 'password', 'is_locked')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('first_name', 'last_name', 'phone')
    ordering = ('email',)
    filter_horizontal = ()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_at', 'is_on_email_list')
    readonly_fields = ('owner', 'created_at',)
    fieldsets = (
        ('Profile', {
            "fields": (
                'owner',
            ),
        }),
        ('Personal Info', {
            "fields": (
                'experience',
                'is_on_email_list',
                'created_at',
            ),
        }),
    )

class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempted_owner', 'attempted_at')
    readonly_fields = ('attempted_owner', 'attempted_at')
    fieldsets = (
        ('Attempt Info', {
            "fields": (
                'attempted_owner',
                'attempted_at',
            ),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(FailedLoginAttempt, FailedLoginAttemptAdmin)

