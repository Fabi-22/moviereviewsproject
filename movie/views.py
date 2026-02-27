from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Movie
import matplotlib
import matplotlib.pyplot as plt
import io
import base64

def home(request):
    search = request.GET.get('searchMovie', '').strip()
    qs = Movie.objects.all()
    if search:
        qs = qs.filter(title__icontains=search)
    return render(request, 'home.html', {'movies': qs})

def about(request):
    return render(request, 'about.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and password:
            # create user if not exists
            if User.objects.filter(username=username).exists():
                error = 'Username already taken'
                return render(request, 'signup.html', {'error': error})
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def statistics_year_view(request):
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1
    years = list(movie_counts_by_year.keys())
    counts = [movie_counts_by_year[y] for y in years]
    bar_positions = range(len(years))
    plt.bar(bar_positions, counts, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, years, rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return render(request, 'statistics_year.html', {'graphic': graphic})

def _first_genre(raw_genre):
    if not raw_genre:
        return "None"
    g = raw_genre.split('|')[0].split(',')[0].strip()
    return g if g else "None"

def statistics_genre_view(request):
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()
    movie_counts_by_genre = {}
    for movie in all_movies:
        genre = _first_genre(movie.genre)
        movie_counts_by_genre[genre] = movie_counts_by_genre.get(genre, 0) + 1
    genres = list(movie_counts_by_genre.keys())
    counts = [movie_counts_by_genre[g] for g in genres]
    bar_positions = range(len(genres))
    plt.bar(bar_positions, counts, align='center')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, genres, rotation=90)
    plt.subplots_adjust(bottom=0.35)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return render(request, 'statistics_genre.html', {'graphic': graphic})