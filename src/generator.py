import random

def gen_infections():
	while True:
		num = input("Please enter the number of random infections to generate: ")

		print("")

		if num is None or num == "":
			return

		try:
			num = int(num)
			if num < 1:
				raise ValueError()
			break
		except:
			print("Please enter a valid number!\n")

	while True:
		f = input("Please enter a file to write infections to: ")

		print("")

		if f is None or f == "":
			return

		try:
			f = open(f, 'a')
			break
		except:
			print("Unable to open file!\n")

	ind_max = 0
	counter = 1
	for i in range(num):
		# Write random indent
		rand_ind = random.randint(0, ind_max)
		for j in range(rand_ind):
			f.write("\t")

		# Set new indent maximum
		ind_max = rand_ind + 1

		# Write infection name
		f.write('Infection{}'.format(counter))

		# Update counter
		counter += 1

		# Write infection values
		f.write("({}, {})\n".format(random.randint(1, 100), random.randint(1, 100)))

	f.close()


def gen_users():
	while True:
		num = input("Please enter the number of random users to generate: ")
		print("")

		if num is None or num == "":
			return

		try:
			num = int(num)
			if num < 1:
				raise ValueError()
			break
		except:
			print("Please enter a valid number!\n")

	while True:
		f = input("Please enter a file to write users to: ")

		print("")

		if f is None or f == "":
			return

		try:
			f = open(f, 'a')
			break
		except:
			print("Unable to open file!\n")

	ind_max = 0
	counter = 1
	for i in range(num):
		# Write random indent
		rand_ind = random.randint(0, ind_max)
		for j in range(rand_ind):
			f.write("\t")

		# Set new indent maximum
		ind_max = rand_ind + 1

		# Write infection name
		f.write('User{}\n'.format(counter))

		# Update counter
		counter += 1

	f.close()

if __name__ == "__main__":
	while True:
		num = None
		print("\n")
		print("[1] Generate random infection file.")
		print("[2] Generate random user file.")
		print("[3] Exit.")


		try:
			num = int(input("Please select an action to perform: "))
		except:
			pass

		print("")

		if num == 1:
			gen_infections()
		elif num == 2:
			gen_users()
		elif num == 3:
			break
		else:
			print("Please select a valid action!")
