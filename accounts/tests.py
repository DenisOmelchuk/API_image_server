from django.test import TestCase
from . models import CustomUser, AccountTier, ThumbnailHeight
from rest_framework.test import APIClient
from rest_framework import status
import os
import io
from PIL import Image as PILImage
from django.urls import reverse

class ImageUploadAPITestCase(TestCase):
    def setUp(self):
        thumbnail = ThumbnailHeight.objects.create(height=200)
        account_tier = AccountTier.objects.create(tier_name='Basic')
        thumbnail.accounttier_set.add(account_tier)
        self.user = CustomUser.objects.create(
            username = 'testuser1',
            account_tier = account_tier
        )
        self.user.set_password('testuser123451')
        self.user.save()
        self.client = APIClient()
        self.image_file = self.generate_photo_file()

    def generate_photo_file(self):
        file = io.BytesIO()
        image = PILImage.new('RGB', size=(500, 500), color=(155, 0, 0))
        image.save(file, 'jpeg')
        file.name = 'test.jpeg'
        file.seek(0)
        return file

    def test_image_upload_api(self):
        user = CustomUser.objects.get(username='testuser1')
        login_successful = self.client.login(username="testuser1", password="testuser123451", account_tier = None, test = None)
        url = reverse('upload_image')
        data = {'original_image': self.image_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        # Clean up, delete the user and their profile
        self.user.delete()
        CustomUser.objects.all().delete()