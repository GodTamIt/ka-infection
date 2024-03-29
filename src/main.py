from Khan import Khan, Infection, User
import re
from multiprocessing import Pool, freeze_support, Value
import glob
import sim

__infection_regex__ = re.compile("(?P<indent>\\s*)(?P<name>\\S.*?)\\s*(\\((?P<severity>\\d+)?(,\\s*(?P<contagiousness>\\d+))?\\))")
__user_regex__ = re.compile("(?P<indent>\\s*)(?P<name>\\S.*)")

def main_prompt(khan):
	while True:
		num = None
		print("\n")
		print("[1] Load infections from file.")
		print("[2] Load users from file.")
		print("[3] Infect a user with a disease (total_infection).")
		print("[4] Infect at most a certain amount of users if possible (limited_infection).")
		print("[5] Infect exactly a certain amount of users if possible (limited_infection_perfect).")
		print("[6] Simulate real-time user-infection interaction.")
		print("[7] Print the infection hierarchy.")
		print("[8] Print the user hierarchy and each user's associated infections.")
		print("[9] Reset all users and infections to defaults.")
		print("[10] Clear all users and infections.")
		print("[11] Exit.")


		try:
			num = int(input("Please select an action to perform: "))
		except:
			pass

		print("")

		if num == 1:
			get_infections(khan)
		elif num == 2:
			get_users(khan)
		elif num == 3:
			total_infection(khan)
		elif num == 4:
			limited_infection(khan)
		elif num == 5:
			limited_infection_perfect(khan)
		elif num == 6:
			sim.simulate(khan)
		elif num == 7:
			print("***** Infections *****")
			khan.print_infections(True)
		elif num == 8:
			print("***** Users *****")
			khan.print_users(print_infections=True)
		elif num == 9:
			reset(khan)
		elif num == 10:
			clear(khan)
		elif num == 11:
			print("Goodbye!")
			return
		else:
			print("Please enter a valid number!")


def get_infections(khan):
	s = input("Please enter the path to the infection file to load: ")

	print("")

	try:
		content = None
		with open(s, 'r') as content_file:
			content = content_file.read()
		added = __parse_infections__(content, khan)
		print("Added {} new infections, updated {} existing infections!".format(added[0], added[1]))
	except:
		print("Error: failed to parse file!")

	print("")

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

def get_users(khan):
	s = input("Please enter the path to the user file to load: ")

	print("")

	try:
		content = None
		with open(s, 'r') as content_file:
			content = content_file.read()
		added = __parse_users__(khan, content)
		print("Added {} new user(s), updated {} existing user(s)!\n".format(added[0], added[1]))
	except:
		print("Error: failed to parse file!\n")

	print("")


def __parse_users__(khan, hierarchy):
	parents = []
	new_count = update_count = 0
	for line in hierarchy.splitlines():
		match = __user_regex__.match(line)
		if match:
			indent = match.group('indent').count("\t") * 4 + match.group('indent').count(' ')
			while len(parents) > 0 and indent <= parents[-1][1]:
				parents.pop()

			is_new = khan.add_user(match.group('name'), None if len(parents) < 1 else parents[-1][0])
			if is_new:
				new_count += 1
			else:
				update_count += 1

			parents.append((match.group('name'), indent))

	return (new_count, update_count)

def total_infection(khan):
	while True:
		user = input("Please enter the name of the user to infect: ")

		if user is None or user == "":
			return

		if (user not in khan.users):
			print("The user '{}' could not found!".format(user))
		else:
			break

	print("")

	while True:
		infection = input("Please enter the name of the infection to infect with or press [Enter] to simulate infection: ")

		if infection is None or infection == "":
			infection = None
			break

		if (infection not in khan.infections):
			print("The infection '{}' could not found!".format(infection))
		else:
			break

	print("")

	infected = khan.infect_user(user, infection)

	print("Infected {} user(s)!".format(len(infected)))
	print("User(s) infected: {{{}}}".format(', '.join(map(str, infected))))

