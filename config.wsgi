import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/donacions_parc')

from app import app as application
