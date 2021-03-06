# Generated by Django 3.0.8 on 2020-08-08 03:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0013_auto_20200807_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='employeejobdetails',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='emp.EmployeeJobDetails'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='employeepersonalid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='emp.EmployeePersonalDetails'),
        ),
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 8, 3, 22, 50, 18954, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 8, 3, 22, 50, 9947, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 8, 3, 22, 50, 16952, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 8, 3, 22, 50, 17953, tzinfo=utc)),
        ),
    ]
