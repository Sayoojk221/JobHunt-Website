# Generated by Django 3.0.8 on 2020-08-06 12:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0003_auto_20200806_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='employernewjobpost',
            name='linkedinurl',
            field=models.URLField(null='empty'),
            preserve_default='empty',
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 6, 12, 25, 53, 838814, tzinfo=utc)),
        ),
    ]
