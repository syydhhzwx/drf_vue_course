import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django_redis import get_redis_connection
from user.models import UserInfo
from user.utils import get_user_by_account


class UserModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text='用户token')
    code = serializers.CharField(max_length=6, write_only=True, help_text='短信验证码')

    class Meta:
        model = UserInfo
        fields = ['phone', 'password',
                  'id', 'username', 'token', 'code']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'phone': {
                'write_only': True,
            },
            'username': {
                'read_only': True
            },
            'id': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        """验证手机号和密码"""
        phone = attrs.get('phone')
        password = attrs.get('password')
        code = attrs.get('code')

        if not re.match(r'^1[3-9][0-9]{9}$', phone):
            raise serializers.ValidationError('手机号格式有误')

        redis_connection = get_redis_connection('sms_code')
        phone_code = redis_connection.get('exp_%s' % phone)
        print(phone_code)

        if phone_code.decode() != code:
            raise serializers.ValidationError('验证码输入错误')
        try:
            user = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user = None

        if user:
            raise serializers.ValidationError('当前手机号已经被注册')

        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        hash_pwd = make_password(password)
        username = validated_data.get('phone')

        user_obj = UserInfo.objects.create(
            phone=username,
            username=username,
            password=hash_pwd,

        )
        # 生成token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload_handler = jwt_payload_handler(user_obj)
        user_obj.token = jwt_encode_handler(payload_handler)

        return user_obj


class PhoneLoginModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text='用户token')
    code = serializers.CharField(max_length=6, write_only=True, help_text='短信验证码')
    fields = ['phone',
              'id', 'token', 'code']
    extra_kwargs = {

        'phone': {
            'write_only': True,
        },

        'id': {
            'read_only': True
        }
    }

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')
        if not re.match(r'^1[3-9][0-9]{9}$', phone):
            raise serializers.ValidationError('手机号格式有误')

        redis_connection = get_redis_connection('sms_code')
        phone_code = redis_connection.get('exp_%s' % phone)
        print(phone_code)

        if phone_code.decode() != code:
            raise serializers.ValidationError('验证码输入错误')
        try:
            user = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user = None

        if user:
            raise serializers.ValidationError('当前手机号已经被注册')
        user_obj = UserInfo.objects.filter(phone=phone)
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload_handler = jwt_payload_handler(user_obj)
        user_obj.token = jwt_encode_handler(payload_handler)

        return user_obj, attrs
        # return
