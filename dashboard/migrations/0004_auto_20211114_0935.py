# Generated by Django 3.2.9 on 2021-11-14 09:35

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20211114_0219'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='dashboard.filealbum')),
            ],
        ),
        migrations.DeleteModel(
            name='Photos',
        ),
    ]
