# Generated by Django 3.2.9 on 2021-11-14 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]