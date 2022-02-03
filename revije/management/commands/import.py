import os
import traceback
from dataclasses import dataclass
import datetime

from django.core.files import File
from django.core.management.base import BaseCommand

from revije.models import Revija


class Command(BaseCommand):
    help = 'Uvozi revije.'
    URL = ''

    def add_arguments(self, parser):
        parser.add_argument('--gm-dir', type=str, default=None)
        parser.add_argument('--glasna-url', type=str, default=None)

    def handle(self, *args, **options):
        gm_dir = options.get('gm_dir')
        glasna_url = options.get('glasna_url')

        if gm_dir:
            self.import_gm(gm_dir)

        if glasna_url:
            self.import_glasna(glasna_url)

    def import_glasna(self, glasna_url):
        raise NotImplementedError

    def import_gm(self, gm_dir):
        TXT, HTML, PDF = '.txt', '.html', '.pdf'
        gm_files = {}
        for fn in os.listdir(gm_dir):
            fn_path = os.path.join(gm_dir, fn)
            if not os.path.isfile(fn_path):
                continue

            base, ext = os.path.splitext(fn)
            if ext not in [TXT, HTML, PDF]:
                continue

            files = gm_files.get(base, {})
            files[ext] = fn_path
            gm_files[base] = files

        for gm in gm_files:
            revija = Revija.objects.filter(from_fn=gm).first() or Revija()

            revija.revija = revija.Type.glasbena_mladina
            year, month = gm.split('_')[-2:]
            revija.from_fn = gm
            revija.datum_izdaje = datetime.date(int(year), int(month), 1)

            gm_file = gm_files[gm]
            with open(gm_file[HTML], 'rb') as f:
                revija.html.save(gm + HTML, File(f))
            with open(gm_file[PDF], 'rb') as f:
                revija.pdf.save(gm + PDF, File(f))
            with open(gm_file[TXT], 'rb') as f:
                revija.txt.save(gm + TXT, File(f))

            revija.save()
