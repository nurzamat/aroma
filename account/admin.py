from django.contrib import admin

from .models import Node, Package, UserProfile, BonusType, BonusSettings, PropertyValueSettings

admin.site.register(Package)
admin.site.register(Node)
admin.site.register(UserProfile)
admin.site.register(BonusType)
admin.site.register(BonusSettings)
admin.site.register(PropertyValueSettings)
# admin.site.register(Bonus)






