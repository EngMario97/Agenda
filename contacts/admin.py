from django.contrib import admin
from .models import Category, Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname', 'telephone', 'email', 'created_at', 'category', 'show')
    list_display_links = ('id', 'name', 'lastname')
    # list_filter = ('name', 'lastname')
    list_per_page = 10
    search_fields = ('name', 'lastname', 'telephone')
    list_editable = ('telephone', 'show')


admin.site.register(Category)
admin.site.register(Contact, ContactAdmin)
