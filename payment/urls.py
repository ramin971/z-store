from django.urls import path
from . import views

urlpatterns = [
    path('go-to-gateway/<uuid:id>/<int:price>/<str:mobile>',views.go_to_gateway_view,name='go-to-gateway'),
    path('callbak-gateway/<uuid:cart_id>',views.callback_gateway_view,name='callback-gateway')
]