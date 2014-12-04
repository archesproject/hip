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
from django.conf import settings
import arches.app.models.models as archesmodels
from arches.app.models.resource import Resource as ArchesResource
from hip.views import forms as hip_forms
from django.utils.translation import ugettext as _

class Resource(ArchesResource):
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)

        if self.entitytypeid == 'HERITAGE_RESOURCE.E18':
            self.form_groups.append({
                'id': 'resource-description',
                'icon':'fa-folder',
                'name': _('Resource Description'),
                'forms': [
                    hip_forms.SummaryForm, 
                    hip_forms.DescriptionForm,
                    hip_forms.MeasurementForm,
                    hip_forms.ConditionForm
                ]
            })      

        self.form_groups.append({
            'id': 'resource-evaluation',
            'icon': 'fa-dashboard',
            'name': _('Evaluate Resource'),
            'forms': []
        })

    def get_primary_name(self):
        displayname = super(Resource, self).get_primary_name()
        names = self.get_names()
        if len(names) > 0:
            displayname = names[0]
        return displayname


    def get_names(self):
        """
        Gets the human readable name to display for entity instances

        """
        pname_key = 'default'
        if self.entitytypeid in settings.PRIMARY_DISPLAY_NAME_LOOKUPS:
            pname_key = self.entitytypeid

        entitytype_of_primaryname = archesmodels.EntityTypes.objects.get(pk = settings.PRIMARY_DISPLAY_NAME_LOOKUPS[pname_key]['entity_type'])
        names = []

        if self.entitytypeid == 'HERITAGE_RESOURCE.E18':
            name_nodes = self.get_root().find_entities_by_type_id(entitytype_of_primaryname)
            if len(name_nodes) > 0:
                for name in name_nodes:
                    names.append(name)

        return names


    @staticmethod
    def get_resource_types():
        types = [{
            'resourcetypeid': 'HERITAGE_RESOURCE.E18',
            'name': _('Heritage Resource'),
            'icon_class': 'fa fa-trophy',
            'default_page': 'summary-form'
        },{
            'resourcetypeid': 'HISTORIC_DISTRICT.E18',
            'name': _('Historic District'),
            'icon_class': 'fa fa-bookmark-o',
            'default_page': 'summary-form'
        },{
            'resourcetypeid': 'ACTIVITY.E7',
            'name': _('Activity'),
            'icon_class': 'fa fa-tasks',
            'default_page': 'summary-form'
        },{
            'resourcetypeid': 'HISTORIC_EVENT.E18',
            'name': _('Historic Event'),
            'icon_class': 'fa fa-calendar-o',
            'default_page': 'summary-form'
        },{
            'resourcetypeid': 'ACTOR.E39',
            'name': _('Actor'),
            'icon_class': 'fa fa-group',
            'default_page': 'summary-form'
        },{
            'resourcetypeid': 'INFORMATION_RESOURCE.E73',
            'name': _('Information Resource'),
            'icon_class': 'fa fa-file-text-o',
            'default_page': 'summary-form'
        }]

        return types      

