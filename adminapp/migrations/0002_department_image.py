# Generated by Django 5.1.3 on 2024-12-21 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='image',
            field=models.ImageField(default='department_images/default.jpg', upload_to='department_images/'),
        ),
    ]
