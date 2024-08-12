from django.contrib import admin
from .models import *

admin.site.register(Userregister)

@admin.register(Contact)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'created_at')
    search_fields = ('name', 'email', 'number')
    list_filter = ('created_at',)
