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
from arches.app.models.edit_history import EditHistory
from arches.app.models.resource import Resource as ArchesResource
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
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
                    hip_forms.SummaryForm.get_info(), 
                    hip_forms.DescriptionForm.get_info(),
                    hip_forms.MeasurementForm.get_info(),
                    hip_forms.ConditionForm.get_info()
                ]
            })      

        self.form_groups.append({
            'id': 'resource-evaluation',
            'icon': 'fa-dashboard',
            'name': _('Evaluate Resource'),
            'forms': [
                EditHistory.get_info()
            ]
        })

    def get_primary_name(self):
        displayname = super(Resource, self).get_primary_name()
        names = self.get_names()
        if len(names) > 0:
            displayname = names[0].value
        return displayname


    def get_names(self):
        """
        Gets the human readable name to display for entity instances

        """

        names = []
        name_nodes = self.find_entities_by_type_id(settings.RESOURCE_TYPE_CONFIGS[self.entitytypeid]['primary_name_lookup']['entity_type'])
        if len(name_nodes) > 0:
            for name in name_nodes:
                names.append(name)

        return names

    def prepare_documents_for_search_index(self):
        """
        Generates a list of specialized resource based documents to support resource search

        """

        documents = super(Resource, self).prepare_documents_for_search_index()

        for document in documents:
            document['date_groups'] = []
            for nodes in self.get_nodes('BEGINNING_OF_EXISTENCE.E63', keys=['value']):
                document['date_groups'].append({
                    'conceptid': nodes['BEGINNING_OF_EXISTENCE_TYPE_E55__value'],
                    'value': nodes['START_DATE_OF_EXISTENCE_E49__value']
                })

            for nodes in self.get_nodes('END_OF_EXISTENCE.E64', keys=['value']):
                document['date_groups'].append({
                    'conceptid': nodes['END_OF_EXISTENCE_TYPE_E55__value'],
                    'value': nodes['END_DATE_OF_EXISTENCE_E49__value']
                })

        return documents

    def prepare_documents_for_map_index(self, geom_entities=[]):
        """
        Generates a list of geojson documents to support the display of resources on a map

        """

        documents = super(Resource, self).prepare_documents_for_map_index(geom_entities=geom_entities)
        
        resource_type = _('None specified')
        resource_type_nodes = []
        if self.entitytypeid == 'HERITAGE_RESOURCE.E18':
            resource_type_nodes = self.find_entities_by_type_id('HERITAGE_RESOURCE_TYPE.E55')
            
        for resource_type in resource_type_nodes:
            resource_type = resource_type.label

        for document in documents:
            document['properties']['resource_type'] = resource_type

        return documents

    def prepare_search_mappings(self, resource_type_id):
        """
        Creates Elasticsearch document mappings

        """

        documents = super(Resource, self).prepare_search_mappings(resource_type_id)

        mapping =  { 
            resource_type_id : {
                'properties' : {
                    'date_groups' : { 
                        'properties' : {
                            'conceptid': {'type' : 'string', 'index' : 'not_analyzed'}
                        }
                    }
                }
            }
        }

        se = SearchEngineFactory().create()
        se.create_mapping('entity', resource_type_id, mapping=mapping)
        
    @staticmethod
    def get_report(resourceid):
        # get resource data for resource_id from ES, return data
        # with correct id for the given resource type
        return {
            'id': 'heritage-resource',
            'data': {
                'hello_world': 'Hello World!'
            }
        }
