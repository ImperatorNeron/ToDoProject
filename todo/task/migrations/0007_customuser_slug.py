# Generated by Django 4.0.6 on 2022-07-31 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_siteimages_alter_customuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
