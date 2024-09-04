from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

def movie_image_upload_path(instance, filename):
    return os.path.join('images', 'movies', filename)

audio_choice = (
    ("English-Hindi", "English-Hindi"),
    ("Hindi", "Hindi"),
    ("English", "English")
)

types = (
    ("Movie", "Movie"),
    ("Series", "Series"),
    ("Animatied-movie", "Animation-movie"),
    ("Animatied-series", "Animation-series")
)


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movies(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    available = models.CharField(max_length=15, choices=audio_choice, default='English')
    type = models.CharField(max_length=20, choices=types, default='Movie')
    image = models.ImageField(upload_to=movie_image_upload_path, default='default.jpg')
    tags = models.ManyToManyField(Tag, related_name='movies', blank=True)

    storyline = models.TextField(blank=True, null=True)
    release = models.DateField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    director = models.ForeignKey(Director, on_delete=models.DO_NOTHING, null=True, blank=True)
    actors = models.ManyToManyField(Actor, related_name='movies', blank=True)
    genre = models.ManyToManyField(Genre, related_name='movies', default='Action')

    class Meta:
        verbose_name = 'movies'
        verbose_name_plural = 'movies'

    def __str__(self):
        return self.name
    


class Comment(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.movie.name}'
    


class UserFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return {self.liked}