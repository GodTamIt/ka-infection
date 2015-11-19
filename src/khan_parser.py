from Khan import Khan, Infection, User
import re


__infection_regex__ = re.compile("(?P<indent>\\s*)(?P<name>\\w+)(\\((?P<severity>\\d+)(,\\s*(?P<contagiousness>\\d+))?\\))?")

def get_infections(khan):
	while True:
		s = input("Please enter the path to the infection file to load or press [Enter] to finish: ")

		if s is None or s == "":
			print("\n")
			return

		try:
			content = None
			with open(s, 'r') as content_file:
				content = content_file.read()
			added = __parse_infections__(content, khan)
			print("Added {} new infections, updated {} existing infections!".format(added[0], added[1]))
		except:
			print("Error: failed to parse file!")
			raise

		print("\n")


def __parse_infections__(hierarchy, khan):
	parents = []
	new_count = update_count = 0
	for line in hierarchy.splitlines():
		match = __infection_regex__.match(line)
		if match:
			indent = match.group('indent').count("\t") * 4 + match.group('indent').count(' ')
			while len(parents) > 0 and indent <= parents[-1][1]:
				parents.pop()

			is_new = khan.add_infection(match.group('name'), None if len(parents) < 1 else parents[-1][0], match.group('severity'), match.group('contagiousness'))
			if is_new:
				new_count += 1
			else:
				update_count += 1

			parents.append((match.group('name'), indent))

	return (new_count, update_count)
