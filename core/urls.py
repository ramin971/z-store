from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,TagViewSet,DescriptionViewSet,SizeViewSet\
                    ,ProductViewSet,RatingProduct,CommentViewSet,ReactionViewSet\
                    ,CouponViewSet,CustomerViewSet,OrderItemViewSet,CartViewSet

from drf_spectacular.views import SpectacularAPIView,SpectacularRedocView\
                                ,SpectacularSwaggerView



router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'tag', TagViewSet)
router.register(r'description', DescriptionViewSet)
router.register(r'size', SizeViewSet)
router.register(r'product', ProductViewSet)
router.register(r'rating',RatingProduct)
router.register(r'comment',CommentViewSet,basename='comment')
router.register(r'reactions',ReactionViewSet)
router.register(r'coupon',CouponViewSet)
router.register(r'customer',CustomerViewSet)
router.register(r'order',OrderItemViewSet)
router.register(r'cart',CartViewSet,basename='cart')






urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('',include(router.urls)),
    
    # swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   

    # path(),
]
