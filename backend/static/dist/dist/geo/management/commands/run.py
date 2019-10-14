from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run server with collected static files'

    def handle(self, *args, **options):
        call_command('runserver')
