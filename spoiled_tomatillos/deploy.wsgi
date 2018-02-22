import os
import sys
import site


site.addsitedir(os.path.join(os.path.dirname(__file__), 'venv/local/lib/python3.6/site-packages'))

sys.path.append('/var/www/team-53-spring18/spoiled_tomatillos')

activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'venv/bin/activate_this.py'))

from cs4500 import app as application
