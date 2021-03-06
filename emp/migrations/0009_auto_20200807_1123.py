# Generated by Django 3.0.8 on 2020-08-07 05:53

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0008_auto_20200807_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employernewjobpost',
            name='createddate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 5, 53, 52, 355975, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 7, 5, 53, 52, 362980, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='JobShortlists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 8, 7, 5, 53, 52, 363981, tzinfo=utc))),
                ('status', models.CharField(default='', max_length=200)),
                ('employeeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emp.EmployeeRegister')),
                ('shortlistedjobid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emp.EmployerNewJobPost')),
            ],
        ),
    ]
