# Generated by Django 5.2.3 on 2025-06-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articleapp', '0002_vacancypost'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancypost',
            name='share_contact',
            field=models.BooleanField(default=False),
        ),
    ]
