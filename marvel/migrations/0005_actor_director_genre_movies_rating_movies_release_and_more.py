# Generated by Django 5.1 on 2024-08-31 06:09

import django.db.models.deletion
import marvel.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marvel', '0004_tag_alter_movies_type_movies_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='movies',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=10, max_digits=3),
        ),
        migrations.AddField(
            model_name='movies',
            name='release',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movies',
            name='storyline',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movies',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to=marvel.models.movie_image_upload_path),
        ),
        migrations.AlterField(
            model_name='movies',
            name='type',
            field=models.CharField(choices=[('Movie', 'Movie'), ('Series', 'Series'), ('Animatied-movie', 'Animation-movie'), ('Animatied-series', 'Animation-series')], default='Movie', max_length=20),
        ),
        migrations.AddField(
            model_name='movies',
            name='actors',
            field=models.ManyToManyField(blank=True, related_name='movies', to='marvel.actor'),
        ),
        migrations.AddField(
            model_name='movies',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='marvel.director'),
        ),
        migrations.AddField(
            model_name='movies',
            name='genre',
            field=models.ManyToManyField(default='Action', to='marvel.genre'),
        ),
    ]