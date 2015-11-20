import time
import datetime
import random
from collections import deque
import math


def simulate(khan):
	while True:
		minutes = input("Please enter how many minutes to simulate (1440 minutes in a day): ")

		print("")

		if minutes is None or minutes == "":
			return

		try:
			minutes = int(minutes)
			if minutes < 1:
				raise ValueError()
			break
		except:
			print("Please enter a valid value!\n")


	while True:
		pause = input("Please enter how long a minute should be simulated as (in milliseconds): ")

		print("")

		if pause is None or pause == "":
			return

		try:
			pause = float(pause) / 1000
			if pause < 0:
				raise ValueError()
			break
		except:
			print("Please enter a valid value!\n")

	while True:
		bugginess = input("Please enter an average infection bugginess rate (float between 0 and 100): ")

		print("")

		if bugginess is None or bugginess == "":
			return

		try:
			bugginess = float(bugginess)
			if bugginess < 0 or bugginess > 100:
				raise ValueError()
			break
		except:
			print("Please enter a valid value!\n")

	print("Beginning simulation...")

	elapsed = 0
	dt = datetime.datetime(datetime.MINYEAR, 1, 1)

	online = []
	offline = list(khan.users.values())
	been_online = set()

	issue_count = 0

	while elapsed < minutes:
		print("Day {}, {}".format((elapsed // 1440) + 1, dt.strftime("%I:%M %p")))

		# Simulate users getting online
		i = 0
		while i < len(offline):
			if random.randint(0, minutes) == 1:
				user = offline.pop(i)
				online.append(user)

				if user in been_online:
					print("{} has logged in again!".format(user.name))
				else:
					infect_user(khan, user)
					print("{} has logged in and has been infected with {{{}}}.".format(user.name, ', '.join(map(str, user.infections))))
					been_online.add(user)
			else:
				i += 1

		print("")

		# Simulate users getting online
		for user in online:
			for inf in user.infections:
				if math.floor(random.random() * 101 * minutes) < bugginess:
					inf.malevolent = True
					issue_count += 1

					disinfected = disinfect_user(khan, user, inf)
					disinfected.update(rollback_infection(khan, inf))
					print("{} has run into an issue with infection '{}' and {} users have been disinfected as a result.".format(user.name, inf.name, len(disinfected)))

		print("")

		# Simulate users going offline
		i = 0
		while i < len(online):
			if random.randint(0, 60) == 1:
				user = online.pop(i)
				offline.append(user)
				print("{} has logged off".format(user.name))
			else:
				i += 1

		time.sleep(pause)
		elapsed += 1
		dt = dt + datetime.timedelta(minutes=1)
		print("\n\n")

	print("Malevolent infections: {}".format(get_malevolent_infections(khan)))
	print("{} unique users came online during this time period.".format(len(been_online)))
	print("{} issues were encountered by users.".format(issue_count))

def infect_user(khan, user):
	q = deque()
	q.extend(khan.root_infections.values())

	while len(q) > 0:
		cur_inf = q.popleft()
		if cur_inf not in user.infections and not cur_inf.malevolent and random.randint(1, 100) <= cur_inf.contagiousness:
			khan.infect_user(user.name, cur_inf.name)
			q.extend(cur_inf.children)

def disinfect_user(khan, user, infection):
	return khan.disinfect_user(user.name, infection.name)

def rollback_infection(khan, infection):
	severity = infection.get_severity()
	disinfected = set()

	for user in khan.users.values():
		if infection in user.infections and random.randint(1, 100) <= severity:
			disinfected.update(khan.disinfect_user(user.name, infection.name))

	return disinfected

def get_malevolent_infections(khan):
	malevolent = []
	for infection in khan.infections.values():
		if infection.malevolent:
			malevolent.append(infection.name)

	return malevolent
