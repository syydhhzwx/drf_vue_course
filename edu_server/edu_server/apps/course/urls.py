from django.urls import path

from course import views

urlpatterns = [
    path('course_category/', views.CourseCategoryAPIVIew.as_view()),
    path('course/', views.CourseAPIView.as_view()),
    path('detail/<str:pk>/', views.CourseDetailAPIView.as_view()),
    path('chapter/', views.CourseLessonAPIView.as_view()),
    # path('course', views.CourseAPIView.as_view()),
]