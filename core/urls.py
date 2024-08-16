from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,TagViewSet,DescriptionViewSet,SizeViewSet\
                    ,ProductViewSet,RatingProduct,CommentViewSet

# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# schema_view = get_schema_view(
#    openapi.Info(
#       title="My Project API",
#       default_version='v1',
#       description="API documentation for My Project",
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )


router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'tag', TagViewSet)
router.register(r'description', DescriptionViewSet)
router.register(r'size', SizeViewSet)
router.register(r'product', ProductViewSet)
router.register(r'rating',RatingProduct)
router.register(r'comment',CommentViewSet,basename='comment')



urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('',include(router.urls)),
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   

    # path(),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)