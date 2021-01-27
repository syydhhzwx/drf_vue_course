from rest_framework.serializers import ModelSerializer
from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategoryModelSerializer(ModelSerializer):
    """课程分类序列器"""

    class Meta:
        model = CourseCategory
        fields = ['id', 'name']


class TeacherModelSerializer(ModelSerializer):
    """讲师序列化器"""

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'title', 'signature', 'image']


class CourseModelSerializer(ModelSerializer):
    """课程列表"""
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'course_img', 'students',
                  'lessons', 'pub_lessons', 'price', 'teacher',
                  'lesson_list', ]

    def validate(self, attrs):
        print(attrs)
        return attrs


class CourseDetailModelSerializer(ModelSerializer):
    """课程 详细信息序列化器"""
    # 嵌套序列化器一对一
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'course_img', 'students',
                  'lessons', 'pub_lessons', 'price', 'teacher',
                  'level_name', 'course_video', 'brief_html']


class CourseLessonModelSerializer(ModelSerializer):
    """课时的序列化器"""

    class Meta:
        model = CourseLesson
        fields = ['id', 'name', 'free_trail']


class CourseChapterModelSerializer(ModelSerializer):
    """章节序列化器"""

    # 嵌套序列化器一对多 给参数many=True
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'chapter', 'name', 'coursesections']
