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

from arches.app.models.entity import Entity
from arches.app.views.resources import ResourceForm
from django.utils.translation import ugettext as _

class ResourceSummaryForm(ResourceForm):
    id = 'resource-summary-form'
    icon = 'fa-tag'
    name = _('Resource Summary')

    def update(self, data):
        for entity in self.resource.find_entities_by_type_id('NAME.E41'):
            self.resource.child_entities.remove(entity)

        schema = Entity.get_mapping_schema(self.resource.entitytypeid)
        for value in data['NAME_E41']:
            baseentity = None
            for newentity in self.decode_data_item(value):
                entity = Entity()
                entity.create_from_mapping(self.resource.entitytypeid, schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                if baseentity == None:
                    baseentity = entity
                else:
                    baseentity.merge(entity)
            
            self.resource.merge_at(baseentity, 'HERITAGE_RESOURCE.E18')


    def load(self):
        self.data['domains']['name_type'] = self.get_e55_domain('NAME_TYPE.E55')
        default_name_type = self.data['domains']['name_type'].first()
        self.data['defaults']['NAME_E41'] = {
            'NAME_E41__entityid': '',
            'NAME_E41__value': '',
            'NAME_TYPE_E55__entityid': '',
            'NAME_TYPE_E55__value': default_name_type.valueid,
            'NAME_TYPE_E55__label': default_name_type.value
        }
        if self.resource:
            if self.resource.entitytypeid == 'HERITAGE_RESOURCE.E18':
                self.data['domains']['resource_type'] = self.get_e55_domain('HERITAGE_RESOURCE_TYPE.E55')
            self.data['NAME_E41'] = self.get_nodes('NAME.E41')


