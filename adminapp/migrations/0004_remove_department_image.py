# Generated by Django 5.1.3 on 2024-12-22 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0003_alter_doctor_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='image',
        ),
    ]