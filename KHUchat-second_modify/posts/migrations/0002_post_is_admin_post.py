# Generated by Django 5.1.3 on 2024-11-21 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_admin_post',
            field=models.BooleanField(default=False),
        ),
    ]
