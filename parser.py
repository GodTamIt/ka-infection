from Khan import Khan, Infection, User
import re


__infection_regex__ = re.compile("(?P<Indent>\\s*)(?P<Name>\\w+)(\\((?P<Severity>\\d+)(,\\s*(?P<Contagiousness>\\d+))?\\))?")

def get_infections():
	while True:
		s = input("Please enter the path to the infection file to load or press [Enter] to finish: ")

		if s == "":
			print("\n")
			return

		try:
			content = None
			with open(s, 'r') as content_file:
				content = content_file.read()
			__parse_infections__(content)
		except:
			print("Error: failed to parse file!")

		print("\n")


def __parse_infections__(hierarchy):
	parents = []

	for line in hierarchy.splitlines():
		print(line)
