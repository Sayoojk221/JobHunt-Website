# Generated by Django 3.0.8 on 2020-08-07 09:54

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0010_auto_20200807_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofileshortlists',
            name='employeejobid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='emp.EmployeeJobDetails'),
        ),
        migrations.AddField(
            model_name='employeeprofileshortlists',
            name='employeepersonalid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='emp.EmployeePersonalDetails'),
        ),
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 9, 54, 25, 418825, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 9, 54, 25, 409819, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 9, 54, 25, 416824, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 9, 54, 25, 417824, tzinfo=utc)),
        ),
    ]
