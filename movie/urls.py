from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("movies/", views.movies, name="movies"),
    path("movies/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("movies/<int:movie_id>/reviews/new/", views.review_create, name="review_create"),
    path("reviews/<int:review_id>/edit/", views.review_edit, name="review_edit"),
    path("reviews/<int:review_id>/delete/", views.review_delete, name="review_delete"),
]
