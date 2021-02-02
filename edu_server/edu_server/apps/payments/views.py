from datetime import datetime

from alipay import AliPay
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import CourseExpire
from course.models import Order
# from payments.models import UserCourse
from payments.models import UserCourse


class AliPayAPIView(APIView):

    def get(self, request):
        """生成支付宝的支付链接地址"""
        # 获取订单号  有订单才可去支付
        order_number = request.query_params.get("order_number")
        print(order_number)

        # 查询订单是否存在
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return Response({"message": "对不起，您支付的订单不存在"}, status=status.HTTP_400_BAD_REQUEST)

        # 初始化支付宝参数
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG['appid'],  # 沙箱支付id
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # the default notify path
            # 应用私钥
            app_private_key_string=settings.ALIAPY_CONFIG['app_private_key_path'],
            # 支付宝公钥
            alipay_public_key_string=settings.ALIAPY_CONFIG['alipay_public_key_path'],
            sign_type=settings.ALIAPY_CONFIG['sign_type'],  # RSA or RSA2
            debug=settings.ALIAPY_CONFIG['debug'],  # False by default
        )

        # TODO 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,
            total_amount=float(order.real_price),
            subject=order.order_title,
            return_url=settings.ALIAPY_CONFIG['return_url'],
            notify_url=settings.ALIAPY_CONFIG['notify_url'],  # 可选, 不填则使用默认notify url
        )

        # 生成好的支付地址需要将order_string 与网关拼接起来才可以访问
        url = settings.ALIAPY_CONFIG['gateway_url'] + order_string

        return Response(url)

class AliPayResultAPIVIew(APIView):
    """
    处理支付宝支付成功后的业务：验证支付宝的支付情况
    修改订单状态  生成用户购买记录  展示订单结算信息
    """

    def get(self, request):
        # 初始化参数
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG['appid'],  # 沙箱支付id
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # the default notify path
            # 应用私钥
            app_private_key_string=settings.ALIAPY_CONFIG['app_private_key_path'],
            # 支付宝公钥
            alipay_public_key_string=settings.ALIAPY_CONFIG['alipay_public_key_path'],
            sign_type=settings.ALIAPY_CONFIG['sign_type'],  # RSA or RSA2
            debug=settings.ALIAPY_CONFIG['debug'],  # False by default
        )

        # 验证支付参数  支付成功结果
        data = request.query_params.dict()
        # 从参数中获取到签名信息
        signature = data.pop("sign")

        success = alipay.verify(data, signature)
        #

        if success:
            # TODO 支付成功后的业务
            """处理订单业务
                   修改订单状态  生成用户购买记录  展示订单结算信息
                   
                  """
            print(success)
            # 先查询订单是否成功
            order_number = data.get("out_trade_no")
            print(order_number)

            try:
                order = Order.objects.get(order_number=order_number, order_status=0)
                print(order)
            except Order.DoesNotExist:
                return Response({"message": "对不起，订单有问题"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():

                # 开启回滚点
                savepoint = transaction.savepoint()

                # TODO 1.修改订单状态
                try:
                    order.pay_time = datetime.now()
                    order.order_status = 1
                    order.save()

                    # TODO 2.记录用户购买记录
                    user = order.user  # 获取用户
                    order_courses_all = order.order_courses.all()
                    # 订单支付成功后展示的页面信息
                    course_list = []

                    for order_detail in order_courses_all:
                        """遍历本次订单中的课程并返回前端"""
                        course = order_detail.course
                        course.students += 1
                        course.save()

                        # 判断用户购买的课程是否长期有效  如果不是长期有效则为课程记录到期时间
                        timestamp = order.pay_time.timestamp()

                        # 如果购买的不是永久有效课程
                        if order_detail.expire > 0:
                            expire = CourseExpire.objects.get(pk=order_detail.expire)
                            expire_time = expire.expire_time * 24 * 60 * 60
                            # 当前时间+有效期时间 = 最终到期时间
                            end_time = datetime.fromtimestamp(timestamp + expire_time)
                        else:
                            # 永久有效
                            end_time = None

                        UserCourse.objects.create(
                            user_id=user.id,
                            course_id=course.id,
                            trade_no=data.get("trade_no"),
                            buy_type=1,
                            pay_time=order.pay_time,
                            out_time=end_time,
                        )

                        course_list.append({
                            "id": course.id,
                            "name": course.name
                        })

                except:
                    # 如果有异常  开始回滚
                    transaction.savepoint_rollback(savepoint)
                    return Response({"message": "对不起，更新订单失败~"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "支付成功",
                             "pay_time": order.pay_time,
                             "real_price": order.real_price,
                             "course_list": course_list})
        else:

            return Response({"message": "对不起，支付结果查询失败"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)



