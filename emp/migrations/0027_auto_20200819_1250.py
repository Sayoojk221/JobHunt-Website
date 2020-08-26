# Generated by Django 3.1 on 2020-08-19 07:20

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0026_auto_20200818_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeepersonaldetails',
            name='description',
            field=models.CharField(max_length=10000, null='empty'),
        ),
        migrations.AlterField(
            model_name='employeeprofileshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 7, 20, 58, 714563, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 7, 20, 58, 703553, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 7, 20, 58, 712561, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobshortlists',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 7, 20, 58, 713562, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='EmployeePersonalResume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(null='empty', upload_to='personalresume')),
                ('employeeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emp.employeeregister')),
            ],
        ),
    ]