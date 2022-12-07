# Generated by Django 4.1.3 on 2022-12-06 19:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import sys_base.models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_base', '0007_alter_patient_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.CharField(choices=[('2022-12-07', '2022-12-07'), ('2022-12-08', '2022-12-08'), ('2022-12-09', '2022-12-09'), ('2022-12-10', '2022-12-10'), ('2022-12-11', '2022-12-11'), ('2022-12-12', '2022-12-12'), ('2022-12-13', '2022-12-13')], max_length=60),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(blank=True, db_column='iin', null=True, on_delete=django.db.models.deletion.CASCADE, to='sys_base.patient', to_field='iin'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='iin',
            field=models.CharField(default='', max_length=12, unique=True, validators=[django.core.validators.MinLengthValidator(12), sys_base.models.charfield_is_number_validator]),
        ),
    ]
