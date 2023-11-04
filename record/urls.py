from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'videos', views.VideoViewSet, basename="videos")

urlpatterns = [
    path('', include(router.urls)),
]


# urlpatterns = [
#     path('videos/', views.VideoList.as_view(), name="video_list"),
#     path('videos/<int:pk>/', views.VideoDetail.as_view(), name="video_detail"), 
# ]
