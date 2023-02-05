from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bookmaker.accounts.models import Account


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Extra Fields', {'fields': ('balance', )}),)


admin.site.register(Account, CustomUserAdmin)
