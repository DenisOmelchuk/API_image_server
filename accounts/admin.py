from django.contrib import admin

from .models import CustomUser, AccountTier, ThumbnailHeight, UserImage, ExpiringLink

admin.site.register(CustomUser)
admin.site.register(AccountTier)
admin.site.register(ThumbnailHeight)
admin.site.register(UserImage)
admin.site.register(ExpiringLink)
