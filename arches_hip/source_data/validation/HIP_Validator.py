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

from arches.management.commands import utils


class Validation_Errors(object):
    def __init__(self, *args):
        self.group_duplicates = []
        self.paired_attribute_errors = []


validation_errors = Validation_Errors()
       

def test_paired_group(group, group_list, test_set):
	original_length = len(test_set)
	l = test_set - group_list
	if len(l) == original_length or len(l) == 0:
		pass
	else:
		test_list = list(test_set)
		append_error('{0} or {1} exists in the {2} group of the {3} resource without the other existing. Both need to exist for this group to be valid.'.format(test_list[0], test_list[1], group.group_id, group.resource_id), 'paired_attribute_errors' )


def check_paired_attributes(resource):
	begin_existence_set = set(['BEGINNING_OF_EXISTENCE_TYPE.E55', 'START_DATE_OF_EXISTENCE.E49'])
	end_existence_set = set(['END_OF_EXISTENCE_TYPE.E55', 'END_DATE_OF_EXISTENCE.E49'])
	name_set = set(['NAME.E41', 'NAME_TYPE.E55'])
	description_set = set(['DESCRIPTION.E62', 'DESCRIPTION_TYPE.E55'])
	right_set = set(['RIGHT.E30', 'RIGHT_TYPE.E55'])
	title_set = set(['TITLE.E41', 'TITLE_TYPE.E55'])
	actor_set = set(['ACTOR_APPELLATION.E82', 'NAME_TYPE.E55'])


	for group in resource.groups:
		group_list = set()
		for row in group.rows:
			group_list.add(row.attributename)

		test_paired_group(group, group_list, begin_existence_set)
		test_paired_group(group, group_list, end_existence_set)
		test_paired_group(group, group_list, description_set)
		test_paired_group(group, group_list, right_set)
		test_paired_group(group, group_list, title_set)

		if resource.entitytypeid == 'ACTOR.E39':
			test_paired_group(group, group_list, actor_set)
		else:
			test_paired_group(group, group_list, name_set)


def check_duplicates_in_group(resource):
	# Checks if there are multiple instances of any one of the entity_types listed within the same group. 
	# Each entity type listed should occur zero or one time in a group.
	entity_types = ['ACTOR_APPELLATION.E82',
					'ADDRESS_TYPE.E55',
					'COMPONENT_TYPE.E55',
					'CULTURAL_PERIOD.E55',
					'DESCRIPTION.E62',
					'DESCRIPTION_TYPE.E55',
					'EVALUATION_CRITERIA_TYPE.E55',
					'FILE_PATH.E62',
					'FROM_DATE.E49',
					'HERITAGE_RESOURCE_TYPE.E55',
					'HERITAGE_RESOURCE_USE_TYPE.E55',
					'NAME.E41',
					'NAME_TYPE.E55',
					'PLACE_ADDRESS.E45',
					'RIGHT.E30',
					'RIGHT_TYPE.E55',
					'THUMBNAIL.E62',
					'TITLE.E41',
					'TITLE_TYPE.E55',
					'TO_DATE.E49']

	for group in resource.groups:
		group_list = []
		for row in group.rows:
			group_list.append(row.attributename)
		
		for entity_type in entity_types:
			if entity_type in group_list:
				if group_list.count(entity_type) > 1:
					append_error('There is more than one instance of {0} in the {1} group of the {2} resource. There can only be one or zero occurences of {3} per group.'.format(entity_type, group.group_id, group.resource_id, entity_type), 'group_duplicates')


def append_error(text, error_type):
	error_type_list = getattr(validation_errors, error_type)
	error_type_list.append(text)


def validate_resource(resource):
	check_duplicates_in_group(resource)
	check_paired_attributes(resource)

