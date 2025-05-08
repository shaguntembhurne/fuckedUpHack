from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, generate_post_from_explanation, proxy_generate_post

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('generate-post/', generate_post_from_explanation, name='generate_post'),
    path('generate-post/', proxy_generate_post, name='proxy_generate_post'),
    path('posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve'}), name='post-detail'),
]
