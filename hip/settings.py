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
    os.path.normpath(os.path.join(PACKAGE_ROOT, '..', '..', 'arches_la', 'source_data', 'business_data', 'sample.arches')),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PACKAGE_ROOT, 'hip.log'),
        },
    },
    'loggers': {
        'arches': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'hip': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


DATE_PARSING_FORMAT = ['%B %d, %Y', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S']

try:
    from settings_local import *
except ImportError:
    pass
