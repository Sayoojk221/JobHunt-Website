# Generated by Django 3.1 on 2020-08-13 10:13

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0022_auto_20200813_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 10, 13, 53, 512936, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employeereview',
            name='employeepersonalid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emp.employeepersonaldetails'),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 10, 13, 53, 501929, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 10, 13, 53, 509934, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 10, 13, 53, 510935, tzinfo=utc)),
        ),
    ]
