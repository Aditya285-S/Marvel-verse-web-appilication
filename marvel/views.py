from django.shortcuts import render, redirect
from .models import Movies, Genre, Comment, UserFavorites
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import UserForm, CommentForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .functions import recommend

# Create your views here.

def home(request):
    movies = Movies.objects.all().order_by('-year')
    genre = Genre.objects.all()

    paginator = Paginator(movies, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    print(request.user)

    context = {
        'movies': page_obj,
        'page_obj': page_obj,
        'genres': genre
    }
    return render(request, 'index.html', context=context)



# @allowed_users(allowed_rols=['admin'])
def movies(request):
    movies = Movies.objects.filter(Q(type='Animatied-movie') | Q(type='Movie')).order_by('-year')
    genre = Genre.objects.all()

    paginator = Paginator(movies, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'movies': page_obj,
        'page_obj': page_obj,
        'type': 'Movie',
        'genres': genre
    }
    return render(request, 'index.html', context=context)



# @allowed_users(allowed_rols=['user'])
def series(request):
    series = Movies.objects.filter(Q(type='Animatied-series') | Q(type='Series')).order_by('-year')
    genre = Genre.objects.all()

    paginator = Paginator(series, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'movies': page_obj,
        'page_obj': page_obj,
        'type': 'Series',
        'genres': genre
    }
    return render(request, 'index.html', context=context)



def animation(request):
    animation = Movies.objects.filter(Q(type='Animatied-series') | Q(type='Animatied-movie')).order_by('-year')
    genre = Genre.objects.all()
    
    paginator = Paginator(animation, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'movies': page_obj,
        'page_obj': page_obj,
        'type': 'Animation',
        'genres': genre
    }
    return render(request, 'index.html', context=context)



def search(request):
    query = request.GET.get('query')
    genre = Genre.objects.all()
    result = None

    if query:
        movies = Movies.objects.filter(
            Q(name__icontains=query) |
            Q(type__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(genre__name__icontains=query)
            ).distinct().order_by('-year')
        
        if not movies:
            result = 'failure'

    else:
        movies = Movies.objects.all().order_by('-year')

    paginator = Paginator(movies, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'movies': page_obj,
        'page_obj': page_obj,
        'type': result,
        'query': query,
        'genres': genre
    }
    return render(request, 'index.html', context = context)



@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user = authenticate(request, username=username, password=password)

        next_url = request.GET.get('next')
        next_url = next_url if next_url else '/'

        if user:
            login(request, user)
            return redirect(next_url)
        else:        
            messages.error(request, 'Invalid password')
            return redirect('login')
        
    return render(request, 'login.html')



@unauthenticated_user
def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # data = User.objects.filter(username=username)

            group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, f'Account created for {username} succesfully!')
            return redirect('login')
        
        else:
            messages.error(request, form.errors)
            return redirect('sign-up')
        
    form = UserForm()
    context = {
        'form' : form
    }
    return render(request, 'sign_up.html', context = context)



def logoutpage(request):
    logout(request)
    referer = request.META.get('HTTP_REFERER', '/')
    messages.info(request, "You have successfully logged out.")
    return redirect(referer)



@admin_only
def admin(request):
    return render(request, 'admin.html')



def movie(request, movie_id):
    genre = Genre.objects.all()
    movie = Movies.objects.filter(id=movie_id)
    comments = Comment.objects.filter(movie=movie[0], parent__isnull=True)

    fav = None
    if request.user.is_authenticated:
        fav, _ = UserFavorites.objects.get_or_create(user=request.user, movie=movie[0])


    movie_list = recommend(movie[0])
    movies = Movies.objects.filter(name__in = movie_list)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.movie = movie[0]
            
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                new_comment.parent = parent_comment

            new_comment.save()
            return redirect(reverse('movie', args=[movie_id]))

    comment_form = CommentForm()
    context = {
        'movies': movie,
        'genres': genre,
        'comments': comments,
        'comment_form': comment_form,
        'related_movies': movies,
        'favourite': fav
    }
    return render(request, 'movie.html', context=context)


@login_required(login_url='login')
def update_like(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    
    favourite, _ = UserFavorites.objects.get_or_create(user=request.user, movie=movie)

    if favourite.liked:
        favourite.liked = False
    else:
        favourite.liked = True
    favourite.save()
    
    return redirect('movie', movie_id=movie_id)



@login_required(login_url='login')
def movie_download(request, name):
    return HttpResponse(f'{name} downloaded succesfully')



def genre(request, genre):
    genre_obj = get_object_or_404(Genre, name=genre)
    movies = Movies.objects.filter(genre=genre_obj).order_by('-year')
    
    paginator = Paginator(movies, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    print(request.user)

    all_genres = Genre.objects.all()

    context = {
        'movies': page_obj,
        'page_obj': page_obj,
        'genres': all_genres,
        'type' : genre
    }
    return render(request, 'index.html', context=context)
