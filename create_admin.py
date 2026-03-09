import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tourism_platform'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourism_platform.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='sidahmed ely').exists():
    User.objects.create_superuser('sidahmed ely', 'sidahmedelyboube@gmail.com', 'elyboube2002')
    print("Admin created!")