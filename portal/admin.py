from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'category', 'status', 'anonymous', 'created_at')
    list_filter = ('status', 'category', 'anonymous')
    search_fields = ('subject', 'description', 'name', 'email')
    ordering = ('-created_at',)
