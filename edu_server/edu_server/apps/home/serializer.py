from rest_framework.serializers import ModelSerializer

from home.models import Banner, Nav


class BannerModelSerializer(ModelSerializer):
    # 轮播图序列化
    class Meta:
        model = Banner
        fields = ['img', 'link']


class FooterModelSerializer(ModelSerializer):
    # 导航栏序列化
    class Meta:
        model = Nav
        fields = ['title', 'link', 'is_site']
