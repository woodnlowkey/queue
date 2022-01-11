from django.contrib import admin
from .models import NewsData

# Register your models here.
class NewsDataAdmin(admin.ModelAdmin):
    search_fields = ['id', 'subject', 'content']

admin.site.register(NewsData, NewsDataAdmin)
