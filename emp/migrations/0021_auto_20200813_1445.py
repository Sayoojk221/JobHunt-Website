# Generated by Django 3.1 on 2020-08-13 09:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0020_auto_20200813_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 9, 15, 34, 499763, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 9, 15, 34, 488755, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 9, 15, 34, 495761, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 9, 15, 34, 496761, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='EmployeeReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(default='', max_length=100)),
                ('employeeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emp.employeeregister')),
            ],
        ),
    ]
