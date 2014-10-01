import os

def install(rootpath):
    trucate_db()
    delete_index(index='concept')

    load_resource_graphs()
    load_authority_files()
    load_map_layers()


def export_data():
    pass

def import_data():
    pass

def trucate_db():
    os.system('python manage.py packages --operation setup')
    pass

def load_resource_graphs():
    pass

def load_authority_files():
    pass

def load_map_layers():
    pass

def delete_index(index=None):
    pass

def install_dependencies():
    pass

def build_permissions():
    pass

def load_users():
    pass

def load_test_data():
    pass