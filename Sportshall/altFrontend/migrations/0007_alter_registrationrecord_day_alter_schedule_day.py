# Generated by Django 4.2 on 2023-04-07 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altFrontend', '0006_auto_20210808_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationrecord',
            name='day',
            field=models.CharField(default='Friday', max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.CharField(default='Friday', max_length=20),
        ),
    ]