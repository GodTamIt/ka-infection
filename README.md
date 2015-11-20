# Khan Academy Infection

The goal of this project is to create a program that emulates an incremental and rolling release model for experimental software.  The details and requirements of the project are found [here](https://docs.google.com/document/d/1NiKv-MjULOFyyc8f5w8R_EqvuPJ10wJVJgZhtTK9VKc/edit#).

## Features
- **Lists**: infections and users are loaded into the program via text files.
- **Total Infection**: heuristic infects a user and all of its affiliates (both ancestors and offspring).
- **Limited Infection**: heuristic infects the maximum number of users under a given limit.
- **Perfect Limited Infection**: heuristic infects an exact number of users if it is possible.
- **Simulation**: simulator emulates a real-time situation where users are logging in and out of Khan Academy.
- **Hierarchical View**: program keeps track of the hierarchy of infections and users.
- Written and tested in Python 3.5

## Using the Program
To run the main program, navigate to the `src` folder of the project and open a terminal window. Run with the following command (Python 3 is required):
```
python main.py
```

You will then be prompted by the following options, which directly correspond to the features. Select a valid number to continue an action.
```
[1] Load infections from file.
[2] Load users from file.
[3] Infect a user with a disease (total_infection).
[4] Infect at most a certain amount of users if possible (limited_infection).
[5] Infect exactly a certain amount of users if possible (limited_infection_perfect).
[6] Simulate real-time, user-infection interaction.
[7] Print the infection hierarchy.
[8] Print the user hierarchy and each user's associated infections.
[9] Reset all users and infections to defaults.
[10] Clear all users and infections.
[11] Exit.

Please select an action to perform: 
```

## Simulator
The program can simulate a minute-by-minute timespan, where users are actively interacting with Khan.  When a user is online, they have a chance of experiencing instability (called malevolent infections in the program), and the simulator handles these instabilities based on the properties of the infection causing the instability (see [Infections](#Infections)).  The program will roll back infections on the fly if issues are reported or detected, so users will be (mostly) shielded from these bugs.

## Lists
### Infections
The format for infections is relatively simple.  There is a new infection entry on each line and the indentation of the line determines the hierarchical placement of the entry.  The format is as follows:
```
<Name>(<Severity>, <Contagiousness>)
```
The *severity* of an infection is an integer value in the range [0, 100] that determines how critical an infection is to the user experience.  During the simulation, if a user runs into an issue with an infection, the *severity* determines how quickly that infection is rolled back back from other users.

The *contagiousness* of an infection is an integer value in the range [0, 100] that determines how many users an infection will reach.  During the simulation, when a user logs in, *contagiousness* determines how likely that user will get the infection.

#### Sample
```
Infection1(55, 15)
	Infection2(24, 54)
	Infection3(23, 46)
	Infection4(93, 17)
		Infection5(8, 52)
	Infection6(2, 85)
Infection7(78, 77)
	Infection8(66, 55)
	Infection9(61, 73)
		Infection10(8, 36)
		Infection11(60, 99)
Infection12(6, 97)
Infection13(79, 30)
Infection14(82, 95)
	Infection15(30, 5)
```

### Users
The format for users is the same as infections, except that there are no parameters next to each entry.  It is just a hierarchical list by tabs.

#### Sample
```
User1
	User2
		User3
User4
User5
	User6
	User7
		User8
			User9
				User10
		User11
	User12
User13
User14
User15
```

### Generating Lists
There is also a separate script that auto-generates random hierarchical lists.  To run the generator program, navigate to the `src` folder of the project and open a terminal window. Run with the following command:
```
python generator.py
```

You will be prompted with a menu similar to the main program:
```
[1] Generate random infection file.
[2] Generate random user file.
[3] Exit.
```
