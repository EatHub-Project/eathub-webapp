apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append('/eathub/eathub-webapp')
sys.path.append('/eathub')

os.environ['DJANGO_SETTINGS_MODULE'] = 'eathub.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
