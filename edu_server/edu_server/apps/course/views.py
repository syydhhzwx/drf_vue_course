from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from course.models import CourseCategory, Course, CourseChapter
from course.pagination import CoursePageNumberPagination
from course.serializer import CourseCategoryModelSerializer, CourseModelSerializer, CourseDetailModelSerializer, \
    CourseChapterModelSerializer


class CourseCategoryAPIVIew(ListAPIView):
    """课程分类信息查询"""
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by('-orders')
    serializer_class = CourseCategoryModelSerializer


class CourseAPIView(ListAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseModelSerializer

    # 分类查询的模板类
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('course_category',)

    # 排序
    ordering_fields = ['id', 'students', 'price']

    # 分页

    pagination_class = CoursePageNumberPagination


class CourseDetailAPIView(RetrieveAPIView):
    """课程详细信息的提示"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseDetailModelSerializer


class CourseLessonAPIView(ListAPIView):
    """课程章节与课时"""

    queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseChapterModelSerializer

    # 根据当时的课程id长训对应的章节与课时信息
    filter_backends = [DjangoFilterBackend]
    # 章节与课程的外键
    filter_fields = ['course']
