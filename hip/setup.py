import os
import sys
from django.conf import settings
from django.core import management
from arches.setup import get_version
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.utils.data_management.resources.importer import ResourceLoader
import arches.app.utils.data_management.resources.remover as resource_remover
from arches.management.commands.package_utils import resource_graphs
from arches.management.commands.package_utils import authority_files


def setup():
    get_version(path_to_file=os.path.abspath(os.path.dirname(__file__)))

def install(path_to_source_data_dir=None):
    truncate_db()
    delete_index(index='concept_labels')

    load_resource_graphs()

    load_authority_files(path_to_source_data_dir)

    load_map_layers()

    resource_remover.truncate_resources()
    delete_index(index='resource')
    delete_index(index='entity')
    delete_index(index='maplayers')
    delete_index(index='term')    
    load_resources()

def export_data():
    pass

def import_data():
    pass

def truncate_db():
    management.call_command('packages', operation='setup') 

def load_resource_graphs():
    resource_graphs.load_graphs(break_on_error=True)
    pass

def load_authority_files(path_to_files=None):
    authority_files.load_authority_files(break_on_error=True)

def load_map_layers():
    pass

def delete_index(index=None):
    se = SearchEngineFactory().create()
    se.delete(index=index, force=True)
    pass

def install_dependencies():
    pass

def build_permissions():
    pass

def load_users():
    pass

def load_resources(external_file=None):
    rl = ResourceLoader()
    if external_file != None:
        print 'loading:', external_file
        rl.load(external_file)
    else:
        for f in settings.BUSISNESS_DATA_FILES:
            rl.load(f)



if __name__ == "__main__":

#     #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hip.settings")
    install()
#     print sys.argv[1]
#     module = import_module('setup')
#     method_ref = getattr(module, sys.argv[1])
#     method_ref() 