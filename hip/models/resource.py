from arches.app.models.resource import Resource as ArchesResource
from hip.models.entity import Entity #as ArchesResource

class Resource(ArchesResource, Entity):
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)
        

        if self.entitytypeid == 'HERITAGE_DISTRICT.E1':
            #self.forms = HeritageDistrictForms()
            pass
        else:
            #.....
            pass

    @staticmethod
    def get_resource_types():
        types = [{
            'resourcetypeid': 'HISTORIC_RESOURCE.E18',
            'name': 'New Historic Resource',
            'icon_class': 'fa fa-trophy',
            'default_page': 'summary'
        },{
            'resourcetypeid': 'HISTORIC_DISTRICT.E18',
            'name': 'New Historic District',
            'icon_class': 'fa fa-bookmark-o',
            'default_page': 'summary'
        },{
            'resourcetypeid': 'ACTIVITY.E7',
            'name': 'New Activity',
            'icon_class': 'fa fa-tasks',
            'default_page': 'summary'
        },{
            'resourcetypeid': 'HISTORIC_EVENT.E18',
            'name': 'New Historic Event',
            'icon_class': 'fa fa-calendar-o',
            'default_page': 'summary'
        },{
            'resourcetypeid': 'ACTOR.E39',
            'name': 'New Actor',
            'icon_class': 'fa fa-group',
            'default_page': 'summary'
        },{
            'resourcetypeid': 'INFORMATION_RESOURCE.E73',
            'name': 'New Information Resource',
            'icon_class': 'fa fa-file-text-o',
            'default_page': 'summary'
        }]

        return types      
