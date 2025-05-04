import os

def get_secret(env_var, backup=None):
    return os.getenv(env_var, backup)

if get_secret('PIPELINE') == 'production':
    from .production import *
else:
    from .local import *