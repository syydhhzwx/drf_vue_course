from rest_framework.generics import ListAPIView

from home.models import Banner, Nav
from home.serializer import BannerModelSerializer, FooterModelSerializer


class BannerAPIView(ListAPIView):
    """轮播图接口"""
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by('-orders')
    serializer_class = BannerModelSerializer


class FooterAPIView(ListAPIView):
    """导航栏接口头部"""
    queryset = Nav.objects.filter(is_delete=False, position=2).order_by('-orders')
    # print(queryset)
    serializer_class = FooterModelSerializer


class FooterAPIView1(ListAPIView):
    """导航栏尾部接口"""
    queryset = Nav.objects.filter(is_delete=False, position=1).order_by('-orders')
    # print(queryset)
    serializer_class = FooterModelSerializer
