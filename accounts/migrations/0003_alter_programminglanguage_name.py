# Generated by Django 5.1.3 on 2024-11-20 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_chatroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programminglanguage',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
