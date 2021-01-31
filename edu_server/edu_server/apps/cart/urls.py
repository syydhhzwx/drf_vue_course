from django.urls import path

from cart import views

urlpatterns = [
    path('option/', views.CartViewSet.as_view({'post': 'add_cart',
                                               'get': 'cart_list',
                                               'put': 'discount_expire'})),
    path('del/', views.CourseSelect.as_view()),
    path('order/', views.CartViewSet.as_view({'get': 'get_select_course'})),
    path('del_course/', views.DeleteCourse.as_view()),
    path('options/', views.OrderAPIView.as_view()),
]