def limited_infection(khan):
	while True:
		target = input("Please enter the maximum number of users to infect: ")

		if target is None or target == "":
			return

		try:
			target = int(target)
			break
		except:
			pass

	print("")

	while True:
		infection = input("Please enter the name of the infection to infect with or press [Enter] to simulate infection: ")

		if infection is None or infection == "":
			infection = None
			break

		if (infection not in khan.infections):
			print("The infection '{}' could not found!".format(infection))
		else:
			break

	print("\n")

	possibilities = []
	for root_user in khan.root_users.values():
		count = __count_users__([root_user])
		if count < target:
			possibilities.append((count, root_user))

	to_infect = __limited_target__(possibilities, target)

	infected = set()
	for user in to_infect[1]:
		infected.update(khan.infect_user(user.name, infection))

	print("Infected {} user(s)!".format(to_infect[0]))
	print("User(s) infected: {{{}}}".format(', '.join(map(str, infected))))


def limited_infection_perfect(khan):
	while True:
		target = input("Please enter the exact number of users to infect: ")

		if target is None or target == "":
			return

		try:
			target = int(target)
			break
		except:
			pass

	print("")

	while True:
		infection = input("Please enter the name of the infection to infect with or press [Enter] to simulate infection: ")

		if infection is None or infection == "":
			infection = None
			break

		if (infection not in khan.infections):
			print("The infection '{}' could not found!".format(infection))
		else:
			break

	print("\n")

	possibilities = []
	for root_user in khan.root_users.values():
		count = __count_users__([root_user])

		if count < target:
			possibilities.append((count, root_user))

	to_infect = __limited_target__(possibilities, target)

	if to_infect[0] != target:
		print("Unable to infect exactly {} user(s)!".format(target))
	else:
		infected = set()
		for user in to_infect[1]:
			infected.update(khan.infect_user(user.name, infection))


		print("Infected exactly {} user(s)!".format(to_infect[0]))
		print("User(s) infected: {{{}}}".format(', '.join(map(str, infected))))


def __count_users__(users):
	count = 0
	for user in users:
		count += __count_users__(user.children) + 1

	return count

def __limited_target__(possibilities, target):
	is_done = Value('B', 0)

	poss_arr = [possibilities[i:] for i in range(len(possibilities))]

	with Pool(initializer=__limited_init__, initargs=(is_done,)) as pool:
		out = [pool.apply_async(__limited_target_threaded__, [poss, target]) for poss in poss_arr]
		results = [o.get() for o in out]

	# with Pool() as pool:
	# 	results = pool.starmap(__limited_target_threaded__, zip(, repeat(target), repeat(is_done)))

	best = (0, [])
	for result in results:
		if result[0] > best[0]:
			best = result
			if best[0] == target:
				break

	return best

def __limited_target_threaded__(possibilities, target):
	if target < 0:
		return (-1, None)
	elif target == 0:
		return (0, [])

	best = (0, [])
	for i in range(len(possibilities)):
		if glob.is_done.value != 0:
			break

		cur_pos = possibilities[i]

		# Skip this iteration if the root already has too many
		if cur_pos[0] > target:
			continue

		# Recursively check for best solution for target
		cur_val = __limited_target_threaded__(possibilities[i+1:], target - cur_pos[0])

		if cur_pos[0] + cur_val[0] > best[0]:
			# Add current node to the latest permutation
			cur_val = (cur_pos[0] + cur_val[0], cur_val[1])
			cur_val[1].append(cur_pos[1])

			# Set current permutation as the best
			best = cur_val

		if best[0] == target:
			glob.is_done.value = 1
			break

	return best

def __limited_init__(is_done):
	glob.is_done = is_done

def __limited_target_old__(possibilities, target):
	if target < 0:
		return (-1, None)
	elif target == 0:
		return (0, [])

	best = (0, [])
	for i in range(len(possibilities)):
		cur_pos = possibilities[i]

		# Skip this iteration if the root already has too many
		if cur_pos[0] > target:
			continue

		# Recursively check for best solution for target
		cur_val = __limited_target__(possibilities[i+1:], target - cur_pos[0])

		if cur_pos[0] + cur_val[0] > best[0]:
			# Add current node to the latest permutation
			cur_val = (cur_pos[0] + cur_val[0], cur_val[1])
			cur_val[1].append(cur_pos[1])

			# Set current permutation as the best
			best = cur_val

	return best

def reset(khan):
	for user in khan.users.values():
		user.infections.clear()

	for inf in khan.infections.values():
		inf.malevolent = False

	print("Successfully disinfected all users and reset all infection malevolent flags!")

def clear(khan):
	khan.clear()
	print("Successfully cleared all users and infections!")

if __name__ == "__main__":
	freeze_support()
	khan = Khan()

	# Prompt user with the main part of the program
	main_prompt(khan)
