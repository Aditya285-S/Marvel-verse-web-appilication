# Generated by Django 5.1 on 2024-09-01 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marvel', '0007_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='movies',
            name='genre',
            field=models.ManyToManyField(default='Action', related_name='movies', to='marvel.genre'),
        ),
        migrations.AlterField(
            model_name='movies',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]
