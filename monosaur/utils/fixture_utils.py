import os, sys

from django.core.management import call_command


# dump the specified database table into a json file
def create_fixture(model, path):
    sysout = sys.stdout
    my_dir = os.path.abspath(os.path.dirname(__name__))
    f = open(os.path.join(my_dir, path).replace('\\', '/'), 'w+')
    sys.stdout = f
    call_command('dump_object', model, '*')
    sys.stdout = sysout
    f.flush()
    
# load the specified json or yaml file into the database
# Into which table you ask? That is specified in the json
def import_fixture(path):
    call_command('loaddata', path)
