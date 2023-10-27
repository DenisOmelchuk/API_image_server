from celery import shared_task
from time import sleep


@shared_task
def timesleep(time):
    sleep(time)
    return None

@shared_task
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