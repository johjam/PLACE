import os
from place.experiment import __version__

INTRO = ("PLACE " + __version__ + " | Author: Paul Freeman | 2018\n" +
         "Originally created by: Jami L Johnson, Henrik tom Wörden, and Kasper van Wijk")

def start():
    print(INTRO)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "placeweb.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(['', 'runserver'])