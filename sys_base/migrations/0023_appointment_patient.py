# Generated by Django 4.1.4 on 2022-12-08 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sys_base', '0022_alter_patient_blood_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sys_base.patient'),
        ),
    ]