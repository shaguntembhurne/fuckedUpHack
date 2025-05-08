from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, UserDetailView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('login/', LoginView.as_view(), name='login'),
]