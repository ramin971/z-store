from django.urls import path,include
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('jwt/create/',views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path('jwt/refresh/',views.CustomTokenRefreshView.as_view(), name="jwt-refresh"),
    path('jwt/verify/', TokenVerifyView.as_view(), name="jwt-verify"),

]