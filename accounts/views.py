from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UploadImageSerializer, DynamicFieldSerializer, ExpiringLinkSerializer
from rest_framework import generics
from django.http import HttpResponse
from .models import CustomUser, UserImage, ExpiringLink
from rest_framework.decorators import api_view, renderer_classes
from django.http import FileResponse, JsonResponse, HttpResponse
from .functions import generate_random_link
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .tasks import timesleep


class ImageCreateAPIView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated,]
    serializer_class = UploadImageSerializer

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        created_instance = serializer.instance
        response_data = created_instance.get_links(self.request)
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, headers=headers)


class ExpiringLinkCreateAPIView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated,]
    serializer_class = ExpiringLinkSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        image_instance = UserImage.objects.get(id = self.request.data['image_id'])
        created_link = generate_random_link(request.build_absolute_uri(''))
        serializer.save(
            image=image_instance,
            link=created_link
        )
        response_data = created_link
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, headers=headers)


# @api_view(['GET',])
# def get_image(request, user_id, image_id, height):
#     user = CustomUser.objects.get(id=user_id)
#     image_instance = user.images.get(id=image_id)
#     field_name = 'original_image' if height == 'original_image' else 'thumbnail_px_' + str(height)
#     serializer = DynamicFieldSerializer(instance=image_instance, fields=[field_name])
#     return Response(serializer.data)


@api_view(['GET',])
def get_image(request, user_id, image_id, height):
    user = CustomUser.objects.get(id=user_id)
    image_instance = user.images.get(id=image_id)
    field_name = 'original_image' if height == 'original_image' else 'thumbnail_px_' + str(height)
    image_file = getattr(image_instance, field_name)
    # serializer = DynamicFieldSerializer(instance=image_instance, fields=[field_name])
    if image_file:
        return FileResponse(image_file, content_type='image/jpeg')  # Change the content type as needed
    else:
        return Response({'detail': 'Image not found'}, status=404)
    return Response(serializer.data)

@api_view(['GET',])
def list_images(request):
    user = request.user
    user_images_instance = user.images.all()
    user_images_links = []
    for image_instance in user_images_instance:
        user_images_links.append(image_instance.get_links(request))
    return Response(user_images_links)



