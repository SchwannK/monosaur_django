from django.core.management.base import BaseCommand
from spend_analyser.transactions import transaction_handler

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        transaction_handler.delete_old_entries()