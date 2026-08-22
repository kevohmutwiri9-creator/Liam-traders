from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.db import connection


class Command(BaseCommand):
    help = 'Ensure django_site table exists and default site is created'

    def handle(self, *args, **options):
        # Check if django_site table exists
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'django_site'
                );
            """)
            table_exists = cursor.fetchone()[0]

        if not table_exists:
            self.stdout.write(self.style.WARNING('django_site table does not exist. Creating it...'))
            # Create the table manually
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE django_site (
                        id SERIAL PRIMARY KEY,
                        domain VARCHAR(100) NOT NULL,
                        name VARCHAR(50) NOT NULL
                    );
                """)
                cursor.execute("""
                    CREATE UNIQUE INDEX django_site_domain_key ON django_site(domain);
                """)
                cursor.execute("""
                    INSERT INTO django_site (id, domain, name) VALUES (1, 'example.com', 'example.com');
                """)
            self.stdout.write(self.style.SUCCESS('django_site table created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('django_site table already exists'))

        # Ensure default site exists
        if not Site.objects.filter(id=1).exists():
            Site.objects.create(id=1, domain='example.com', name='example.com')
            self.stdout.write(self.style.SUCCESS('Default site created'))
        else:
            self.stdout.write(self.style.SUCCESS('Default site already exists'))
