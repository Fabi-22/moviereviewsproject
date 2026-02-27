from django.core.management.base import BaseCommand
from movie.models import Movie
from django.conf import settings
import os
import json
import csv
import urllib.request
import ssl

class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        # prefer CSV if available, otherwise use the bundled JSON
        csv_path = 'movies_initial.csv'
        json_path = 'movie/management/commands/movies.json'

        movies = []
        if os.path.exists(csv_path):
            self.stdout.write(f"Loading data from CSV: {csv_path}")
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    movies.append({
                        'imdbid': row.get('imdbID'),
                        'title': row.get('title'),
                        'genre': row.get('genre'),
                        'year': row.get('year'),
                        'plot': row.get('plot'),
                        'poster': row.get('poster'),
                    })
        elif os.path.exists(json_path):
            self.stdout.write(f"Loading data from JSON: {json_path}")
            with open(json_path, 'r', encoding='utf-8') as file:
                movies = json.load(file)
        else:
            self.stderr.write("No source file found (CSV or JSON)")
            return

        # add/update first 100 entries
        for movie in movies[:100]:
            exist = Movie.objects.filter(title=movie.get('title')).first()
            poster = movie.get('poster') or ''
            # default placeholder
            image_value = 'movie/images/default.png'
            if poster:
                # if it's an HTTP(S) URL, download it locally
                if poster.startswith('http'):
                    # use imdbid or title to name file
                    name = movie.get('imdbid') or movie.get('title', '').replace(' ', '_')
                    ext = os.path.splitext(poster)[1] or '.jpg'
                    local_filename = f"{name}{ext}"
                    dest_dir = os.path.join(settings.MEDIA_ROOT, 'movie', 'images')
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, local_filename)
                    try:
                        # ignore SSL certificate errors when downloading
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        with urllib.request.urlopen(poster, context=ctx) as response:
                            with open(dest_path, 'wb') as out_file:
                                out_file.write(response.read())
                        image_value = os.path.join('movie/images', local_filename)
                    except Exception as e:
                        self.stderr.write(f"failed to download poster for {movie.get('title')}: {e}")
                else:
                    # assume it's already a relative path we can use
                    image_value = poster

            if not exist:
                try:
                    Movie.objects.create(
                        title=movie.get('title'),
                        image=image_value,
                        genre=movie.get('genre'),
                        year=movie.get('year'),
                        description=movie.get('plot'),
                    )
                except Exception as e:
                    self.stderr.write(f"Failed to create {movie.get('title')}: {e}")
            else:
                try:
                    exist.title = movie.get('title')
                    exist.image = image_value
                    exist.genre = movie.get('genre')
                    exist.year = movie.get('year')
                    exist.description = movie.get('plot')
                    exist.save()
                except Exception as e:
                    self.stderr.write(f"Failed to update {movie.get('title')}: {e}")