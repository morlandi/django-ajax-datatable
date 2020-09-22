import pylast
from django.conf import settings
from django.db import transaction
from django.db import connections
from django.db import DEFAULT_DB_ALIAS
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from backend.models import Artist
from backend.models import Album
from backend.models import Track

ARTISTS = [
    'Genesis',
    'Caparezza',
    'Wim Mertens',
    'Nick Cave',
    'Supertramp',
    'Peter Gabriel',
    'Jethro Tull',
    'Giorgio Gaber',
    'Fabrizio de Andrè',
    'Pete and the Pirates',
    'Men at Work',
    'David Bowie',
    'Pink Floyd',
    'Led Zeppelin',
    'The Police',
    'Depeche Mode',
    'Status Quo',
    'The Who',
    'King Crimson',
]


class Command(BaseCommand):
    help = 'Get a list of all permissions available in the system.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--database', action='store', dest='database', default=DEFAULT_DB_ALIAS,
            help='Nominates a specific database to load fixtures into. Defaults to the "default" database.',
        )
        parser.add_argument('--max-days', type=int, default=0)

    def handle(self, *args, **options):

        self.using = options['database']

        # Be transactional !
        with transaction.atomic(using=self.using):

            self.load_artists()

            # Close the DB connection -- unless we're still in a transaction. This
            # is required as a workaround for an edge case in MySQL: if the same
            # connection is used to create tables, load data, and query, the query
            # can return incorrect results. See Django #7572, MySQL #37735.
            if transaction.get_autocommit(self.using):
                connections[self.using].close()

    def load_artists(self):

        network = pylast.LastFMNetwork(
            api_key=settings.LASTFM_API_KEY,
            api_secret=settings.LASTFM_API_SECRET,
            username=settings.LASTFM_USERNAME,
            password_hash=pylast.md5(settings.LASTFM_PASSWORD)
        )

        for name in ARTISTS:

            if Artist.objects.filter(name=name).exists():
                print('Skip %s' % name)
            else:
                artist = Artist.objects.create(name=name)
                obj_artist = network.get_artist(name)
                self.load_artist(artist, obj_artist)

    def load_artist(self, artist, obj_artist):
        obj_albums = obj_artist.get_top_albums(limit=20)
        for obj_album in obj_albums:

            title = obj_album.item.title

            obj_tracks = obj_album.item.get_tracks()
            num_tracks = len(obj_tracks)
            if num_tracks > 5:

                print('%s/%s (%d tracks)' % (artist.name, title, num_tracks))

                album = Album.objects.create(
                    artist=artist,
                    name=title
                )

                for obj_track in obj_tracks:
                    try:
                        title = obj_track.get_title()
                        print('    %s' % title)
                        track = Track.objects.create(
                            album=album,
                            name=title,
                        )
                    except Exception as e:
                        print('ERROR: ' + str(e))
