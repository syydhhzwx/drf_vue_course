# Generated by Django 2.0.6 on 2021-01-26 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_teacher_course_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_video',
            field=models.FileField(blank=True, null=True, upload_to='video', verbose_name='视频'),
        ),
    ]
