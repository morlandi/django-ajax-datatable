import pylast
import requests
from bs4 import BeautifulSoup

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


class Command(BaseCommand):
    help = 'Scrape LastFM site to retrieve missing release dates form albums'

    def add_arguments(self, parser):
        parser.add_argument(
            '--database', action='store', dest='database', default=DEFAULT_DB_ALIAS,
            help='Nominates a specific database to load fixtures into. Defaults to the "default" database.',
        )

    def handle(self, *args, **options):

        self.using = options['database']

        # Be transactional !
        with transaction.atomic(using=self.using):

            self.fix_release_dates()

            # Close the DB connection -- unless we're still in a transaction. This
            # is required as a workaround for an edge case in MySQL: if the same
            # connection is used to create tables, load data, and query, the query
            # can return incorrect results. See Django #7572, MySQL #37735.
            if transaction.get_autocommit(self.using):
                connections[self.using].close()

    def fix_release_dates(self):

        albums = Album.objects.filter(year=None).exclude(url='')
        print(albums)

        network = pylast.LastFMNetwork(
            api_key=settings.LASTFM_API_KEY,
            api_secret=settings.LASTFM_API_SECRET,
            username=settings.LASTFM_USERNAME,
            password_hash=pylast.md5(settings.LASTFM_PASSWORD)
        )

        for album in albums:
            year = scrape_release_date(album.url)
            print('%s --> %s' % (album, year))
            album.year = year
            album.save(update_fields=['year', ])


def scrape_release_date(url):
    year = None
    try:
        response = requests.get(url)
        assert response.ok

        # Sample html:
        # <div class="metadata-column visible-xs">
        #     <dl class="catalogue-metadata">
        #         <dt class="catalogue-metadata-heading">Length</dt>
        #         <dd class="catalogue-metadata-description">
        #             6 tracks, 48:35
        #         </dd>
        #         <dt class="catalogue-metadata-heading">Release Date</dt>
        #         <dd class="catalogue-metadata-description">25 April 1975</dd>
        #     </dl>
        # </div>

        html = BeautifulSoup(response.content.decode(), features="lxml")
        block = html.find("dl", {"class": "catalogue-metadata"})
        dt = [e for e in block.find_all('dt') if e.text=='Release Date'][0]
        dl = dt.findNextSibling()

        # Sample text:
        # - 25 April 1975
        # - October 2002
        # - 1970

        #print(dl.text)
        tokens = dl.text.split(' ')
        year = int(tokens[-1])
        #print(year)
    except Exception as e:
        year = None

    return year
