'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from arches.app.models.resource import Resource as ArchesResource
from hip.models.entity import Entity
from hip.views import forms as hip_forms
from django.utils.translation import ugettext as _

class Resource(ArchesResource, Entity):
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)

        if self.entitytypeid == 'HERITAGE_RESOURCE.E18':
            self.form_groups = [{
                'id': 'resource-description',
                'icon':'fa-folder',
                'name': _('Resource Description'),
                'forms': [hip_forms.ResourceSummaryForm]
            }]

        self.form_groups.append({
            'id': 'resource-evaluation',
            'icon': 'fa-dashboard',
            'name': _('Evaluate Resource'),
            'forms': []
        })


    def get_name(self):
        return self.get_primary_display_name()


    @staticmethod
    def get_resource_types():
        types = [{
            'resourcetypeid': 'HERITAGE_RESOURCE.E18',
            'name': _('Heritage Resource'),
            'icon_class': 'fa fa-trophy',
            'default_page': 'resource-summary-form'
        },{
            'resourcetypeid': 'HISTORIC_DISTRICT.E18',
            'name': _('Historic District'),
            'icon_class': 'fa fa-bookmark-o',
            'default_page': 'resource-summary-form'
        },{
            'resourcetypeid': 'ACTIVITY.E7',
            'name': _('Activity'),
            'icon_class': 'fa fa-tasks',
            'default_page': 'resource-summary-form'
        },{
            'resourcetypeid': 'HISTORIC_EVENT.E18',
            'name': _('Historic Event'),
            'icon_class': 'fa fa-calendar-o',
            'default_page': 'resource-summary-form'
        },{
            'resourcetypeid': 'ACTOR.E39',
            'name': _('Actor'),
            'icon_class': 'fa fa-group',
            'default_page': 'resource-summary-form'
        },{
            'resourcetypeid': 'INFORMATION_RESOURCE.E73',
            'name': _('Information Resource'),
            'icon_class': 'fa fa-file-text-o',
            'default_page': 'resource-summary-form'
        }]

        return types      
