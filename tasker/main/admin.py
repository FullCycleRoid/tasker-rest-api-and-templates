from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import MainTaskBoard, TaskInfo, Mark, AdvancedUser


class AdvancedUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = AdvancedUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'profile_image', 'board')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff',
                       'is_active', 'name', 'profile_image', 'board')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(MainTaskBoard)
admin.site.register(TaskInfo)
admin.site.register(Mark)
admin.site.register(AdvancedUser, AdvancedUserAdmin)
admin.site.unregister(Group)
