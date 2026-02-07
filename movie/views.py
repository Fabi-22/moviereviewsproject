from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Movie, Review
from .forms import ReviewForm


def home(request):
    return render(request, "movie/home.html", {"name": "Fabiola Valencia Barrios"})


def about(request):
    return render(request, "movie/about.html")


def movies(request):
    searchTerm = request.GET.get("searchMovie")
    if searchTerm:
        movie_list = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movie_list = Movie.objects.all()

    review_form = ReviewForm() if request.user.is_authenticated else None

    movies_with_reviews = []
    for movie in movie_list:
        movies_with_reviews.append({
            "movie": movie,
            "reviews": movie.reviews.order_by("-created_at"),
        })

    return render(
        request,
        "movie/movies.html",
        {
            "movies_data": movies_with_reviews,
            "searchTerm": searchTerm or "",
            "review_form": review_form,
        },
    )


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.order_by("-created_at")

    form = ReviewForm() if request.user.is_authenticated else None

    return render(
        request,
        "movie/movie_detail.html",
        {"movie": movie, "reviews": reviews, "form": form},
    )


def login_view(request):
    error = ""
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("movies")
        error = "Invalid email or password."
    return render(request, "movie/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.name = request.user.username
            review.save()
            return redirect("movie_detail", movie_id=movie.id)
    else:
        form = ReviewForm()
    return render(
        request,
        "movie/review_form.html",
        {"form": form, "movie": movie, "mode": "create"},
    )


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("movie_detail", movie_id=review.movie.id)
    else:
        form = ReviewForm(instance=review)
    return render(
        request,
        "movie/review_form.html",
        {"form": form, "movie": review.movie, "mode": "edit"},
    )


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        movie_id = review.movie.id
        review.delete()
        return redirect("movie_detail", movie_id=movie_id)
    return render(
        request,
        "movie/review_delete.html",
        {"review": review},
    )
