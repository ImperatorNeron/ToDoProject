from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import SignUpForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = SignUpForm
    # Виділяємо поля під окрему категорію
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'More information about user',
            {
                'fields': (
                    'phone', 'bio', 'photo', 'score', 'slug'
                )
            }
        )
    )


class TaskAdminSettings(admin.ModelAdmin):
    list_display = ('user', 'title', 'complete', 'to_do_date')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_editable = ('complete',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task, TaskAdminSettings)
admin.site.register(SiteImages)
