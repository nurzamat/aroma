from django.contrib import admin

from .models import Node, Package, UserProfile

admin.site.register(Package)
admin.site.register(Node)
admin.site.register(UserProfile)






