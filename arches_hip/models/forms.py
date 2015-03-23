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
from arches.app.models.concept import Concept
from arches.app.models.forms import ResourceForm
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
        self.update_nodes('RESOURCE_TYPE_CLASSIFICATION.E55', data)

        beginning_of_existence_nodes = []
        end_of_existence_nodes = []
        for branch_list in data['important_dates']:
            for node in branch_list['nodes']:
                if node['entitytypeid'] == 'BEGINNING_OF_EXISTENCE_TYPE.E55':
                    beginning_of_existence_nodes.append(branch_list)
                if node['entitytypeid'] == 'END_OF_EXISTENCE_TYPE.E55':
                    end_of_existence_nodes.append(branch_list)

        for branch_list in beginning_of_existence_nodes:
            for node in branch_list['nodes']:        
                if node['entitytypeid'] == 'START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49':
                    node['entitytypeid'] = 'START_DATE_OF_EXISTENCE.E49'

        for branch_list in end_of_existence_nodes:
            for node in branch_list['nodes']:        
                if node['entitytypeid'] == 'START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49':
                    node['entitytypeid'] = 'END_DATE_OF_EXISTENCE.E49'

        self.update_nodes('BEGINNING_OF_EXISTENCE.E63', {'BEGINNING_OF_EXISTENCE.E63':beginning_of_existence_nodes})
        self.update_nodes('END_OF_EXISTENCE.E64', {'END_OF_EXISTENCE.E64':end_of_existence_nodes})

    def load(self):
        self.data['important_dates'] = {
            'branch_lists': self.get_nodes('BEGINNING_OF_EXISTENCE.E63') + self.get_nodes('END_OF_EXISTENCE.E64'),
            'domains': {'important_dates' : Concept().get_e55_domain('BEGINNING_OF_EXISTENCE_TYPE.E55') + Concept().get_e55_domain('END_OF_EXISTENCE_TYPE.E55')}
        }

        if self.resource:
            if self.resource.entitytypeid == 'HERITAGE_RESOURCE.E18':            
                self.data['RESOURCE_TYPE_CLASSIFICATION.E55'] = {
                    'branch_lists': self.get_nodes('RESOURCE_TYPE_CLASSIFICATION.E55'),
                    'domains': {'RESOURCE_TYPE_CLASSIFICATION.E55' : Concept().get_e55_domain('RESOURCE_TYPE_CLASSIFICATION.E55')}
                }

            self.data['NAME.E41'] = {
                'branch_lists': self.get_nodes('NAME.E41'),
                'domains': {'NAME_TYPE.E55' : Concept().get_e55_domain('NAME_TYPE.E55')}
                # 'defaults': {
                #     'NAME_TYPE.E55': default_name_type['id'],
                #     'NAME.E41': ''
                # }
            }
            self.data['KEYWORD.E55'] = {
                'branch_lists': self.get_nodes('KEYWORD.E55'),
                'domains': {'KEYWORD.E55' : Concept().get_e55_domain('KEYWORD.E55')}
            }

            self.data['primaryname_conceptid'] = self.data['NAME.E41']['domains']['NAME_TYPE.E55'][3]['id']



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
        description_types = Concept().get_e55_domain('DESCRIPTION_TYPE.E55')
        default_description_type = description_types[2]
        if self.resource:
            self.data['DESCRIPTION.E62'] = {
                'branch_lists': self.get_nodes('DESCRIPTION.E62'),
                'domains': {'DESCRIPTION_TYPE.E55' : description_types},
                'defaults': {
                    'DESCRIPTION_TYPE.E55': default_description_type['id'],
                }
            }


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
        if self.resource:
            self.data['MEASUREMENT_TYPE.E55'] = {
                'branch_lists': self.get_nodes('MEASUREMENT_TYPE.E55'),
                'domains': {
                    'MEASUREMENT_TYPE.E55' : Concept().get_e55_domain('MEASUREMENT_TYPE.E55'),
                    'UNIT_OF_MEASUREMENT.E55': Concept().get_e55_domain('UNIT_OF_MEASUREMENT.E55')
                }
            }

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
        self.data['domains']['CONDITION_TYPE_E55'] = Concept().get_e55_domain('CONDITION_TYPE.E55')
        default_description_type = self.data['domains']['CONDITION_TYPE_E55'][0]
        self.data['defaults']['CONDITION_TYPE_E55'] = {
            'CONDITION_TYPE_E55__entityid': '',
            'CONDITION_TYPE_E55__value': '',
            'CONDITION_TYPE_E55__label': ''
        }
        if self.resource:
            self.data['CONDITION_TYPE_E55'] = self.get_nodes('CONDITION_TYPE.E55')

class ClassificationForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'classification',
            'icon': 'fa-asterisk',
            'name': _('Classification/Components'),
            'class': ClassificationForm
        }

    def update(self, data):
        self.update_nodes('PHASE_TYPE_ASSIGNMENT.E17', data)
        return

    def load(self):
        self.data['PHASE_TYPE_ASSIGNMENT.E17'] = {
            'branch_lists': self.get_nodes('PHASE_TYPE_ASSIGNMENT.E17'),
            'domains': {
                'HERITAGE_RESOURCE_TYPE.E55': Concept().get_e55_domain('HERITAGE_RESOURCE_TYPE.E55'),
                'HERITAGE_RESOURCE_USE_TYPE.E55' : Concept().get_e55_domain('HERITAGE_RESOURCE_USE_TYPE.E55'),
                'CULTURAL_PERIOD.E55' : Concept().get_e55_domain('CULTURAL_PERIOD.E55'),
                'STYLE.E55' : Concept().get_e55_domain('STYLE.E55')
            }
        }
        return

