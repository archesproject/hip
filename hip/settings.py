import os
import inspect
from arches.settings import *

PACKAGE_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PACKAGE_NAME = PACKAGE_ROOT.split(os.sep)[-1]
DATABASES['default']['NAME'] = 'arches_%s' % (PACKAGE_NAME)
ELASTICSEARCH_HTTP_PORT = 9200
INSTALLED_APPS = INSTALLED_APPS + (PACKAGE_NAME,)
STATICFILES_DIRS = (os.path.join(PACKAGE_ROOT, 'media'),) + STATICFILES_DIRS
TEMPLATE_DIRS = (os.path.join(PACKAGE_ROOT, 'templates'),os.path.join(PACKAGE_ROOT, 'templatetags')) + TEMPLATE_DIRS
ENTITY_MODEL = {'default': 'hip.models.entity.Entity'}
RESOURCE_MODEL = {'default': 'hip.models.resource.Resource'}

PRIMARY_DISPLAY_NAME_LOOKUPS = {
   'default':{
       'entity_type': 'NAME.E41',
       'lookup_value': 'Primary'
   }
}
RESOURCE_GRAPH_LOCATIONS = (
    # Put strings here, like "/home/data/resource_graphs" or "C:/data/resource_graphs".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	os.path.join(PACKAGE_ROOT, 'source_data', 'resource_graphs'),
)
CONCEPT_SCHEME_LOCATIONS = (
    # Put strings here, like "/home/data/authority_files" or "C:/data/authority_files".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	
    #'absolute/path/to/authority_files',
    os.path.normpath(os.path.join(PACKAGE_ROOT, '..', '..', 'arches_la', 'source_data', 'concepts', 'authority_files')),
)
BUSISNESS_DATA_FILES = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.normpath(os.path.join(PACKAGE_ROOT, '..', '..', 'arches_la', 'source_data', 'business_data', 'arches_la.arches')),
)

try:
    from settings_local import *
except ImportError:
    pass
