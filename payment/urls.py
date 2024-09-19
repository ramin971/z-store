from django.urls import path
from . import views

urlpatterns = [
    path('go-to-gateway/', views.payment_start, name='payment_start'),
    path('callbak-gateway/', views.payment_return, name='payment_return'),
    path('receipt/<str:tc>/<uuid:cart_id>',views.receipt,name='receipt'),
]