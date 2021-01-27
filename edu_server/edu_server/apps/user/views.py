import random
import re
import string

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from edu_server.libs.geetest import GeetestLib
from edu_server.settings import constants
from edu_server.utils.send_message import Message
from user.models import UserInfo
from user.serializer import UserModelSerializer, PhoneLoginModelSerializer
from user.utils import get_user_by_account
from django_redis import get_redis_connection

pc_geetest_id = "45dbe199c830b4b9cb1bebd76fbbfdb7"
pc_geetest_key = "cbdff4cfb81c08cb1312f36b963fec22"


class CaptchaAPIView(APIView):
    """极验验证码"""

    user_id = 0
    status = False

    def get(self, request, *args, **kwargs):
        """获取验证码"""

        # 根据用户名验证当前用户是否存在

        account = request.query_params.get('username')
        user = get_user_by_account(account)
        print(user)

        if user is None:
            return Response({'message': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id
        print(self.user_id)

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()
        print(response_str)
        return Response(response_str)

    def post(self, request, *args, **kwargs):
        """校验验证码"""

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge", '')
        validate = request.data.get("geetest_validate", '')
        seccode = request.data.get("geetest_seccode", '')
        account = request.data.get('username')
        user = get_user_by_account(account)

        if user:
            # 验证结果是否正确
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.success_validate(challenge, validate, seccode)
        result = {'status': 'success'} if result else {'status': 'fail'}
        return Response(result)


# 注册API
class UserAPIView(CreateAPIView):
    queryset = UserInfo.objects.all()
    # print(queryset)
    serializer_class = UserModelSerializer


class MessageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """获取验证码 为手机号生成验证码并发送"""

        phone = request.query_params.get('phone')
        # print(phone)
        redis_connection = get_redis_connection('sms_code')
        mobile = redis_connection.get('sms_%s' % phone)
        # print(mobile)
        if mobile is not None:
            return Response({
                'message': '您已经在60s内发送过短信',
            }, status=status.HTTP_400_BAD_REQUEST)
        code_ = random.sample(string.digits, 6)
        code = ''.join(code_)
        print(code)

        redis_connection.setex('sms_%s' % phone, constants.SMS_EXPIRE_TIME, code)
        redis_connection.setex('exp_%s' % phone, constants.MOBILE_EXPIRE_TIME, code)

        # try:
        #     message = Message(constants.API_KEY)
        #     message.send_message(phone, code)
        # except:
        #     return Response({
        #         'message': '短信发送失败，请稍候再试'
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'message': '短信发送成功'
        }, status=status.HTTP_200_OK)


# 验证手机号
class PhoneAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data_get = request.query_params.get('phone')
        data = UserInfo.objects.filter(phone=data_get).first()
        if data:
            return Response({'message': False})
        return Response({'message': True})


# 短信登录
class PhoneLoginAPIView(APIView):
    # def post(self, request, *args, **kwargs):
    # queryset = UserInfo.objects.all()
    # serializer_class = PhoneLoginModelSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.get('phone')
        code = request.data.get('code')
        redis_connection = get_redis_connection('sms_code')
        phone_code = redis_connection.get('exp_%s' % data)
        print(phone_code)
        user_obj = UserInfo.objects.filter(phone=data).first()
        if user_obj and code == phone_code.decode():
            from rest_framework_jwt.settings import api_settings
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload_handler = jwt_payload_handler(user_obj)
            user_obj.token = jwt_encode_handler(payload_handler)
            return Response({
                'id': user_obj.id,
                'token': user_obj.token,
                'username': user_obj.username
            }, status=status.HTTP_200_OK)
        return Response({
            'message': False
        }, status=status.HTTP_400_BAD_REQUEST)
