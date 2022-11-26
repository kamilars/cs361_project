# Generated by Django 4.1.3 on 2022-11-26 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_base', '0005_rename_admin_adminstaff'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentRequest',
            fields=[
                ('requestId', models.IntegerField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(max_length=50)),
                ('patient_surname', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=50)),
                ('doctor', models.CharField(max_length=100)),
                ('time_slot', models.CharField(max_length=50)),
            ],
        ),
    ]
