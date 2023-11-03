from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import os
from .functions import get_upload_path
from django.dispatch import receiver
from django.db.models.signals import pre_save
from PIL import Image
from .validators import validate_time_to_expired
from django.utils import timezone
import time
# from images.models import ThumbnailSize


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    account_tier = models.ForeignKey(
        'AccountTier',
        on_delete=models.SET_NULL,
        null=True, blank= True
    )
    test = models.CharField(max_length=20, null=True, blank=True)
    # slug = models.SlugField(default=None, blank=True, null=True)


class ThumbnailHeight(models.Model):

    height = models.IntegerField()

    def __str__(self):
        return f'{self.height}'

class AccountTier(models.Model):
    tier_name = models.CharField(max_length=64)
    thumbnail_height = models.ManyToManyField(ThumbnailHeight)

    is_original_file = models.BooleanField(
        default=False,
        verbose_name='Original file')
    is_expiring_link = models.BooleanField(
        default=False,
        verbose_name='Expiring link')

    def __str__(self):
        return f'{self.tier_name}'


# add params to func
class UserImage(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        default = None,
        related_name='images'
    )
    image_name = models.CharField(max_length=50, null=True, blank=True)
    image_extension = models.CharField(max_length=5, null=True, blank=True)
    original_image = models.ImageField(upload_to='images')
    thumbnail_px_200 = models.ImageField(upload_to='images', blank=True, null=True)
    thumbnail_px_400 = models.ImageField(upload_to='images', blank=True, null=True)
    test = models.CharField(max_length=20, null=True, blank=True)

    def get_field_by_name(self, field_name):
        try:
            return getattr(self, field_name)
        except AttributeError:
            return None

    def get_links(self, request):
        user_id = self.user.id
        user_tier = self.user.account_tier
        user_tier_thumbnail_heights = self.user.account_tier.thumbnail_height.all()
        base_file = os.path.dirname(self.original_image.name)
        base_url = request.build_absolute_uri('get_image/')
        base_url = base_url + str(user_id) + '/' + str(self.id) + '/'
        links_for_user = {}
        if user_tier.is_original_file:
            links_for_user['original_image'] = base_url + 'original_image/'
        for thumbnail_height in user_tier_thumbnail_heights:
            links_for_user_key = 'tumbnail'+str(thumbnail_height)
            links_for_user[links_for_user_key] = base_url + str(thumbnail_height)
        return links_for_user



class ExpiringLink(models.Model):
    image = models.OneToOneField(UserImage, on_delete=models.CASCADE, unique=True, related_name='expiring_link', blank=True, null=True)
    time_to_expired = models.IntegerField(validators=[validate_time_to_expired], blank=True, null=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)
    link = models.URLField(blank=True, null=True)

    def is_expired(self):
        current_time = time.time()
        created_at_timestamp = self.created_at.timestamp()
        time_difference = current_time - created_at_timestamp
        return self.time_to_expired < time_difference

#
# @receiver(pre_save, sender=UserImage)
# def create_thumbnails(sender, instance, *args, **kwargs):
#     image_name, image_extension = os.path.splitext(os.path.basename(instance.original_image.name))
#     instance.image_name = image_name
#     instance.image_extension = image_extension
#     user_tier_thumbnail_heights = instance.user.account_tier.thumbnail_height.all()
#     for thumb_height in user_tier_thumbnail_heights:
#         field_name = 'thumbnail_px_' + str(thumb_height)
#         if not instance.get_field_by_name(field_name):
#             original_image = Image.open(instance.original_image)
#             size_of_original_image = original_image.size
#             resizing_ratio = size_of_original_image[1] / thumb_height.height
#             thumbnail = original_image.resize((int(size_of_original_image[0]/resizing_ratio), thumb_height.height))
#
#             # Thumbnail_path presents the location for model field
#             # full_thumbnail_path is only for storing thumbnail inside of media directory and it's not used further
#             thumbnail_path = 'images/' + image_name + '_thumbnail' + str(thumb_height) + image_extension
#             full_thumbnail_path = 'media/' + thumbnail_path
#             thumbnail.save(full_thumbnail_path)
#             setattr(instance, field_name, thumbnail_path)

