#!/usr/bin/python3
from functions import console, linux, setup
from profiles import load as load_profiles

def main():

	# Ensure this is running on Arch Linux
	with open("/etc/os-release", "r") as release:

		if not "Arch Linux" in release.read():

			# Exit if system is not Arch Linux
			console.log("This is not Arch Linux.", "err")
			exit(1)
	
	username, p_dict = linux.whoami(), load_profiles()

	console.log(f"Welcome {username}, select a profile:")
	
	for i, P in enumerate(p_dict):
		console.log(f"{i+1}) {p_dict[P].name}", "nof")

	try:

		# intGet makes sure this is an integer input
		input = console.intGet(1, len(p_dict), "Answer: ")
		
		# Configure selected profile
		if not setup.resolve(p_dict, input-1, username):
			console.log("A problem occurred, check log files!", "err")
			exit(1)

		# Conclusion
		console.log("All operations completed, please reboot!", "suc")

	except KeyboardInterrupt:

		# Just quit if ctrl+c
		console.log("Detected keyboard interrupt, terminating.", "wrn")
		exit(1)

if __name__ == "__main__":
	main()