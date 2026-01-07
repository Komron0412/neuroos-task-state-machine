import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neuroos.settings")
django.setup()