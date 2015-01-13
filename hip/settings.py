import os
import inspect
from django.utils.translation import ugettext as _
from arches.settings import *

PACKAGE_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PACKAGE_NAME = PACKAGE_ROOT.split(os.sep)[-1]
DATABASES['default']['NAME'] = 'arches_%s' % (PACKAGE_NAME)
ROOT_URLCONF = '%s.urls' % (PACKAGE_NAME)
ELASTICSEARCH_HTTP_PORT = 9200
INSTALLED_APPS = INSTALLED_APPS + (PACKAGE_NAME,)
STATICFILES_DIRS = (os.path.join(PACKAGE_ROOT, 'media'),) + STATICFILES_DIRS
TEMPLATE_DIRS = (os.path.join(PACKAGE_ROOT, 'templates'),os.path.join(PACKAGE_ROOT, 'templatetags')) + TEMPLATE_DIRS
RESOURCE_MODEL = {'default': 'hip.models.resource.Resource'}
DEFAULT_MAP_X = -13168799.0
DEFAULT_MAP_Y = 4012635.2
DEFAULT_MAP_ZOOM = 10
RESOURCE_CLUSTERING_MIN_RESOLUTION = 4.777314267823516


RESOURCE_TYPE_CONFIGS = {
    'HERITAGE_RESOURCE.E18': {
        'resourcetypeid': 'HERITAGE_RESOURCE.E18',
        'name': _('Heritage Resource'),
        'icon_class': 'fa fa-trophy',
        'default_page': 'summary',
        'description': _('INSERT RESOURCE DESCRIPTION HERE'),
        'categories': [_('Resource')],
        'has_layer': True,
        'on_map': False,
        'vector_color': '#3366FF',
        'primary_name_lookup': {
            'entity_type': 'NAME.E41',
            'lookup_value': 'Primary'
        },
        'sort_order': 1
    },
    'HERITAGE_RESOURCE_GROUP.E27': {
        'resourcetypeid': 'HERITAGE_RESOURCE_GROUP.E27',
        'name': _('Historic District'),
        'icon_class': 'fa fa-bookmark-o',
        'default_page': 'summary',
        'description': _('INSERT RESOURCE DESCRIPTION HERE'),
        'categories': [_('Resource')],
        'has_layer': True,
        'on_map': False,
        'vector_color': '#F5B800',
        'primary_name_lookup': {
            'entity_type': 'NAME.E41',
            'lookup_value': 'Primary'
        },
        'sort_order': 2
    },
    'ACTIVITY.E7': {
        'resourcetypeid': 'ACTIVITY.E7',
        'name': _('Activity'),
        'icon_class': 'fa fa-tasks',
        'default_page': 'summary',
        'description': _('INSERT RESOURCE DESCRIPTION HERE'),
        'categories': [_('Resource')],
        'has_layer': True,
        'on_map': False,
        'vector_color': '#24a221',
        'primary_name_lookup': {
            'entity_type': 'NAME.E41',
            'lookup_value': 'Primary'
        },
        'sort_order': 3
    },
    'HISTORICAL_EVENT.E5':{
        'resourcetypeid': 'HISTORICAL_EVENT.E5',
        'name': _('Historic Event'),
        'icon_class': 'fa fa-calendar-o',
        'default_page': 'summary',
        'description': _('INSERT RESOURCE DESCRIPTION HERE'),
        'categories': [_('Resource')],
        'has_layer': True,
        'on_map': False,
        'vector_color': '#C31C46',
        'primary_name_lookup': {
            'entity_type': 'NAME.E41',
            'lookup_value': 'Primary'
        },
        'sort_order': 4
    },
    'ACTOR.E39': {
        'resourcetypeid': 'ACTOR.E39',
        'name': _('Actor'),
        'icon_class': 'fa fa-group',
        'default_page': 'summary',
        'description': _('INSERT RESOURCE DESCRIPTION HERE'),
        'categories': [_('Resource')],
        'has_layer': True,
        'on_map': False,
        'vector_color': '#28BE99',
        'primary_name_lookup': {
            'entity_type': 'ACTOR_APPELLATION.E82',
            'lookup_value': 'Primary'
        },
        'sort_order': 5
    },
    'INFORMATION_RESOURCE.E73': {
        'resourcetypeid': 'INFORMATION_RESOURCE.E73',
        'name': _('Information Resource'),
        'icon_class': 'fa fa-file-text-o',
        'default_page': 'summary',
        'description': _('INSERT RESOURCE DESCRIPTION HERE'),
        'categories': [_('Resource')],
        'has_layer': True,
        'on_map': False,
        'vector_color': '#FF6633',
        'primary_name_lookup': {
            'entity_type': 'TITLE.E41',
            'lookup_value': 'Primary'
        },
        'sort_order': 6
    }
}

GEOCODING_PROVIDER = 'hip.utils.losangeles_geocoder'

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
