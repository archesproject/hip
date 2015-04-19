import os
import inspect
from arches.settings import *
from django.utils.translation import ugettext as _

PACKAGE_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PACKAGE_NAME = PACKAGE_ROOT.split(os.sep)[-1]
DATABASES['default']['NAME'] = 'arches_%s' % (PACKAGE_NAME)
ROOT_URLCONF = '%s.urls' % (PACKAGE_NAME)
INSTALLED_APPS = INSTALLED_APPS + (PACKAGE_NAME,)
STATICFILES_DIRS = (os.path.join(PACKAGE_ROOT, 'media'),) + STATICFILES_DIRS
TEMPLATE_DIRS = (os.path.join(PACKAGE_ROOT, 'templates'),os.path.join(PACKAGE_ROOT, 'templatetags')) + TEMPLATE_DIRS
RESOURCE_MODEL = {'default': 'arches_hip.models.resource.Resource'}
APP_NAME = 'Arches v3.0 - HIP v1.0'
PACKAGE_VALIDATOR = 'arches_hip.source_data.validation.HIP_Validator'

DEFAULT_MAP_ZOOM = 1

def RESOURCE_TYPE_CONFIGS():
    return {
        'HERITAGE_RESOURCE.E18': {
            'resourcetypeid': 'HERITAGE_RESOURCE.E18',
            'name': _('Historic Resource'),
            'icon_class': 'fa fa-university',
            'default_page': 'summary',
            'default_description': 'No description available',
            'description_node': _('DESCRIPTION.E62'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#fa6003',
            'stroke_color': '#fb8c49',
            'fill_color': '#ffc29e',
            'primary_name_lookup': {
                'entity_type': 'NAME.E41',
                'lookup_value': 'Primary'
            },
            'sort_order': 1
        },
        'HERITAGE_RESOURCE_GROUP.E27': {
            'resourcetypeid': 'HERITAGE_RESOURCE_GROUP.E27',
            'name': _('Historic District'),
            'icon_class': 'fa fa-th',
            'default_page': 'summary',
            'default_description': 'No description available',
            'description_node': _('REASONS.E62'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#FFC53D',
            'stroke_color': '#d9b562',
            'fill_color': '#eedbad',
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
            'default_page': 'activity-summary',
            'default_description': 'No description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#6DC3FC',
            'stroke_color': '#88bde0',
            'fill_color': '#afcce1',
            'primary_name_lookup': {
                'entity_type': 'NAME.E41',
                'lookup_value': 'Primary'
            },
            'sort_order': 3
        },
        'HISTORICAL_EVENT.E5':{
            'resourcetypeid': 'HISTORICAL_EVENT.E5',
            'name': _('Historic Event'),
            'icon_class': 'fa fa-calendar',
            'default_page': 'historical-event-summary',
            'default_description': 'No description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#4EBF41',
            'stroke_color': '#61a659',
            'fill_color': '#c2d8bf',
            'primary_name_lookup': {
                'entity_type': 'NAME.E41',
                'lookup_value': 'Primary'
            },
            'sort_order': 4
        },
        'ACTOR.E39': {
            'resourcetypeid': 'ACTOR.E39',
            'name': _('Person/Organization'),
            'icon_class': 'fa fa-group',
            'default_page': 'actor-summary',
            'default_description': 'No description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#a44b0f',
            'stroke_color': '#a7673d',
            'fill_color': '#c8b2a3',
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
            'default_page': 'information-resource-summary',
            'default_description': 'No description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#8D45F8',
            'stroke_color': '#9367d5',
            'fill_color': '#c3b5d8',
            'primary_name_lookup': {
                'entity_type': 'TITLE.E41',
                'lookup_value': 'Primary'
            },
            'sort_order': 6
        }
    }

EXPORT_CONFIG = os.path.normpath(os.path.join(PACKAGE_ROOT, 'source_data', 'resource_export_mappings.json'))

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
)
BUSISNESS_DATA_FILES = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PACKAGE_ROOT, 'logs', 'application.txt'),
        },
    },
    'loggers': {
        'arches': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'arches_hip': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}


DATE_PARSING_FORMAT = ['%B %d, %Y', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S']

try:
    from settings_local import *
except ImportError:
    pass
