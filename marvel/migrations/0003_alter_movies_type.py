# Generated by Django 5.1 on 2024-08-29 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marvel', '0002_alter_movies_options_movies_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='type',
            field=models.CharField(choices=[('Movie', 'Movie'), ('Series', 'Series'), ('Animatied-movie', 'Animatied-movie'), ('Animatied-series', 'Animatied-series')], default='Movie', max_length=20),
        ),
    ]
