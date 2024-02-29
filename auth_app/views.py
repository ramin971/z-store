from .serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView




class CustomTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 1 # 1 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True, path='/auth/jwt')
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    # If SimpleJWT ROTATE_REFRESH_TOKENS = True :
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 1 # 1 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True, path='/auth/jwt')
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)