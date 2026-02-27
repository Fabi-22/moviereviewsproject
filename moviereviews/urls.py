from django.contrib import admin
from django.urls import path, include
from movie import views as movie_views
from django.conf.urls.static import static
from django.conf import settings

# authentication views will be handled by our own functions in movie.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie_views.home, name='home'),
    path('about/', movie_views.about, name='about'),
    path('news/', include('news.urls')),
    path('signup/', movie_views.signup, name='signup'),
    path('statistics/year/', movie_views.statistics_year_view, name='statistics_year'),
    path('statistics/genre/', movie_views.statistics_genre_view, name='statistics_genre'),
    path('login/', movie_views.login_view, name='login'),
    path('logout/', movie_views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
