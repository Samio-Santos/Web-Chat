from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import ProfileUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

class ProfileUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ProfileUser

class ProfileUserAdmin(UserAdmin):
    form = ProfileUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('imagem', 'token', 'is_online')}),
    )

admin.site.register(ProfileUser, ProfileUserAdmin)