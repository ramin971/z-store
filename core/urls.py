from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,TagViewSet,DescriptionViewSet,SizeViewSet,ProductViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'tag', TagViewSet)
router.register(r'description', DescriptionViewSet)
router.register(r'size', SizeViewSet)
router.register(r'product', ProductViewSet)



urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('',include(router.urls)),
   

    # path(),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)