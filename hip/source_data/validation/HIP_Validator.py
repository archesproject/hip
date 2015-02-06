def test_group(group, group_list, test_set):
	original_length = len(test_set)
	l = test_set - group_list
	if len(l) == original_length or len(l) == 0:
		pass
	else:
		print group_list


def validate_groups(resource):
	begin_existence_set = set(['BEGINNING_OF_EXISTENCE_TYPE.E55', 'START_DATE_OF_EXISTENCE.E49'])
	end_existence_set = set(['END_OF_EXISTENCE_TYPE.E55', 'END_DATE_OF_EXISTENCE.E49'])


	for group in resource.groups:
		group_list = set()
		for row in group.rows:
			group_list.add(row.attributename)

		test_group(group, group_list, begin_existence_set)
		test_group(group, group_list, end_existence_set)


def validate_resource(resource):
	# validate_groups(resource)
	pass

if __name__ == "__main__":
	main()
