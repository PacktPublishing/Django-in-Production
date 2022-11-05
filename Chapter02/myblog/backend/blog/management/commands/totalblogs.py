from django.core.management.base import BaseCommand
from blog.models import Blog

class Command(BaseCommand):
    help = 'Returns total number of blogs'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('author_ids', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--custom',
            type=int,
            help='custom optional param',
        )

    def handle(self, *args, **options):
        print(f'Author ids - {options["author_ids"]}')
        print(f'Custom - {options["custom"]}')
        total_blogs = Blog.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Total blogs: "{total_blogs}"'))