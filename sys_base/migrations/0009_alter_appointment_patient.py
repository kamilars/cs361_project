# Generated by Django 4.1.3 on 2022-12-06 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_base', '0008_alter_appointment_date_alter_appointment_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.CharField(max_length=60),
        ),
    ]