# Generated by Django 3.1 on 2020-08-20 09:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0029_auto_20200820_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='employernewjobpost',
            name='jobcode',
            field=models.CharField(max_length=200, null='empty'),
            preserve_default='empty',
        ),
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 9, 52, 53, 43561, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 9, 52, 53, 32552, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 9, 52, 53, 39558, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 9, 52, 53, 41541, tzinfo=utc)),
        ),
    ]
