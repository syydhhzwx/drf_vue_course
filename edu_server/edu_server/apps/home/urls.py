from django.urls import path


from home import views

urlpatterns = [
    path('banner/', views.BannerAPIView.as_view()),
    path('footer/', views.FooterAPIView.as_view()),
    path('footer1/', views.FooterAPIView1.as_view()),
]