# Generated by Django 3.0.8 on 2020-08-07 04:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0007_auto_20200807_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 4, 35, 56, 69077, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 4, 35, 56, 76081, tzinfo=utc)),
        ),
    ]
