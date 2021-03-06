# Generated by Django 3.1 on 2020-08-22 00:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0033_auto_20200822_0519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeprofileshortlists',
            old_name='lettersentdate',
            new_name='lettersenddate',
        ),
        migrations.RenameField(
            model_name='jobapplication',
            old_name='lettersentdate',
            new_name='lettersenddate',
        ),
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 22, 0, 5, 26, 35603, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 22, 0, 5, 26, 24595, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 22, 0, 5, 26, 32601, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 22, 0, 5, 26, 34602, tzinfo=utc)),
        ),
    ]
