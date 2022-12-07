# Generated by Django 4.1.3 on 2022-12-06 15:23

import django.core.validators
from django.db import migrations, models
import sys_base.models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_base', '0003_remove_appointment_patient_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='patient',
            name='blood_group',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='patient',
            name='contact_number',
            field=models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator('^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$', message='Incorrect Phone Number'), django.core.validators.MinLengthValidator(11)]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.CharField(blank=True, max_length=30, validators=[django.core.validators.EmailValidator]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='iin',
            field=models.CharField(default='', max_length=12, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(12), sys_base.models.charfield_is_number_validator]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='marital_status',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
