import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dzi_project.settings')

application = get_wsgi_application()
app = application # <-- This is the line you add