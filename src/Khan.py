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

	def __str__(self):
		return self.name

class Infection:
	def __init__(self, name):
		self.name = str(name)
		self.parents = set()
		self.children = set()
		self.malevolent = False
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

	def __str__(self):
		return self.name

class Khan:
	def __init__(self):
		self.users = {}
		self.infections = {}
		self.root_users = {}
		self.root_infections = {}

	def add_infection(self, name, parent_name=None, severity=None, contagiousness=None):
		cur = self.infections.get(name)
		is_new = cur is None

		if is_new:
			cur = Infection(name)
			self.infections[name] = cur

		cur.set_severity(severity)
		cur.set_contagiousness(contagiousness)

		if parent_name is not None:
			parent = self.infections.get(parent_name)
			if parent is None:
				raise ValueError("Parent with name '{}' does not exist!".format(parent_name))

			# Add parent to infection's list of parents
			cur.parents.add(parent)
			# Add infection to parent's list of children
			parent.children.add(cur)

		if len(cur.parents) < 1:
			self.root_infections[cur.name] = cur
		else:
			self.root_infections.pop(cur.name, None)

		return is_new


	def add_user(self, name, parent_name=None):
		cur = self.users.get(name)
		is_new = cur is None

		if is_new:
			cur = User(name)
			self.users[name] = cur

		if parent_name is not None:
			parent = self.users.get(parent_name)
			if parent is None:
				raise ValueError("Parent with name '{}' does not exist!".format(parent_name))

			# Add parent to infection's list of parents
			cur.parents.add(parent)
			# Add infection to parent's list of children
			parent.children.add(cur)
			# Add all of parent's infections
			for infection in parent.infections:
				cur.infections.add(infection)

		if len(cur.parents) < 1:
			self.root_users[cur.name] = cur
		else:
			self.root_users.pop(cur.name, None)

		return is_new

	def infect_user(self, user_name, infection_name=None):
		infected = set()
		q = deque()

		# Get user to start infection spread
		cur = self.users.get(user_name)
		# Get infection to spread (if not None)
		infection = None if infection_name is None else self.infections.get(infection_name)

		if cur is None:
			return infected
			#raise ValueError("User '{}' does not exist.".format(user_name))
		elif infection_name is not None and infection is None:
			return infected
			#raise ValueError("Infection '{}' does not exist.".format(infection_name))

		# Add initial user to infection to-add list (queue)
		q.append(cur)

		while len(q) > 0:
			cur = q.popleft()
			if cur not in infected:
				# Infect the current user and add it to the set of infected
				infected.add(cur)
				if infection is not None:
					cur.infections.add(infection)
					cur.infections.update(infection.parents)

				# Add the parents and children to the queue
				q.extend(cur.parents)
				q.extend(cur.children)

		return infected

	def print_users(self, users=None, print_infections=False):
		if users is None:
			users = self.root_users.values()
		self.__print_users__(self.root_users.values(), print_infections)

	def __print_users__(self, children, print_infections, indent=0):
		for user in children:
			# Print indentation
			print("{}{}{}".format('.' * (indent * 4), user.name, '(' + ', '.join(map(str, user.infections)) + ')' if print_infections and len(user.infections) > 0 else ""))
			# Print children recursively
			self.__print_users__(user.children, print_infections, indent + 1)

	def print_infections(self, print_malevolent=False):
		self.__print_infections__(self.root_infections.values(), print_malevolent)

	def __print_infections__(self, children, print_malevolent, indent=0):
		for inf in children:
			# Print indentation
			print("{}{}{}".format('.' * (indent * 4), inf.name, "(Malevolent!)" if print_malevolent and inf.malevolent else ""))
			# Print children recursively
			self.__print_infections__(inf.children, print_malevolent, indent + 1)
