# Generated by Django 3.1 on 2020-08-21 08:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0031_auto_20200821_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 21, 8, 45, 10, 865743, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 21, 8, 45, 10, 853734, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 21, 8, 45, 10, 860739, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 21, 8, 45, 10, 863741, tzinfo=utc)),
        ),
    ]
