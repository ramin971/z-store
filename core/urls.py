from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,TagViewSet,DescriptionViewSet,SizeViewSet\
                    ,ProductViewSet,RatingProduct,CommentViewSet,ReactionViewSet

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
router.register(r'reactions',ReactionViewSet)



urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('',include(router.urls)),
    
    # swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   

    # path(),
]
