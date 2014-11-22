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
from datetime import datetime
import uuid
import types
from arches.app.models.entity import Entity as ArchesEntity
import arches.app.models.models as archesmodels
from arches.app.models.models import RelatedResource
from arches.app.models.models import Concepts
from arches.app.models.models import Values
from arches.app.models.concept import Concept
from django.db.models import Q
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import fromstr
from django.db import connection
from django.db import transaction
from arches.app.models.search import SearchResult, MapFeature
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
import datetime


class Entity(ArchesEntity):
    """ 
    Used for mapping complete entity graph objects to and from the database

    """
    def __init__(self, *args, **kwargs):
        self.label = None
        self.businesstablename = None
        super(Entity, self).__init__(*args, **kwargs)


    def get(self, pk, parent=None, showlabels=False):
        """
        Gets a complete entity graph for a single entity instance given an entity id
        If a parent is given, will attempt to lookup the rule used to relate parent to child

        if showlabels = True, then concept uuids and related asset uuids will be replaced with their
        labels or primary display names respectively

        """

        entity = archesmodels.Entities.objects.get(pk = pk)
        self.entitytypeid = entity.entitytypeid_id
        self.entityid = entity.pk
        self.businesstablename = entity.entitytypeid.businesstablename
        
        # get the entity value if any
        if entity.entitytypeid.businesstablename != None:
            themodel = self._get_model(entity.entitytypeid.businesstablename)
            themodelinstance = themodel.objects.get(pk = pk)
            columnname = entity.entitytypeid.getcolumnname()

            if (isinstance(themodelinstance, archesmodels.Domains)): 
                self.value = themodelinstance.getlabelid()
                self.label = themodelinstance.getlabelvalue()
            elif (isinstance(themodelinstance, archesmodels.Files)): 
                self.label = themodelinstance.getname()
                self.value = themodelinstance.geturl() 
            else:
                self.value = getattr(themodelinstance, columnname, 'Entity %s could not be found in the table %s' % (pk, entity.entitytypeid.businesstablename))                   
                
        # get the property that related parent to child
        if parent is not None:
            relation = archesmodels.Relations.objects.get(entityiddomain =  parent.entityid, entityidrange = entity.entityid)
            self.property = relation.ruleid.propertyid_id                
        
        # get the related entities if any
        relatedentities = archesmodels.Relations.objects.filter(entityiddomain = pk)
        for relatedentity in relatedentities:       
            self.append_child(Entity().get(relatedentity.entityidrange_id, entity, showlabels))

        return self

    def save(self, username='', note=''):
        """
        Saves an entity back to the db wrapped in a transaction
        We can't simply apply the decorator to the _save method 
        because of the recursive nature of the save process

        """
        super(Entity, self).save(username, note)

        # if this resource has related resources, then make those connections now 
        # from related resources back to us
        for arches_resources in self.find_entities_by_type_id('ARCHES RESOURCE.E1'):
            self.add_related_asset(arches_resources)

        return self

    def delete(self, username='', note='', delete_root=False):
        """
        Deltes an entity from the db wrapped in a transaction 
        """

        timestamp = datetime.datetime.now()
        for entity in self.flatten():
            if entity.value != '':
                edit = archesmodels.EditLog()        
                edit.editlogid = str(uuid.uuid4())
                edit.resourceentitytypeid = self.entitytypeid
                edit.resourceid = self.entityid
                edit.attributeentitytypeid = entity.entitytypeid
                edit.edittype = 'delete'
                edit.userid = username
                edit.timestamp = timestamp
                edit.oldvalue = None
                edit.newvalue = entity.value
                edit.user_firstname = username
                edit.user_lastname = username
                edit.note = note
                edit.save()

        self.delete_all_resource_relationships()
        self._delete(delete_root)

    def _delete(self, delete_root=False):
        """
        Deletes this entity and all it's children.  
        Also attempts to delete the highest parent (and any nodes on the way) of this node when I'm the only child and 
        my parent has no value.

        if delete_root is False prevent the root node from deleted

        """

        nodes_to_delete = []

        # gather together a list of all entities that includes self and all its children
        def gather_entities(entity):
            nodes_to_delete.append(entity)
        self.traverse(gather_entities)

        # delete any related assests first
        for entity in nodes_to_delete:
            if entity.entitytypeid == 'ARCHES RESOURCE.E1':
                entity.delete_related_asset(entity)
        
        # delete the remaining entities
        for entity in nodes_to_delete:         
            self_is_root = entity.get_rank() == 0

            if self_is_root and delete_root:
                dbentity = archesmodels.Entities.objects.get(pk = entity.entityid)
                #print 'deleting root: %s' % dbentity
                dbentity.delete()
            else:
                parent = entity.get_parent()
                parent_is_root = parent.get_rank() == 0              
                #print 'deleting: %s' % entity
                dbentity = archesmodels.Entities.objects.filter(pk = entity.entityid)
                if len(dbentity) == 1:
                    dbentity[0].delete()
                    parent.relatedentities.remove(entity)
                    #print 'deleted: %s' % dbentity[0]
            
                # now try and remove this entity's parent 
                if len(parent.relatedentities) == 1 and parent.value == '' and not parent_is_root:
                    parent._delete() 

    def load(self, E):
        """
        Populate an Entity instance from a generic python object 

        """

        self.label = E.get('label', '')
        self.businesstablename = E.get('businesstablename', '')
        super(Entity, self).load(E)

    def add_related_asset(self, resource_node):
        """
        Adds a related asset to this entity

        """

        id_of_asset_to_x_reference = resource_node.value
        node_in_common = resource_node.relatedentities[0]
        related_asset_entity = Entity().get(id_of_asset_to_x_reference)
        if self.is_already_x_referenced(node_in_common, related_asset_entity) == False:       
            rule = archesmodels.Rules.objects.get(entitytypedomain = related_asset_entity.entitytypeid, entitytyperange = 'ARCHES RESOURCE.E1')
            newresource = related_asset_entity.add_related_entity('ARCHES RESOURCE.E1', rule.propertyid_id, self.entityid, '')
            newdbresrouce = newresource._save()
            newrelationship = archesmodels.Relations()
            newrelationship.entityiddomain = archesmodels.Entities.objects.get(pk = id_of_asset_to_x_reference)
            newrelationship.entityidrange = newdbresrouce
            newrelationship.ruleid = rule
            newrelationship.save()
            
            rule = archesmodels.Rules.objects.get(entitytypedomain = 'ARCHES RESOURCE.E1', entitytyperange = node_in_common.entitytypeid)
            newrelationship = archesmodels.Relations()
            newrelationship.entityiddomain = newdbresrouce
            newrelationship.entityidrange = archesmodels.Entities.objects.get(pk = node_in_common.entityid)
            newrelationship.ruleid = rule
            newrelationship.save()

            related_asset_entity.index()
            
    def delete_related_asset(self, resource_node):
        """
        Deletes a related asset from this entity
        
        """

        related_asset_entity = Entity().get(resource_node.value) 
        for xref_node in related_asset_entity.find_entities_by_type_id('ARCHES RESOURCE.E1'):
            if xref_node.relatedentities[0].equals(resource_node.relatedentities[0]):
                entity = archesmodels.Entities.objects.filter(pk = xref_node.entityid)
                if len(entity) == 1:
                    entity[0].delete()
                return




    def create_resource_relationship(self, related_resource_id, reason=None, date_started=None, date_ended=None, relationship_type_id=None):
        """
        Creates a from this entity to another entity. 
        
        """
        print 'CREATING RELATIONSHIP WITH', self.entityid, related_resource_id
        relationship = RelatedResource(
                entityid1 = self.entityid,
                entityid2 = related_resource_id,
                reason = reason,
                relationshiptype = relationship_type_id,
                datestarted = date_started,
                dateended = date_ended,
                )

        relationship.save()


    def delete_all_resource_relationships(self):
        """
        Deletes all relationships to other resources. 
        
        """        
        relationships = RelatedResource.objects.filter( Q(entityid2=self.entityid)|Q(entityid1=self.entityid) )

        for relationship in relationships:
            relationship.delete()


    def delete_resource_relationship(self, related_resource_id, relationship_type_id=None):
        """
        Deletes the relationships from this entity to another entity. 
        
        """        

        if relationship_type:
            relationships = RelatedResource.objects.filter( Q(entityid2=self.entityid)|Q(entityid1=self.entityid), Q(entityid2=related_resource_id)|Q(entityid1=related_resource_id), Q(relationshiptype=relationship_type_id))
        else:
            relationships = RelatedResource.objects.filter( Q(entityid2=self.entityid)|Q(entityid1=self.entityid), Q(entityid2=related_resource_id)|Q(entityid1=related_resource_id) )

        for relationship in relationships:
            relationship.delete()


    def get_related_resources(self, entitytypeid=None, showlabels=False, fromdate=datetime.date(1,1,1), todate=datetime.date.today(), relationship_type_id=None, relationship_type_label=None, return_entities=True):
        """
        Gets a list of entities related to this entity, optionaly takes in an entitytypeid and relationship type to return just 
        related entities of that type and/or relationship type. Setting return_entities to False will return the relationship records 
        rather than the related entities. This is useful in cases where you only need the information about the relationship, 
        but want to avoid the overhead of creating entities.

        """
        ret = []

        if self.entityid:

            if relationship_type_id:
                relationships = RelatedResource.objects.filter(Q(entityid2=self.entityid)|Q(entityid1=self.entityid), Q(relationshiptype=relationship_type_id))
            else:
                relationships = RelatedResource.objects.filter(Q(entityid2=self.entityid)|Q(entityid1=self.entityid))
      
            for relationship in relationships: 
                if relationship.entityid1 != self.entityid:
                    relationshipid = relationship.entityid1
                else:
                    relationshipid = relationship.entityid2

                entity_obj = archesmodels.Entities.objects.get(pk = relationshipid)

                if relationship_type_label and relationship.relationshiptype:

                    relationship_type_entity = archesmodels.Values.objects.get(pk = relationship.relationshiptype)
                    if relationship_type_label == relationship_type_entity.value:
                        relationship_type_id = relationship.relationshiptype
                        if (entitytypeid == None or entity_obj.entitytypeid_id == entitytypeid):
                            foundentity = Entity().get(relationshipid, showlabels=showlabels)
                            if return_entities:
                                ret.append(foundentity)
                            else:
                                ret.append(relationship)

                else:
                    if (entitytypeid == None or entity_obj.entitytypeid_id == entitytypeid) and (relationship_type_id == None or relationship_type_id == relationship.relationshiptype):
                        foundentity = Entity().get(relationshipid, showlabels=showlabels)
                        if return_entities == True:
                            ret.append(foundentity)
                        else:
                            ret.append(relationship)

        return ret


    def is_already_x_referenced(self, xref_to_check, xref_entity):
        """
        A check to see if xref_to_check is already related to xref_entity
        
        """

        xrefs = xref_entity.find_entities_by_type_id('ARCHES RESOURCE.E1')
        for xref in xrefs:
            if xref.relatedentities[0].equals(xref_to_check):
                return True

        return False

    def find_entities_by_type_id(self, entitytypeid):
        """
        Gets a list of entities within this instance of a given type

        """
        ret = []        
        # try:
        #     #print 'trying: %s' % entitytypeid
        #     ret = self._obj[entitytypeid]
        #     #print 'getting=%s' % self._obj[entitytypeid]
        # except:
        #     def appendValue(entity):
        #         try:
        #             self._obj[entity.entitytypeid].append(entity)
        #         except:
        #             try:
        #                 self._obj
        #             except:
        #                 self._obj = {}
        #             self._obj[entity.entitytypeid] = []
        #             self._obj[entity.entitytypeid].append(entity)

        #         if entity.entitytypeid == entitytypeid:
        #             ret.append(entity)
                    
        #     #if self.valid_entity_type_id(entitytypeid):
        #     #print 'self: %s' % self
        #     self.traverse(appendValue)

        def appendValue(entity):
            if entity.entitytypeid == entitytypeid:
                ret.append(entity)
                    
        self.traverse(appendValue)        
        return ret

    
    def add_related_entity(self, entitytypeid, property, value, entityid):
        """
        Add a related entity to this entity instance

        """     
        entity_type = archesmodels.EntityTypes.objects.get(entitytypeid = entitytypeid)
        node = Entity()
        node.property = property
        node.entitytypeid = entitytypeid
        node.businesstablename = entity_type.businesstablename
        node.value = value
        node.entityid = entityid
        
        self.append_child(node)
        return node


    def get_primary_display_name(self):
        """
        Gets the human readable name to display for entity instances

        """

        pname_key = 'default'
        if self.entitytypeid in settings.PRIMARY_DISPLAY_NAME_LOOKUPS:
            pname_key = self.entitytypeid

        entitytype_of_primaryname = archesmodels.EntityTypes.objects.get(pk = settings.PRIMARY_DISPLAY_NAME_LOOKUPS[pname_key]['entity_type'])
        displayname = []

        if self.entitytypeid == 'HERITAGE_RESOURCE.E18':
            names = self.get_root().find_entities_by_type_id(entitytype_of_primaryname)
            if len(names) > 0:
                for name in names:
                    displayname.append(name)

        return displayname


    def get_e55_concept_label(self, e55_type, id):
        concept = archesmodels.EntityTypes.objects.get(pk = e55_type).conceptid
        concept_graph = Concept().get(id=concept.pk, include_subconcepts=True, include=['label'])
        result = ''
        if len(concept_graph.subconcepts) > 0:
            for subconcept in concept_graph.subconcepts[0].subconcepts:
                for label in subconcept.values:
                    if label.id == id:
                        result = label.value
        return result

    # def get_district(self):
    #     """
    #     Gets the district number given a project, document, or mitgation entity

    #     """

    #     def get_district_from_project(project):
    #         districts = project.find_entities_by_type_id('CALTRANS DISTRICT.E55')
    #         if len(districts) > 0:
    #             return project.get_e55_concept_label('CALTRANS DISTRICT.E55', districts[0].value)
    #         return None

    #     def get_district_from_document(document):
    #         projects = document.get_related_resources('PROJECT.E27')
    #         for project in projects:
    #             return get_district_from_project(project)

    #     def get_district_from_mitigation(mitgation):
    #         documents = mitgation.get_related_resources('IGR DOCUMENT.E31')
    #         for document in documents:
    #             return get_district_from_document(document)

    #     if self.entitytypeid == 'PROJECT.E27':
    #         return get_district_from_project(self)
    #     elif self.entitytypeid == 'IGR DOCUMENT.E31':
    #         return get_district_from_document(self)
    #     elif self.entitytypeid == 'MITIGATION.E7':
    #         return get_district_from_mitigation(self)

    # def index(self):
    #     """
    #     Gets a SearchResult object for a given asset entity
    #     Used for populating the search index with searchable entity information

    #     """

            
    #     if self.get_rank() == 0:
    #         se = SearchEngineFactory().create()
    #         search_result = {}
    #         search_result['entityid'] = self.entityid
    #         search_result['entitytypeid'] = self.entitytypeid  
    #         search_result['appelations'] = []
    #         search_result['geometries'] = []
    #         search_result['concepts'] = []

    #         term_entities = []

    #         names = []
    #         for name in self.get_primary_display_name():
    #             names.append(name.value)

    #         primary_display_name = ' '.join(names)

    #         for enititytype in settings.SEARCHABLE_ENTITY_TYPES:
    #             for entity in self.find_entities_by_type_id(enititytype):
    #                 search_result['appelations'].append(entity.value)
    #                 term_entities.append(entity)


    #         for geom_entity in self.find_entities_by_type_id(settings.ENTITY_TYPE_FOR_MAP_DISPLAY):
    #             search_result['geometries'].append(fromstr(geom_entity.value).json)
    #             mapfeature = MapFeature()
    #             mapfeature.geomentityid = geom_entity.entityid
    #             mapfeature.entityid = self.entityid
    #             mapfeature.entitytypeid = self.entitytypeid
    #             mapfeature.primaryname = primary_display_name
    #             mapfeature.geometry = geom_entity.value
    #             mapfeature.address_number = self.find_entities_by_type_id("ADDRESS_NUMBER IN ROAD OR STREET.E45")[0].value if len(self.find_entities_by_type_id("ADDRESS_NUMBER IN ROAD OR STREET.E45")) > 0 else ''
    #             mapfeature.street_name = self.find_entities_by_type_id("ADDRESS_ROAD OR STREET NAME.E45")[0].value if len(self.find_entities_by_type_id("ADDRESS_ROAD OR STREET NAME.E45")) > 0 else ''
    #             mapfeature.city = self.find_entities_by_type_id("ADDRESS_TOWN_CITY.E55")[0].label if len(self.find_entities_by_type_id("ADDRESS_TOWN_CITY.E55")) > 0 else ''
    #             mapfeature.post_code = self.find_entities_by_type_id("ADDRESS_POSTCODE.E45")[0].value if len(self.find_entities_by_type_id("ADDRESS_POSTCODE.E45")) > 0 else ''
    #             mapfeature.county = self.find_entities_by_type_id("ADDRESS_COUNTY.E55")[0].label if len(self.find_entities_by_type_id("ADDRESS_COUNTY.E55")) > 0 else ''
    #             mapfeature.name = self.find_entities_by_type_id("PROJECT NAME.E41")[0].value if len(self.find_entities_by_type_id("PROJECT NAME.E41")) > 0 else ''
    #             mapfeature.coordinating_district = self.find_entities_by_type_id("COORDINATING DISTRICT.E55")[0].label if len(self.find_entities_by_type_id("COORDINATING DISTRICT.E55")) > 0 else ''
    #             staff_contacts = self.get_related_resources("DISTRICT STAFF.E21")
    #             if staff_contacts:
    #                 mapfeature.staff_contact = {}
    #                 mapfeature.staff_contact["first_name"] = staff_contacts[0].find_entities_by_type_id("DISTRICT STAFF FIRST NAME.E82")[0].value if len(staff_contacts[0].find_entities_by_type_id("DISTRICT STAFF FIRST NAME.E82")) > 0 else ''
    #                 mapfeature.staff_contact["last_name"] = staff_contacts[0].find_entities_by_type_id("DISTRICT STAFF LAST NAME.E82")[0].value if len(staff_contacts[0].find_entities_by_type_id("DISTRICT STAFF LAST NAME.E82")) > 0 else ''
    #                 mapfeature.staff_contact["phone_number"] = staff_contacts[0].find_entities_by_type_id("DISTRICT STAFF PHONE NUMBER.E1")[0].value if len(staff_contacts[0].find_entities_by_type_id("DISTRICT STAFF PHONE NUMBER.E1")) > 0 else ''
    #                 mapfeature.staff_contact["email"] = staff_contacts[0].find_entities_by_type_id("DISTRICT STAFF EMAIL.E1")[0].value if len(staff_contacts[0].find_entities_by_type_id("DISTRICT STAFF EMAIL.E1")) > 0 else ''
    #             data = JSONSerializer().serializeToPython(mapfeature, ensure_ascii=True, indent=4)
    #             se.index_data('maplayers', self.entitytypeid, data, idfield='geomentityid')


    #         district = self.get_district()

    #         if self.entitytypeid == 'PROJECT.E27':
    #             project_name = self.find_entities_by_type_id('PROJECT NAME.E41')[0].value
    #             project_for_simple_search = {
    #                 'project_entityid': self.entityid,
    #                 'entityid': self.entityid,
    #                 'district': district,
    #                 'values':[project_name] 
    #             }

    #             data = JSONSerializer().serializeToPython(project_for_simple_search, ensure_ascii=True, indent=4)
    #             se.index_data('resources', self.entitytypeid, data, idfield='entityid')
    #             related = self.get_related_resources('IGR DOCUMENT.E31')

    #             for resource in related:
    #                 document_for_simple_search = {
    #                     'project_entityid': self.entityid,
    #                     'entityid': resource.entityid,
    #                     'district': district,
    #                     'values':[resource.find_entities_by_type_id('SCH NUMBER.E1')[0].value] 
    #                 }
                    
    #                 data = JSONSerializer().serializeToPython(document_for_simple_search, ensure_ascii=True, indent=4)
    #                 se.index_data('resources', resource.entitytypeid, data, idfield='entityid')
                        


            # for entitytype in ('PROJECT NAME.E41','SCH NUMBER.E1'):
            #     for entity in self.find_entities_by_type_id(entitytype):
            #         resource_for_simple_search['values'].append(entity.value)
            #         print self.entityid, entitytype, resource_for_simple_search['values']
            #     data = JSONSerializer().serializeToPython(resource_for_simple_search, ensure_ascii=True, indent=4)
            #     se.index_data('resources', self.entitytypeid, data, idfield='entityid')
                    

            # def to_int(s):
            #     try:
            #         return int(s)
            #     except ValueError:
            #         return ''

            # def inspect_node(entity):
            #     if entity.entitytypeid[-3:] == 'E55':
            #         if entity.value != '':
            #             label = archesmodels.Values.objects.filter(pk = entity.value)
            #             if len(label) > 0:
            #                 search_result['concepts'].append(label[0].conceptid_id)
                
            #     if entity.entitytypeid in settings.ADV_SEARCHABLE_ENTITY_TYPES or entity.entitytypeid in settings.SEARCHABLE_ENTITY_TYPES:
            #         if entity.entitytypeid not in search_result:
            #             search_result[entity.entitytypeid] = []

            #         if entity.entitytypeid in settings.ENTITY_TYPE_FOR_MAP_DISPLAY:
            #             search_result[entity.entitytypeid].append(JSONDeserializer().deserialize(fromstr(entity.value).json))
            #         elif entity.entitytypeid == 'PHASE TYPE ASSIGNMENT.E17':
            #             labeledentity = Entity().get(entity.entityid, showlabels=True)
            #             fromdate = labeledentity.find_entities_by_type_id('FROM DATE.E49')
            #             todate = labeledentity.find_entities_by_type_id('TO DATE.E49')
            #             period = labeledentity.find_entities_by_type_id('CULTURAL PERIOD.E55')
            #             heritagetype = labeledentity.find_entities_by_type_id(self.entitytypeid[0:-4] + ' TYPE.E55')
            #             search_result[entity.entitytypeid].append({
            #                 'from': to_int(fromdate[0].value) if len(fromdate) > 0 else '', 
            #                 'to': to_int(todate[0].value) if len(todate) > 0 else '',
            #                 'period': period[0].value if len(period) > 0 else '',
            #                 'type': heritagetype[0].value if len(heritagetype) > 0 else ''
            #             })
            #         else:
            #             search_result[entity.entitytypeid].append(entity.value)

            # se.create_mapping('term', 'value', 'ids', 'string', 'not_analyzed')
            
            # mapping =  { 
            #     self.entitytypeid : {
            #         'properties' : {
            #             'entityid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #             'parentid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #             'property' : {'type' : 'string', 'index' : 'not_analyzed'},
            #             'entitytypeid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #             'businesstablename' : {'type' : 'string', 'index' : 'not_analyzed'},
            #             'value' : {'type' : 'string', 'index' : 'analyzed'},
            #             'relatedentities' : { 
            #                 'type' : 'nested', 
            #                 'index' : 'analyzed',
            #                 'properties' : {
            #                     'entityid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'parentid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'property' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'entitytypeid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'businesstablename' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'value' : {
            #                         'type' : 'string',
            #                         'index' : 'analyzed',
            #                         'fields' : {
            #                             'raw' : { 'type' : 'string', 'index' : 'not_analyzed'}
            #                         }
            #                     }
            #                 }
            #             },
            #             'geometries' : { 
            #                 'type' : 'nested', 
            #                 'index' : 'analyzed',
            #                 'properties' : {
            #                     'entityid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'parentid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'property' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'entitytypeid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'businesstablename' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'value' : {
            #                         "type": "geo_shape"
            #                     }
            #                 }
            #             },
            #             'dates' : { 
            #                 'type' : 'nested', 
            #                 'index' : 'analyzed',
            #                 'properties' : {
            #                     'entityid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'parentid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'property' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'entitytypeid' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'businesstablename' : {'type' : 'string', 'index' : 'not_analyzed'},
            #                     'value' : {
            #                         "type" : "date"
            #                     }
            #                 }
            #             }
            #         }
            #     }
            # }
            # se.create_mapping('entity', self.entitytypeid, mapping=mapping)

            # # add district number to the base mapping
            # mapping =  { 
            #     self.entitytypeid : {
            #         'properties' : {
            #             'district' : {'type' : 'integer', 'index' : 'not_analyzed'}
            #         }
            #     }
            # }
            # se.create_mapping('entity', self.entitytypeid, mapping=mapping)

            # def index_terms(entity):
            #     dbentity = archesmodels.Entities.objects.get(pk=entity.entityid)
            #     businesstablename = dbentity.entitytypeid.businesstablename
            #     entity.businesstablename = businesstablename
            #     if businesstablename == 'strings':
            #         if len(entity.value.split(' ')) < 10:
            #             se.index_term(entity.value, entity.entityid, options={'context': entity.entitytypeid})
            #     elif businesstablename == 'domains':
            #         domain = archesmodels.Domains.objects.get(pk=dbentity.entityid)
            #         if domain.val:
            #             concept = Concept({'id': domain.val.conceptid.pk}).get(inlude=['label'])
            #             if concept:
            #                 auth_pref_label = ''
            #                 auth_doc_concept = concept.get_auth_doc_concept()
            #                 if auth_doc_concept:
            #                     auth_pref_label = auth_doc_concept.get_preflabel().value
            #                 se.index_term(concept.get_preflabel().value, entity.entityid, options={'context': auth_pref_label, 'conceptid': domain.val.conceptid_id})
            #     elif businesstablename == 'geometries':
            #         entity.value = JSONDeserializer().deserialize(fromstr(entity.value).json)
            #         pass
            #     elif businesstablename == 'dates':
            #         pass
            #     elif businesstablename == 'numbers':
            #         pass
            #     elif businesstablename == 'files':
            #         pass
            #     return businesstablename


            # flattend_entity = self.flatten()
            # root_entity = self
            # root_entity.district = district
            # root_entity.relatedentities = []
            # root_entity.dates = []
            # root_entity.geometries = []
            # for entity in flattend_entity:
            #     businesstablename = index_terms(entity)
            #     if entity.entityid != self.entityid:
            #         try:
            #             del entity.relatedentities
            #         except: pass
            #         if businesstablename == 'dates':
            #             root_entity.dates.append(entity)
            #         elif businesstablename == 'geometries':
            #             root_entity.geometries.append(entity)
            #         else:
            #             root_entity.relatedentities.append(entity)

            # se.index_data('entity', root_entity.entitytypeid, JSONSerializer().serializeToPython(root_entity, ensure_ascii=True), idfield=None, id=root_entity.entityid)

            # #self.traverse(inspect_node)

            # # create ES mappings (need to do this well before you try and use the mapping otherwise you may get a NoShardAvailableActionException)
            # # se.create_mapping('term', 'value', 'entityids', 'string', 'not_analyzed')
            # # for entitytype, value in search_result.iteritems():
            # #     if entitytype in settings.ADV_SEARCHABLE_ENTITY_TYPES or entitytype in settings.SEARCHABLE_ENTITY_TYPES:
            # #         if entitytype in settings.ENTITY_TYPE_FOR_MAP_DISPLAY:
            # #             se.create_mapping('entity', self.entitytypeid, entitytype, 'geo_shape') 
            # #         elif entitytype == 'PHASE TYPE ASSIGNMENT.E17':
            # #             se.create_mapping('entity', self.entitytypeid, entitytype, fieldtype='nested')
            # #         else:                   
            # #             try:
            # #                 uuid.UUID(value[0])
            # #                 # SET FIELDS WITH UUIDS TO BE "NOT ANALYZED" IN ELASTIC SEARCH
            # #                 se.create_mapping('entity', self.entitytypeid, entitytype, 'string', 'not_analyzed')
            # #             except(ValueError):
            # #                 pass

            # #             search_result[entitytype] = list(set(search_result[entitytype]))

            # # # index the data
            # # search_result['concepts'] = list(set(search_result['concepts']))
            # # data = JSONSerializer().serializeToPython(search_result, ensure_ascii=True, indent=4)
            # # se.index_data('entity', self.entitytypeid, data, idfield=None, id=self.entityid)

            
            # mapping =  { 
            #     self.entitytypeid : {
            #         'properties' : {
            #             'value' : { 
            #                 'type' : 'string'
            #             },
            #             'relatedentities' : { 
            #                 'type' : 'nested', 
            #                 'index' : 'analyzed',
            #                 'properties' : {
            #                     'value' : { 
            #                         'type' : 'string'
            #                     },
            #                     'relatedentities' : { 
            #                         'type' : 'nested', 
            #                         'index' : 'analyzed',
            #                         'properties' : {
            #                             'value' : { 
            #                                 'type' : 'string'
            #                             },
            #                             'relatedentities' : { 
            #                                 'type' : 'nested', 
            #                                 'index' : 'analyzed',
            #                                 'properties' : {
            #                                     'value' : { 
            #                                         'type' : 'string'
            #                                     },
            #                                     'relatedentities' : { 
            #                                         'type' : 'nested', 
            #                                         'index' : 'analyzed',
            #                                         'properties' : {
            #                                             'value' : { 
            #                                                 'type' : 'string'
            #                                             },
            #                                             'relatedentities' : { 
            #                                                 'type' : 'nested', 
            #                                                 'index' : 'analyzed',
            #                                                 'properties' : {
            #                                                     'value' : { 
            #                                                         'type' : 'string'
            #                                                     },
            #                                                     'relatedentities' : { 
            #                                                         'type' : 'nested', 
            #                                                         'index' : 'analyzed',
            #                                                         'properties' : {

            #                                                         }
            #                                                     }
            #                                                 }
            #                                             }
            #                                         }
            #                                     }

            #                                 }
            #                             }
            #                         }
            #                     }
            #                 }
            #             }
            #         }
            #     }
            # }

            # # se.index_data(index='entity_nested', type=self.entitytypeid, data=mapping, id='_mapping')
            # # se.index_data('entity_nested', self.entitytypeid, JSONSerializer().serializeToPython(self, ensure_ascii=True, indent=4), idfield=None, id=self.entityid)
            
            # mapping =  { 
            #     self.entitytypeid : {
            #         'properties' : {
            #             'value' : { 
            #                 'type' : 'string'
            #             },
            #             'relatedentities' : { 
            #                 'type' : 'object', 
            #                 'index' : 'analyzed',
            #                 'properties' : {
            #                     'value' : { 
            #                         'type' : 'string'
            #                     },
            #                     'relatedentities' : { 
            #                         'type' : 'object', 
            #                         'index' : 'analyzed',
            #                         'properties' : {
            #                             'value' : { 
            #                                 'type' : 'string'
            #                             },
            #                             'relatedentities' : { 
            #                                 'type' : 'object', 
            #                                 'index' : 'analyzed',
            #                                 'properties' : {
            #                                     'value' : { 
            #                                         'type' : 'string'
            #                                     },
            #                                     'relatedentities' : { 
            #                                         'type' : 'object', 
            #                                         'index' : 'analyzed',
            #                                         'properties' : {
            #                                             'value' : { 
            #                                                 'type' : 'string'
            #                                             },
            #                                             'relatedentities' : { 
            #                                                 'type' : 'object', 
            #                                                 'index' : 'analyzed',
            #                                                 'properties' : {
            #                                                     'value' : { 
            #                                                         'type' : 'string'
            #                                                     },
            #                                                     'relatedentities' : { 
            #                                                         'type' : 'object', 
            #                                                         'index' : 'analyzed',
            #                                                         'properties' : {
            #                                                             'value' : { 
            #                                                                 'type' : 'string'
            #                                                             },
            #                                                             'relatedentities' : { 
            #                                                                 'type' : 'object', 
            #                                                                 'index' : 'analyzed',
            #                                                                 'properties' : {

            #                                                                 }
            #                                                             }
            #                                                         }
            #                                                     }
            #                                                 }
            #                                             }
            #                                         }
            #                                     }
            #                                 }
            #                             }
            #                         }
            #                     }
            #                 }
            #             }
            #         }
            #     }
            # }
            # # se.index_data(index='entity_full', type=self.entitytypeid, data=mapping, id='_mapping')
            # # se.index_data('entity_full', self.entitytypeid, JSONSerializer().serializeToPython(self, ensure_ascii=True, indent=4), idfield=None, id=self.entityid)
            
            # #se.index_terms(term_entities)

            # return search_result 