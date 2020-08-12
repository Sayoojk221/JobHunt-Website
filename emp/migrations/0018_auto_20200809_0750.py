# Generated by Django 3.0.8 on 2020-08-09 02:20

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0017_auto_20200808_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 9, 2, 20, 12, 66276, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 9, 2, 20, 12, 50651, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 9, 2, 20, 12, 66276, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 9, 2, 20, 12, 66276, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='deletedcandidates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emp.EmployeeRegister')),
                ('employerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emp.EmployerRegister')),
            ],
        ),
    ]
