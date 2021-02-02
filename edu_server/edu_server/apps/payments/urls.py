from django.urls import path

from payments import views

urlpatterns = [
    path('option/', views.AliPayAPIView.as_view()),
    path('result/', views.AliPayResultAPIVIew.as_view()),
]