from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView

from cart.serializer import OrderModelSerializer
from course.models import Course, CourseExpire, Order


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    # 添加课程到购物车
    def add_cart(self, request):
        """购物车添加"""
        course_id = request.data.get('course_id')
        # 当前视图只允许认证后的用户访问
        user_id = request.user.id
        select = True
        # 有效期
        expire = 0

        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({
                'message': '参数有误，课程不存在'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            redis_connection = get_redis_connection('cart')
            # redis 管道
            pipeline = redis_connection.pipeline()
            #  开启管道
            pipeline.multi()
            # 添加商品信息
            pipeline.hset('cart_%s' % user_id, course_id, expire)
            # 添加商品的勾选状态
            pipeline.sadd('select_%s' % user_id, course_id)
            # 管道执行
            pipeline.execute()
            # 获取购物城的商品数量
            cart_len = redis_connection.hlen('cart_%s' % user_id)
        except Exception:
            return Response({
                'message': '参数有误'
            }, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        return Response({
            'message': '购物车添加成功',
            'cart_length': cart_len,
        })

    # 获取购物车信息
    def cart_list(self, request):
        """获取购物车信息"""
        user_id = request.user.id
        redis_connection = get_redis_connection('cart')
        cart_list_byte = redis_connection.hgetall('cart_%s' % user_id)
        select_list_byte = redis_connection.smembers('select_%s' % user_id)

        data = []
        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue

            data.append({
                'selected': True if course_id_byte in select_list_byte else False,
                'course_img': "http://127.0.0.1:8000" + course.course_img.url,
                'name': course.name,
                'id': course.id,
                'expire_id': expire_id,
                'price': course.price,
                # 当前课程的有效期
                'expire_list': course.expire_list,
                'real_price': course.expire_real_price(expire_id),
                # 'active': course,
            })

        return Response(data)

    def discount_expire(self, request):
        """改变redis中的有效期"""
        course_id = request.data.get('course_id')
        user_id = request.user.id
        expire_id = request.data.get('expric_id')
        # print(course_id,user_id,expire_id)

        try:
            course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            # 判断前端传递 的有效期 选项
            if expire_id > 0:
                expire_item = CourseExpire.objects.filter(is_show=True, is_delete=False, pk=expire_id)
                if not expire_item:
                    raise Course.DoesNotExist()
        except Course.DoesNotExist:
            return Response({'message': '课程信息不存在'}, status=status.HTTP_400_BAD_REQUEST)
        connection = get_redis_connection('cart')
        connection.hset('cart_%s' % user_id, course_id, expire_id)

        price = course.expire_real_price(expire_id)
        if price != '':
            return Response({'message': '切换有效期成功',
                             "price": price})
        return Response({'message': '切换有效期成功'})

    def get_select_course(self, request):
        """获取购物车中已勾选的课程并返回到前端"""
        user_id = request.user.id
        redis_connection = get_redis_connection('cart')

        # 获取当前购物车中的所有商品
        cart_list_byte = redis_connection.hgetall("cart_%s" % user_id)
        select_list_byte = redis_connection.smembers("select_%s" % user_id)

        # 循环从mysql中获取课程的信息
        data = []
        total_price = 0  # 商品总价
        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            # print(course_id,course_id_byte)

            # 判断商品id是否在已勾选的商品列表中
            if course_id_byte in select_list_byte:
                print(111)
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

                # 根据已勾选的商品对应有效期的价格去计算勾选商品的价格
                real_expire_price = course.expire_real_price(expire_id)

                # 将购物车中所需的信息返回
                data.append({
                    "course_img": "http://127.0.0.1:8000" + course.course_img.url,
                    "name": course.name,
                    "id": course.id,
                    "expire_text": expire_text,
                    # 原价
                    "price": original_price,
                    # 活动 有效期计算后的真是价格
                    "real_price": "%.2f" % float(real_expire_price),
                    "discount_name": course.discount_name,
                })

                # 商品叠加后的总价
                total_price += float(real_expire_price)

        return Response({"course_list": data, "total_price": total_price, "message": "获取成功"})


# 改变状态
class CourseSelect(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        print(request.data)
        course_id = request.data.get('course_id')
        user_id = request.data.get('user_id')
        print(course_id)
        redis_connection = get_redis_connection('cart')
        try:
            redis_connection.sadd('select_%s' % user_id, course_id)
        except:
            return Response({'message': '参数错误'})
        return Response({'message': False})

    def delete(self, request):
        course_id = request.data.get('course_id')
        user_id = request.data.get('user_id')
        redis_connection = get_redis_connection('cart')
        print(course_id)
        try:
            redis_connection.srem('select_%s' % user_id, course_id)
        except:
            return Response({'message': '参数错误'})
        return Response({'message': False})


# 删除课程
class DeleteCourse(APIView):

    def delete(self, request):
        course_id = request.data.get('course_id')
        user_id = request.data.get('user_id')
        redis_connection = get_redis_connection('cart')
        print(course_id)
        try:
            redis_connection.hdel('cart_%s' % user_id, course_id)
        except:
            return Response({'message': '参数错误'})
        return Response({'message': False})


# 生成订单
class OrderAPIView(CreateAPIView):
    queryset = Order.objects.filter(is_show=True, is_delete=False)
    serializer_class = OrderModelSerializer
