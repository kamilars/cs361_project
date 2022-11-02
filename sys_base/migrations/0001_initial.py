# Generated by Django 4.1.2 on 2022-10-31 16:48

import django.core.validators
from django.db import migrations, models
import sys_base.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('iin', models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(12), sys_base.models.charfield_is_number_validator])),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('middlename', models.CharField(max_length=30)),
                ('contact_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$', message='Incorrect Phone Number'), django.core.validators.MinLengthValidator(11)])),
                ('department_id', models.PositiveIntegerField()),
                ('specialization_details_id', models.PositiveIntegerField()),
                ('experience', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('category_doctor', models.CharField(max_length=10)),
                ('price_of_appointment', models.PositiveIntegerField()),
                ('degree', models.CharField(max_length=10)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('address_doctor', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('iin', models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(12), sys_base.models.charfield_is_number_validator])),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('middlename', models.CharField(max_length=30)),
                ('blood_group', models.CharField(max_length=3, validators=[sys_base.models.blood_type_validator])),
                ('contact_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$', message='Incorrect Phone Number'), django.core.validators.MinLengthValidator(11)])),
                ('email', models.CharField(max_length=30, validators=[django.core.validators.EmailValidator])),
                ('address', models.CharField(max_length=30)),
                ('marital_status', models.CharField(max_length=30)),
                ('registration_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]