from pathlib import Path
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = "Populate the database with collections and products"
    
    def handle(self, *args, **options) -> str | None:
        print("Seeding the database...")
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "seed.sql")
        sql = Path(file_path).read_text()
        
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql)
            except Exception as e:
                raise CommandError(e)