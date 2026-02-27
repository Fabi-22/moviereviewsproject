from django.contrib import admin
from django.urls import path, include
from movie import views as movie_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie_views.home, name='home'),
    path('about/', movie_views.about, name='about'),
    path('news/', include('news.urls')),
    path('signup/', movie_views.signup, name='signup'),
    path('statistics/year/', movie_views.statistics_year_view, name='statistics_year'),
    path('statistics/genre/', movie_views.statistics_genre_view, name='statistics_genre'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)