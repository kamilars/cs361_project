# Generated by Django 4.1.3 on 2022-12-07 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_base', '0016_alter_appointment_timeslot_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.CharField(choices=[('2022-12-08', '2022-12-08'), ('2022-12-09', '2022-12-09'), ('2022-12-10', '2022-12-10'), ('2022-12-11', '2022-12-11'), ('2022-12-12', '2022-12-12'), ('2022-12-13', '2022-12-13'), ('2022-12-14', '2022-12-14')], max_length=60),
        ),
    ]