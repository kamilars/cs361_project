# Generated by Django 4.1.3 on 2022-12-07 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sys_base', '0013_alter_appointment_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together={('doctor', 'date', 'timeslot')},
        ),
    ]
