import sys
import os
import inspect

try:
    from arches.settings import *
except ImportError:
    pass

LOAD_TEST_DATA = True

PACKAGE_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PACKAGE = PACKAGE_ROOT.split(os.sep)[-1]
DATABASES['default']['NAME'] = 'arches_%s' % (PACKAGE)

SITE_URL = 'http://localhost:8000',
INSTALLED_APPS = INSTALLED_APPS + (PACKAGE,)
STATICFILES_DIRS = (os.path.join(ROOT_DIR, 'media'),) + STATICFILES_DIRS
TEMPLATE_DIRS = (os.path.join(ROOT_DIR, 'templates'),os.path.join(ROOT_DIR, 'templatetags')) + TEMPLATE_DIRS
LOGIN_URL = '/Arches/'
DATA_CONCEPT_SCHEME = 'CA DOT'
ENTITY_MODEL = {'default': 'arches.app.packages.%s.models.entity.Entity' % PACKAGE, 'project': 'arches.app.packages.%s.views.view_models.project.Project' % PACKAGE}
HIP_TEST = 'so cool'

try:
    from settings_local import *
except ImportError:
    pass
