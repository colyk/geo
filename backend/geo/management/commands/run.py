import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run server with collected static files'

    def handle(self, *args, **options):
        build_dir = os.path.join(settings.BASE_DIR, 'dist')
        if os.path.isdir(build_dir):
            shutil.rmtree(build_dir)
        call_command('collectstatic')
        call_command('runserver')
