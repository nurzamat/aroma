from django.contrib import admin

from .models import Node, Package, UserProfile, BonusType, BonusSettings

admin.site.register(Package)
admin.site.register(Node)
admin.site.register(UserProfile)
admin.site.register(BonusType)
admin.site.register(BonusSettings)






