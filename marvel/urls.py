from django.urls import path
from .views import *
from .views_admin import *
# from django.contrib import admin

urlpatterns = [
    path('', home, name='home'),
    path('movies/', movies, name='movies'),
    path('series/', series, name='series'),
    path('animation/', animation, name='animation'),
    path('search/', search, name='search'),
    path('login/', loginpage, name='login'),
    path('logout/', logoutpage, name='logout'),
    path('sign-up/', sign_up, name='sign-up'),
    path('admin-url/', admin, name='admin-url'),
    path('movie/<int:movie_id>/', movie, name='movie'),
    path('movie/update-like/<int:movie_id>', update_like, name='update-like'),
    path('movie/download/<str:name>/', movie_download, name='movie-download'),
    path('movies/<str:genre>/', genre, name='genre'),
    path('admin-url/add-movie/', add_movie, name='add-movie'),
    path('admin-url/<str:name>/', add_details, name='add-details'),
    path('movie/delete-confirmation/<int:id>/', delete_confirmation, name='delete-confirmation'),
    path('movie/delete/<int:id>/', delete_movie, name='delete-movie'),
    path('movie/update/<int:id>/', update_movie, name='update-movie'),
    path('movie/generate-csv/', generate_csv, name='genearte-csv'),
]