from django.urls import path

from cart import views

urlpatterns = [
    path('option/', views.CartViewSet.as_view({'post': 'add_cart', 'get': 'cart_list'})),
    path('del/', views.CourseSelect.as_view()),
    path('del_course/', views.DeleteCourse.as_view()),
]