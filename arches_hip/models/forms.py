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
from arches.app.utils.imageutils import generate_thumbnail
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

class ClassificationForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'classification',
            'icon': 'fa fa-bar-chart-o',
            'name': _('Classification/Components'),
            'class': ClassificationForm
        }

    def update(self, data):
        self.update_nodes('PHASE_TYPE_ASSIGNMENT.E17', data)
        self.update_nodes('COMPONENT.E18', data)
        self.update_nodes('MODIFICATION_EVENT.E11', data)
        return

    def load(self):
        if self.resource:
            self.data['PHASE_TYPE_ASSIGNMENT.E17'] = {
                'branch_lists': self.get_nodes('PHASE_TYPE_ASSIGNMENT.E17'),
                'domains': {
                    'HERITAGE_RESOURCE_TYPE.E55': Concept().get_e55_domain('HERITAGE_RESOURCE_TYPE.E55'),
                    'HERITAGE_RESOURCE_USE_TYPE.E55' : Concept().get_e55_domain('HERITAGE_RESOURCE_USE_TYPE.E55'),
                    'CULTURAL_PERIOD.E55' : Concept().get_e55_domain('CULTURAL_PERIOD.E55'),
                    'STYLE.E55' : Concept().get_e55_domain('STYLE.E55')
                }
            }
            self.data['COMPONENT.E18'] = {
                'branch_lists': self.get_nodes('COMPONENT.E18'),
                'domains': {
                    'CONSTRUCTION_TECHNIQUE.E55': Concept().get_e55_domain('CONSTRUCTION_TECHNIQUE.E55'),
                    'MATERIAL.E57' : Concept().get_e55_domain('MATERIAL.E57'),
                    'COMPONENT_TYPE.E55' : Concept().get_e55_domain('COMPONENT_TYPE.E55')
                }
            }
            self.data['MODIFICATION_EVENT.E11'] = {
                'branch_lists': self.get_nodes('MODIFICATION_EVENT.E11'),
                'domains': {
                    'MODIFICATION_TYPE.E55': Concept().get_e55_domain('MODIFICATION_TYPE.E55'),
                }
            }
            self.data['ANCILLARY_FEATURE_TYPE.E55'] = {
                'branch_lists': self.get_nodes('PHASE_TYPE_ASSIGNMENT.E17'),
                'domains': {
                    'ANCILLARY_FEATURE_TYPE.E55' : Concept().get_e55_domain('ANCILLARY_FEATURE_TYPE.E55')
                }
            }


class ExternalReferenceForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'external-reference',
            'icon': 'fa-random',
            'name': _('External System References'),
            'class': ExternalReferenceForm
        }

    def update(self, data):
        self.update_nodes('EXTERNAL_RESOURCE.E1', data)
        return

    def load(self):
        if self.resource:
            self.data['EXTERNAL_RESOURCE.E1'] = {
                'branch_lists': self.get_nodes('EXTERNAL_RESOURCE.E1'),
                'domains': {
                    'EXTERNAL_XREF_TYPE.E55': Concept().get_e55_domain('EXTERNAL_XREF_TYPE.E55'),
                }
            }

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
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'condition',
            'icon': 'fa-asterisk',
            'name': _('Condition Assessment'),
            'class': ConditionForm
        }

    def get_nodes(self, entity, entitytypeid):
        ret = []
        entities = entity.find_entities_by_type_id(entitytypeid)
        for entity in entities:
            ret.append({'nodes': entity.flatten()})

        return ret

    def update_nodes(self, entitytypeid, data):
        if self.schema == None:
            self.schema = Entity.get_mapping_schema(self.resource.entitytypeid)

        for value in data[entitytypeid]:
            if entitytypeid == 'CONDITION_IMAGE.E73':
                temp = None
                for newentity in value['nodes']:
                    if newentity['entitytypeid'] != 'CONDITION_IMAGE.E73':
                        entity = Entity()
                        entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                        if temp == None:
                            temp = entity
                        else:
                            temp.merge(entity)

                self.baseentity.merge_at(temp, 'CONDITION_STATE.E3')
            else:
                for newentity in value['nodes']:
                    entity = Entity()
                    entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                    if self.baseentity == None:
                        self.baseentity = entity
                    else:
                        self.baseentity.merge(entity)

    def update(self, data, files):
        if len(files) > 0:
            for f in files:
                data['CONDITION_IMAGE.E73'].append({
                    'nodes':[{
                        'entitytypeid': 'CONDITION_IMAGE_FILE_PATH.E62',
                        'entityid': '',
                        'value': files[f]
                    },{
                        'entitytypeid': 'CONDITION_IMAGE_THUMBNAIL.E62',
                        'entityid': '',
                        'value': generate_thumbnail(files[f])
                    }]
                })

        for value in data['CONDITION_ASSESSMENT.E14']:
            for node in value['nodes']:
                if node['entitytypeid'] == 'CONDITION_ASSESSMENT.E14' and node['entityid'] != '':
                    #remove the node
                    self.resource.filter(lambda entity: entity.entityid != node['entityid'])

        self.update_nodes('CONDITION_TYPE.E55', data)
        self.update_nodes('THREAT_TYPE.E55', data)
        self.update_nodes('RECOMMENDATION_TYPE.E55', data)
        self.update_nodes('DATE_CONDITION_ASSESSED.E49', data)
        self.update_nodes('CONDITION_DESCRIPTION.E62', data)
        self.update_nodes('DISTURBANCE_TYPE.E55', data)
        self.update_nodes('CONDITION_IMAGE.E73', data)

        self.resource.merge_at(self.baseentity, self.resource.entitytypeid)
        self.resource.trim()
                   
    def load(self):

        self.data = {
            'data': [],
            'domains': {
                'DISTURBANCE_TYPE.E55': Concept().get_e55_domain('DISTURBANCE_TYPE.E55'),
                'CONDITION_TYPE.E55' : Concept().get_e55_domain('CONDITION_TYPE.E55'),
                'THREAT_TYPE.E55' : Concept().get_e55_domain('THREAT_TYPE.E55'),
                'RECOMMENDATION_TYPE.E55' : Concept().get_e55_domain('RECOMMENDATION_TYPE.E55')
            }
        }

        condition_assessment_entities = self.resource.find_entities_by_type_id('CONDITION_ASSESSMENT.E14')

        for entity in condition_assessment_entities:
            self.data['data'].append({
                'DISTURBANCE_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'DISTURBANCE_TYPE.E55')
                },
                'CONDITION_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'CONDITION_TYPE.E55')
                },
                'THREAT_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'THREAT_TYPE.E55')
                },
                'RECOMMENDATION_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'RECOMMENDATION_TYPE.E55')
                },
                'DATE_CONDITION_ASSESSED.E49': {
                    'branch_lists': self.get_nodes(entity, 'DATE_CONDITION_ASSESSED.E49')
                },
                'CONDITION_DESCRIPTION.E62': {
                    'branch_lists': self.get_nodes(entity, 'CONDITION_DESCRIPTION.E62')
                },
                'CONDITION_IMAGE.E73': {
                    'branch_lists': self.get_nodes(entity, 'CONDITION_IMAGE.E73')
                },
                'CONDITION_ASSESSMENT.E14': {
                    'branch_lists': self.get_nodes(entity, 'CONDITION_ASSESSMENT.E14')
                }
            })


class LocationForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'location',
            'icon': 'fa-map-marker',
            'name': _('Location'),
            'class': LocationForm
        }

    def update(self, data):
        self.update_nodes('SPATIAL_COORDINATES_GEOMETRY.E47', data)
        self.update_nodes('PLACE_ADDRESS.E45', data)
        self.update_nodes('DESCRIPTION_OF_LOCATION.E62', data)
        self.update_nodes('SETTING_TYPE.E55', data)
        self.update_nodes('ADMINISTRATIVE_SUBDIVISION.E48', data)
        self.update_nodes('PLACE_APPELLATION_CADASTRAL_REFERENCE.E44', data)
        return

    def load(self):
        self.data['SPATIAL_COORDINATES_GEOMETRY.E47'] = {
            'branch_lists': self.get_nodes('SPATIAL_COORDINATES_GEOMETRY.E47'),
            'domains': {
                'GEOMETRY_QUALIFIER.E55': Concept().get_e55_domain('GEOMETRY_QUALIFIER.E55')
            }
        }

        self.data['PLACE_ADDRESS.E45'] = {
            'branch_lists': self.get_nodes('PLACE_ADDRESS.E45'),
            'domains': {
                'ADDRESS_TYPE.E55': Concept().get_e55_domain('ADDRESS_TYPE.E55')
            }
        }
        
        self.data['DESCRIPTION_OF_LOCATION.E62'] = {
            'branch_lists': self.get_nodes('DESCRIPTION_OF_LOCATION.E62'),
            'domains': {}
        }

        self.data['SETTING_TYPE.E55'] = {
            'branch_lists': self.get_nodes('SETTING_TYPE.E55'),
            'domains': {
                'SETTING_TYPE.E55': Concept().get_e55_domain('SETTING_TYPE.E55')
            }
        }

        self.data['ADMINISTRATIVE_SUBDIVISION.E48'] = {
            'branch_lists': self.get_nodes('ADMINISTRATIVE_SUBDIVISION.E48'),
            'domains': {
                'ADMINISTRATIVE_SUBDIVISION_TYPE.E55': Concept().get_e55_domain('ADMINISTRATIVE_SUBDIVISION_TYPE.E55')
            }
        }

        self.data['PLACE_APPELLATION_CADASTRAL_REFERENCE.E44'] = {
            'branch_lists': self.get_nodes('PLACE_APPELLATION_CADASTRAL_REFERENCE.E44'),
            'domains': {}
        }

        return
