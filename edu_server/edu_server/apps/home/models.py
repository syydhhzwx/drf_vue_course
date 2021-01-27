from django.db import models

from edu_server.utils.model import BaseModel


class Banner(BaseModel):
    """轮播图模型"""
    img = models.ImageField(upload_to='banner', max_length=255, verbose_name='轮播图图片')
    link = models.CharField(max_length=100, verbose_name='轮播图链接')
    title = models.CharField(max_length=40, verbose_name='轮播图标题')

    class Meta:
        db_table = 'bz_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Nav(BaseModel):
    """导航栏"""
    POSITION_OPTION = (
        (1, '顶部导航'),
        (2, '底部导航'),
    )

    title = models.CharField(max_length=40, verbose_name='导航标题')
    link = models.CharField(max_length=100, verbose_name='导航链接')
    position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name='导航首位')
    is_site = models.BooleanField(default=False, verbose_name='是否有外部链接')

    class Meta:
        db_table = 'bz_nav'
        verbose_name = '导航栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
