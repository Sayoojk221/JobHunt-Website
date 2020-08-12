# Generated by Django 3.0.8 on 2020-08-07 14:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0012_auto_20200807_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeecoverletter',
            name='description',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 14, 23, 29, 803586, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 14, 23, 29, 794579, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 14, 23, 29, 801584, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 14, 23, 29, 802585, tzinfo=utc)),
        ),
    ]