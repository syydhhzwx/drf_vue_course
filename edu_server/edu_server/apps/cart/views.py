from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_redis import get_redis_connection

from course.models import Course


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

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
            })

        return Response(data)


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
