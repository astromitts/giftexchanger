from django.contrib import admin
from giftexchanger.models.app import GiftExchange, UserProfile, UserDetails
# Register your models here.

admin.site.register(GiftExchange)
admin.site.register(UserProfile)
admin.site.register(UserDetails)
