from collections import deque

class User:
	def __init__(self, name):
		self.name = name
		self.parents = set()
		self.children = set()
		self.infections = set()

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.name == other.name

	def __hash__(self):
		return hash(self.name)

class Infection:
	def __init__(self, name):
		self.name = str(name)
		self.parents = set()
		self.children = set()
		self.diseased = False
		self.__severity__ = 50
		self.__contagiousness__ = 25

	def get_severity(self):
		return self.__severity__

	def set_severity(self, severity):
		if severity is not None:
			self.__severity__ = min(max(int(severity), 0), 100)

	def get_contagiousness(self):
		return self.__contagiousness__

	def set_contagiousness(self, contagiousness):
		if contagiousness is not None:
			self.contagiousness = min(max(int(contagiousness), 0), 100)

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.name == other.name

	def __hash__(self):
		return hash(self.name)

class Khan:
	def __init__(self):
		self._users = {}
		self._infections = {}

	def add_infection(self, name, parent_name=None, severity=None, contagiousness=None):
		cur = self._infections.get(name)
		is_new = cur is None

		if is_new:
			cur = Infection(name)
			self._infections[name] = cur

		cur.set_severity(severity)
		cur.set_contagiousness(contagiousness)

		if parent_name is not None:
			parent = self._infections.get(parent_name)
			if parent is None:
				raise ValueError("Parent with name '{}' does not exist!".format(parent_name))

			# Add parent to infection's list of parents
			cur.parents.add(parent)
			# Add infection to parent's list of children
			parent.children.add(cur)

		return is_new


	def add_user(self, name, parent_name=None):
		cur = self._users.get(name)
		if cur is None:
			cur = User(name)
			self._users[name] = cur

		if parent_name is not None:
			parent = self._users.get(parent_name)
			if parent is None:
				raise ValueError("Parent with name '{}' does not exist!".format(parent_name))

			# Add parent to infection's list of parents
			cur.parents.add(parent)
			# Add infection to parent's list of children
			parent.children.add(cur)

	def infect_user(self, user_name, infection_name=None):
		infected = set()
		q = deque()

		# Get user to start infection spread
		cur = self._users.get(user_name)
		# Get infection to spread (if not None)
		infection = None if infection_name is None else self._infections.get(infection_name)

		if cur is None:
			raise ValueError("User '{}' does not exist.".format(user_name))
		elif infection_name is not None and infection is None:
			raise ValueError("Infection '{}' does not exist.".format(infection_name))

		# Add initial user to infection to-add list (queue)
		q.append(cur)

		while len(q) > 0:
			cur = q.popleft()
			if cur not in infected:
				# Infect the current user and add it to the set of infected
				infected.add(cur)
				if infection is not None:
					cur.infections.add(infection)

				# Add the parents and children to the queue
				q.extend(cur.parents)
				q.extend(cur.children)

		return infected
