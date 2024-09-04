from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from .decorators import admin_only
from django.urls import reverse
# from django.contrib import 


@admin_only
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            form.save_m2m()
            name = request.POST.get('name')
            messages.success(request, f'{name} added succesfully!')
            return redirect('admin-url')
        
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('/admin-url/add-movie')
        
    form = MovieForm
    context = {
        'form': form,
        'title': 'Movie',
        'type': 'Add'
    }
    return render(request, 'add.html', context=context)



@admin_only
def add_details(request, name):
    if request.method == 'POST':

        if name =='Actor':
            form = ActorForm(request.POST)
        elif name == 'Director':
            form = DirectorForm(request.POST)
        elif name == 'Tag':
            form = TagForm(request.POST)
        elif name == 'Genre':
            form = GenreForm(request.POST)
        else:
            messages.error(request, 'Invalid request')
            return redirect('admin-url')

        if form.is_valid():
            form.save()
            actor = request.POST.get('name')
            messages.success(request, f'{actor} added succesfully!')
            return redirect('admin-url')
    
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('/admin-url/actor/')
    
    form = ActorForm()
    context = {
        'form': form,
        'title': name,
        'type': 'Add'
    }
    return render(request, 'add.html', context=context)



@admin_only
def delete_confirmation(request, id):
    movie = Movies.objects.filter(id=id)
    context = {
        'id' : id,
        'movie': movie
    }
    return render(request, 'delete.html', context=context)
    


@admin_only
def delete_movie(request, id):
    movie = Movies.objects.filter(id=id)
    if movie:
        for i in movie:
            name = i.name
    movie.delete()

    messages.info(request, f'{name} deleted succesfully')
    return redirect('/')


@admin_only
def update_movie(request, id):
    movie = get_object_or_404(Movies, id=id)

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            update_movie = form.save(commit=False)
            update_movie.user = request.user
            update_movie.save()
            form.save_m2m()
            messages.success(request, f'Updated succesfully')
            return redirect(reverse('movie', args=[id]))
        
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect(reverse('movie', args=[id]))
    
    form = MovieForm(instance=movie)
    context = {
        'form': form,
        'title': 'Movie',
        'type' : 'Update'
    }
    return render(request, 'add.html', context=context)


import csv
from django.db import connection
from django.http import HttpResponse
from django.utils.text import slugify


@admin_only
def generate_csv(request):
    movies = Movies.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{slugify("movies_data")}.csv"'

    writer = csv.writer(response)
    
    writer.writerow(['Movie_id','Movie', 'Description', 'type', 'Tags', 'Genres', 'Actors'])

    for movie in movies:
        tags = []
        genres = []
        actors = []

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM marvel_movies_tags WHERE movies_id = %s", [movie.id])
            tag_rows = cursor.fetchall()

            for row in tag_rows:
                tag_id = row[2]
                tag = Tag.objects.get(id=tag_id)
                tags.append(tag.name)


        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM marvel_movies_genre WHERE movies_id = %s", [movie.id])
            genre_rows = cursor.fetchall()

            for row in genre_rows:
                genre_id = row[2]
                genre = Genre.objects.get(id=genre_id)
                genres.append(genre.name)


        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM marvel_movies_actors WHERE movies_id = %s", [movie.id])
            actor_rows = cursor.fetchall()

            for row in actor_rows:
                actor_id = row[2]
                actor = Actor.objects.get(id=actor_id)
                actors.append(actor.name)

        writer.writerow([
            movie.id,
            movie.name,
            movie.storyline,
            movie.type,
            ', '.join(tags),
            ', '.join(genres),
            ', '.join(actors)
        ])

    return response
