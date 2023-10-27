from django.dispatch import receiver
from django.db.models.signals import post_migrate, post_save, pre_save
from .models import AccountTier, UserImage, ThumbnailHeight
from .builtin_account_tiers_data import builtin_account_tiers


@receiver(post_migrate)
def create_builtin_tiers(sender, **kwargs):
    """Creates built-in tiers after db migration."""
    # Checks if builtin tier with the name 'Basic" exists in the database to prevent
    # duplicating the creation of account tiers
    if sender.name == 'accounts':
        if AccountTier.objects.only('tier_name').filter(tier_name='Basic').exists():
            return

        # basic account tier
        basic_account_tier = AccountTier.objects.create(
            tier_name='Basic',
            is_expiring_link=builtin_account_tiers['Basic']['is_expiring_link'],
            is_original_file=builtin_account_tiers['Basic']['is_original_file'],
        )
        basic_thumbnail_height = ThumbnailHeight.objects.create(
            height=builtin_account_tiers['Basic']['thumbnail_height']
        )
        basic_account_tier.thumbnail_height.add(basic_thumbnail_height)
        basic_account_tier.save()

        # premium account tier
        premium_account_tier = AccountTier.objects.create(
            tier_name='Premium',
            is_expiring_link=builtin_account_tiers['Premium']['is_expiring_link'],
            is_original_file=builtin_account_tiers['Premium']['is_original_file']
        )
        premium_thumbnail_height = ThumbnailHeight.objects.create(
            height=builtin_account_tiers['Premium']['thumbnail_height']
        )
        premium_account_tier.thumbnail_size.set([
            basic_thumbnail_height,
            premium_thumbnail_height
        ])
        premium_account_tier.save()

        # enterprise account tier
        enterprise_account_tier = AccountTier.objects.create(
            tier_name='Enterprise',
            is_expiring_link=builtin_account_tiers['Enterprise']['is_expiring_link'],
            is_original_file=builtin_account_tiers['Enterprise']['is_original_file']
        )
        enterprise_account_tier.thumbnail_height.set([
            basic_thumbnail_height,
            premium_thumbnail_height
        ])
        enterprise_account_tier.save()


@receiver(pre_save, sender=UserImage)
def create_thumbnails(sender, instance, *args, **kwargs):
    image_name, image_extension = os.path.splitext(os.path.basename(instance.original_image.name))
    instance.image_name = image_name
    instance.image_extension = image_extension
    user_tier_thumbnail_heights = instance.user.account_tier.thumbnail_height.all()
    for thumb_height in user_tier_thumbnail_heights:
        field_name = 'thumbnail_px_' + str(thumb_height)
        if not instance.get_field_by_name(field_name):
            original_image = Image.open(instance.original_image)
            size_of_original_image = original_image.size
            resizing_ratio = size_of_original_image[1] / thumb_height.height
            thumbnail = original_image.resize((int(size_of_original_image[0]/resizing_ratio), thumb_height.height))

            # Thumbnail_path presents the location for model field
            # full_thumbnail_path is only for storing thumbnail inside of media directory and it's not used further
            thumbnail_path = 'images/' + image_name + '_thumbnail' + str(thumb_height) + image_extension
            full_thumbnail_path = 'media/' + thumbnail_path
            thumbnail.save(full_thumbnail_path)
            setattr(instance, field_name, thumbnail_path)