# Generated by Django 2.0.6 on 2021-01-28 17:10

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_course_course_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=150, verbose_name='活动名称')),
                ('start_time', models.DateTimeField(verbose_name='优惠策略的开始时间')),
                ('end_time', models.DateTimeField(verbose_name='优惠策略的结束时间')),
                ('remark', models.CharField(blank=True, max_length=250, null=True, verbose_name='备注信息')),
            ],
            options={
                'verbose_name': '商品活动',
                'verbose_name_plural': '商品活动',
                'db_table': 'bz_activity',
            },
        ),
        migrations.CreateModel(
            name='CourseDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('condition', models.IntegerField(blank=True, default=0, help_text='设置参与优惠的价格门槛，表示商品必须在xx价格以上的时候才参与优惠活动，<br>如果不填，则不设置门槛', verbose_name='满足优惠的价格条件')),
                ('sale', models.TextField(blank=True, help_text='\n    不填表示免费；<br>\n    *号开头表示折扣价，例如*0.82表示八二折；<br>\n    -号开头则表示减免，例如-20表示原价-20；<br>\n    如果需要表示满减,则需要使用 原价-优惠价格,例如表示课程价格大于100,优惠10;大于200,优惠20,格式如下:<br>\n    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>\n    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-25<br>\n    ', null=True, verbose_name='优惠公式')),
            ],
            options={
                'verbose_name': '价格优惠策略',
                'verbose_name_plural': '价格优惠策略',
                'db_table': 'bz_course_discount',
            },
        ),
        migrations.CreateModel(
            name='CourseDiscountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=32, verbose_name='优惠类型名称')),
                ('remark', models.CharField(blank=True, max_length=250, null=True, verbose_name='备注信息')),
            ],
            options={
                'verbose_name': '课程优惠类型',
                'verbose_name_plural': '课程优惠类型',
                'db_table': 'bz_course_discount_type',
            },
        ),
        migrations.CreateModel(
            name='CourseExpire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('expire_time', models.IntegerField(blank=True, help_text='有效期按天数计算', null=True, verbose_name='有效期')),
                ('expire_text', models.CharField(blank=True, max_length=150, null=True, verbose_name='提示文本')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='课程价格')),
            ],
            options={
                'verbose_name': '课程有效期',
                'verbose_name_plural': '课程有效期',
                'db_table': 'bz_course_expire',
            },
        ),
        migrations.CreateModel(
            name='CoursePriceDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('active', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='activecourses', to='course.Activity', verbose_name='活动')),
            ],
            options={
                'verbose_name': '课程与优惠策略的关系表',
                'verbose_name_plural': '课程与优惠策略的关系表',
                'db_table': 'bz_course_price_discount',
            },
        ),
        migrations.AlterField(
            model_name='course',
            name='brief',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=2048, null=True, verbose_name='详情介绍'),
        ),
        migrations.AddField(
            model_name='coursepricediscount',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activeprices', to='course.Course', verbose_name='课程'),
        ),
        migrations.AddField(
            model_name='coursepricediscount',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discountcourse', to='course.CourseDiscount', verbose_name='优惠折扣'),
        ),
        migrations.AddField(
            model_name='courseexpire',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_expire', to='course.Course', verbose_name='课程名称'),
        ),
        migrations.AddField(
            model_name='coursediscount',
            name='discount_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursediscounts', to='course.CourseDiscountType', verbose_name='优惠类型'),
        ),
    ]
