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

from arches.app.views.resources import ResourceForm
from django.utils.translation import ugettext as _

class ResourceSummaryForm(ResourceForm):
    id = 'resource-summary-form'
    icon = 'fa-tag'
    name = _('Resource Summary')

    def __init__(self, resource=None):
        super(ResourceSummaryForm, self).__init__(resource=resource)

        self.data['names'] = []
        if self.resource:
            if self.resource.entitytypeid == 'HERITAGE_RESOURCE.E18':
                self.domains['resource_type'] = self.get_e55_domain('HERITAGE_RESOURCE_TYPE.E55')
            self.domains['name_type'] = self.get_e55_domain('NAME_TYPE.E55')
            self.load()

    def update(self, post_data):
        # update resource w/ post data
        return self.resource

    def load(self):
        # get data from the resource
        self.data['names'] = [{'id': '1341345', 'name': 'ANP test', 'type_name': 'primary', 'type_id:': '1987234'}]
        # self.data['NAME.E41'] = [{'NAME.E41': 'ANP test', 'NAME_TYPE.E55': 'primary'},
        #                       {'NAME.E41': 'ANP TEST 2', 'NAME_TYPE.E55': 'alias'}]


