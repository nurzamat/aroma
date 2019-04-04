from django.contrib import admin

from .models import News , Testimonials


# Модель товара
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'video', 'description', 'created', 'updated']

class TestimAdmin(admin.ModelAdmin):
    list_display = ['name', 'profession', 'text']


admin.site.register(News, NewsAdmin)
admin.site.register(Testimonials, TestimAdmin)