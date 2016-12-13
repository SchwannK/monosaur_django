import sys

from django.core.management import call_command


def create_fixture(model, path):
    sysout = sys.stdout
    f = open(path, 'w')
    sys.stdout = f
    call_command('dump_object', model, '*')
    sys.stdout = sysout
    f.flush()