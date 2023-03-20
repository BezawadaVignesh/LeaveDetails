from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, CLS, CCLS, SLS


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'sid', 'is_staff', 'is_active',)
    list_filter = ('sid', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'sid', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions',)
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'sid', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('sid', 'email',)
    ordering = ('sid', 'email',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(CLS)
admin.site.register(CCLS)
admin.site.register(SLS)
