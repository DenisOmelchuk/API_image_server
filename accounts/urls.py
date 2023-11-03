from django.urls import path, include
from . import views
from .views import ImageCreateAPIView, ExpiringLinkCreateAPIView

urlpatterns = [
    path('upload/', ImageCreateAPIView.as_view(), name='upload_image'),
    path('get_image/<str:user_id>/<str:image_id>/<str:height>/', views.get_image),
    path('expiring_link/', ExpiringLinkCreateAPIView.as_view())
]