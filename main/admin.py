from django.contrib import admin

from .models import News


# Модель товара
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'video', 'description', 'created', 'updated']


admin.site.register(News, NewsAdmin)
