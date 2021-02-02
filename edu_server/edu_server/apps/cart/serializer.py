from datetime import datetime

from django.db import transaction
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from course.models import Order, CourseExpire, Course, OrderDetail
from django_redis import get_redis_connection


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
            "id": {"read_only": True},
            "order_number": {"read_only": True},
        }

    def validate(self, attrs):
        """对数据进行验证"""
        attrs_get = attrs.get('pay_type')
        try:
            Order.pay_choices[attrs_get]
        except Order.DoesNotExist:
            raise serializers.ValidationError('您当前选择的支付方式不允许')
        return attrs

    def create(self, validated_data):
        """生成订单与订单详情"""
        redis_connection = get_redis_connection('cart')
        incr = redis_connection.incr('number')
        request = self.context['request']
        user_id = request.data.get('user_id')

        # 生成订单号 时间戳 + 用户id  +随机字符串
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % int(user_id) + "%06d" % int(incr)


        # 生成订单
        with transaction.atomic():
            order = Order.objects.create(
                order_title="百知教育在线商城",
                # 订单总价与支付总价在支付后生成
                total_price=0,
                real_price=0,
                order_number=order_number,
                order_status=0,
                pay_type=validated_data.get("pay_type"),
                credit=0,
                coupon=0,
                order_desc="选择这个课程是你最好的决定",
                user_id=user_id,
            )
        # print(order.order_number)
        # 获取当前购物车中的所有商品
        cart_list_byte = redis_connection.hgetall("cart_%s" % user_id)
        select_list_byte = redis_connection.smembers("select_%s" % user_id)

        # 循环从redis中获取课程的信息
        data = []
        total_price = 0  # 商品总价
        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            # 判断商品id是否在已勾选的商品列表中
            if course_id_byte in select_list_byte:
                try:
                    # 获取对应的课程信息
                    course = Course.objects.get(is_delete=False, is_show=True, pk=course_id)
                except Course.DoesNotExist:
                    continue

                # 如果有效期的id大于0，则代表需要重新计算商品的价格，有效期id不大于0，说明是原价
                original_price = course.price
                expire_text = "永久有效"

                try:
                    if expire_id > 0:
                        course_expire = CourseExpire.objects.get(id=expire_id)
                        # 对应有效期的价格
                        original_price = course_expire.price
                        expire_text = course_expire.expire_text
                except CourseExpire.DoesNotExist:
                    pass

                # 根据已勾选的商品对应有效期的价格去计算勾选商品的总价
                real_expire_price = course.expire_real_price(expire_id)


                # TODO 获取到redis中已勾选的课程后，开始生成订单详细
                try:
                    with transaction.atomic():
                        OrderDetail.objects.create(
                            order=order,
                            course=course,
                            expire=expire_id,
                            price=original_price,
                            real_price=real_expire_price,
                            discount_name=course.discount_name
                        )
                except:
                    raise serializers.ValidationError("订单生成失败")

                # 开始计算订单总价
                order.total_price += float(original_price)
                order.real_price += float(real_expire_price)

            order.save()

        return order
