#!/usr/bin/python3
import utilities.configs as configs
import utilities.methods as methods
import utilities.formats as formats

def main(logname):
	#Prepare greeting text
	prompt = f"{formats.msgStr} Archibald utility for Arch Linux, select a profile:\n"
	
	#Format-add every profile name and target to greetings
	for i, p in enumerate(configs.profiles):
		prompt += formats.selStr.format(i + 1, p.name, p.type)
	prompt += f"{formats.bold}User input:{formats.endc} "

	#Print prompt text and get user imput, must be integer
	index = methods.integerget(prompt, f"{formats.warnStr} Input not a number, retry.") - 1
	while index < 0 or index >= len(configs.profiles):

		#Repeat input until a valid one is given
		print(f"{formats.warnStr} Not in range, try again.")
		index = methods.integerget(prompt, f"{formats.warnStr} Input not a number, retry.") - 1

	#When success, save chosen profile inside selection and prompt user his choice again
	selection = configs.profiles[index]
	print(f"{formats.msgStr} Selected profile is {selection.name} ({selection.type})")
	
	#Try to find user defined driver name inside lspci output
	print(f"{formats.warnStr} Searching for any known graphics device...")
	lspci = methods.subprocess_try("lspci")
	for device in configs.drivers:

		#Repeat match for every user defined driver group
		match = [f"VGA compatible controller: {device}", f"Display controller: {device}"]
		if any(x in lspci.stdout.rstrip("\n") for x in match):

			#If is found, add packages to profile.pkgs
			print(f"{formats.succStr} Found {device} device!")
			selection.pkgs += configs.drivers[device]

	#Packages installation via pacman subprocess
	print(f"{formats.warnStr} Please wait while PacMan installs packages...")
	methods.subprocess_try(["pacman", "-S", "--needed", "--noconfirm"] + selection.pkgs,
		"pacman.log", 
		f"{formats.succStr} Successfully installed all packages!", 
		f"{formats.errStr} PacMan encountered errors, check pacman.log")
	
	#Config files creation
	print(f"{formats.warnStr} Deploying configuration files...")
	for i, f in enumerate(configs.files):
		methods.makefile(f.path, f.name, f.text, f"{formats.errStr} Could not open {f.path}{f.name}.")
	
	#Archibald runs with root privileges, so files in home will have rw protection
	methods.subprocess_try(["chown", "-R", f"{logname}", f"/home/{logname}"])

	#Setting user groups one by one
	print(f"{formats.warnStr} Settings user groups...")
	for i in selection.groups:
		methods.subprocess_try(["usermod", "-aG", f"{logname}"] + i)

	#Enabling systemd units all at one (systemctl supports it)
	print(f"{formats.warnStr} Enabling systemd units...")
	methods.subprocess_try(["systemctl", "enable"] + selection.units,
		"systemctl.log", 
		f"{formats.succStr} Successfully enabled systemd units!", 
		f"{formats.errStr} Systemctl encountered errors, check systemctl.log")

if not methods.subprocess_watch("whoami", "root", "all"):
	#Exit if not executing with sudo
	print(f"{formats.errStr} Archibald needs {formats.uline}high{formats.endc} privileges.")
elif not methods.subprocess_watch(["cat", "/etc/os-release"], "Arch Linux", "any"):
	#Exit if system is not Arch Linux (pacman is used)
	print(f"{formats.errStr} This is not Arch Linux.")
else:
	logname = methods.subprocess_try("logname").stdout.rstrip("\n")
	
	if logname == "root":
		#Exit if logged in as the root use (/home/root does not exist)
		print(f"{formats.errStr} Executing logged as root is not supported.")
		quit()

	#Run main logic
	main(logname)