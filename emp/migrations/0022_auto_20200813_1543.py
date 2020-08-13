# Generated by Django 3.1 on 2020-08-13 10:13

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0021_auto_20200813_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeereview',
            name='employeepersonalid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='emp.employeepersonaldetails'),
        ),
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 10, 13, 24, 500943, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 10, 13, 24, 489936, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 10, 13, 24, 496940, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 10, 13, 24, 498941, tzinfo=utc)),
        ),
    ]
