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

class SummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'summary',
            'icon': 'fa-tag',
            'name': _('Resource Summary'),
            'class': SummaryForm
        }

    def update(self, data):
        self.update_nodes('NAME.E41', data)
        self.update_nodes('KEYWORD.E55', data)

        self.update_node('HERITAGE_RESOURCE_TYPE.E55', data)

    def load(self):
        self.data['domains']['NAME_TYPE_E55'] = self.get_e55_domain('NAME_TYPE.E55')
        default_name_type = self.data['domains']['NAME_TYPE_E55'][0]
        self.data['defaults']['NAME_E41'] = {
            'NAME_E41__entityid': '',
            'NAME_E41__value': '',
            'NAME_TYPE_E55__entityid': '',
            'NAME_TYPE_E55__value': default_name_type['id'],
            'NAME_TYPE_E55__label': default_name_type['value']
        }

        self.data['domains']['KEYWORD_E55'] = self.get_e55_domain('KEYWORD.E55')
        self.data['defaults']['KEYWORD_E55'] = {
            'KEYWORD_E55__entityid': '',
            'KEYWORD_E55__value': '',
            'KEYWORD_E55__label': ''
        }
        if self.resource:
            if self.resource.entitytypeid == 'HERITAGE_RESOURCE.E18':
                self.data['domains']['HERITAGE_RESOURCE_TYPE_E55'] = self.get_e55_domain('HERITAGE_RESOURCE_TYPE.E55')
                default_resource_type = self.data['domains']['HERITAGE_RESOURCE_TYPE_E55'][0]
                resource_type_nodes = self.get_nodes('HERITAGE_RESOURCE_TYPE.E55')
                resource_type_default = {
                    'HERITAGE_RESOURCE_TYPE_E55__entityid': '',
                    'HERITAGE_RESOURCE_TYPE_E55__value': '',
                    'HERITAGE_RESOURCE_TYPE_E55__label': ''
                }
                self.data['HERITAGE_RESOURCE_TYPE_E55'] = resource_type_nodes[0] if len(resource_type_nodes) > 0 else resource_type_default
            self.data['NAME_E41'] = self.get_nodes('NAME.E41')
            self.data['KEYWORD_E55'] = self.get_nodes('KEYWORD.E55')


class DescriptionForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'description',
            'icon': 'fa-picture-o',
            'name': _('Descriptions'),
            'class': DescriptionForm
        }

    def update(self, data):
        self.update_nodes('DESCRIPTION.E62', data)

    def load(self):
        self.data['domains']['DESCRIPTION_TYPE_E55'] = self.get_e55_domain('DESCRIPTION_TYPE.E55')
        default_description_type = self.data['domains']['DESCRIPTION_TYPE_E55'][0]
        self.data['defaults']['DESCRIPTION_E62'] = {
            'DESCRIPTION_E62__entityid': '',
            'DESCRIPTION_E62__value': '',
            'DESCRIPTION_TYPE_E55__entityid': '',
            'DESCRIPTION_TYPE_E55__value': default_description_type['id'],
            'DESCRIPTION_TYPE_E55__label': default_description_type['value']
        }
        if self.resource:
            self.data['DESCRIPTION_E62'] = self.get_nodes('DESCRIPTION.E62')


class MeasurementForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'measurement',
            'icon': 'fa-th-large',
            'name': _('Measurements'),
            'class': MeasurementForm
        }

    def update(self, data):
        self.update_nodes('MEASUREMENT_TYPE.E55', data)


    def load(self):
        self.data['domains']['MEASUREMENT_TYPE_E55'] = self.get_e55_domain('MEASUREMENT_TYPE.E55')
        self.data['domains']['UNIT_OF_MEASUREMENT_E55'] = self.get_e55_domain('UNIT_OF_MEASUREMENT.E55')
        default_measurement_type = self.data['domains']['MEASUREMENT_TYPE_E55'][0]
        default_measurement_unit = self.data['domains']['UNIT_OF_MEASUREMENT_E55'][0]
        self.data['defaults']['MEASUREMENT_TYPE_E55'] = {
            'VALUE_OF_MEASUREMENT_E60__entityid': '',
            'VALUE_OF_MEASUREMENT_E60__value': '',
            'VALUE_OF_MEASUREMENT_E60__label': '',
            'MEASUREMENT_TYPE_E55__entityid': '',
            'MEASUREMENT_TYPE_E55__value': '',
            'MEASUREMENT_TYPE_E55__label': '',
            'UNIT_OF_MEASUREMENT_E55__entityid': '',
            'UNIT_OF_MEASUREMENT_E55__value': '',
            'UNIT_OF_MEASUREMENT_E55__label': ''

        }
        if self.resource:
            self.data['MEASUREMENT_TYPE_E55'] = self.get_nodes('MEASUREMENT_TYPE.E55')

class ConditionForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'condition',
            'icon': 'fa-asterisk',
            'name': _('Condition Assessment'),
            'class': ConditionForm
        }

    def update(self, data):
        self.update_nodes('CONDITION_TYPE.E55', data)

    def load(self):
        self.data['domains']['CONDITION_TYPE_E55'] = self.get_e55_domain('CONDITION_TYPE.E55')
        default_description_type = self.data['domains']['CONDITION_TYPE_E55'][0]
        self.data['defaults']['CONDITION_TYPE_E55'] = {
            'CONDITION_TYPE_E55__entityid': '',
            'CONDITION_TYPE_E55__value': '',
            'CONDITION_TYPE_E55__label': ''
        }
        if self.resource:
            self.data['CONDITION_TYPE_E55'] = self.get_nodes('CONDITION_TYPE.E55')