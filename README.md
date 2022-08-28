# Archibald
## Disclaimer
This is a personal project, started for fun and personal purposes only. You DO take responsability if this breaks your installation. 

## What's this?
Archibald is a configurable python utility that allows to recreate Arch Linux setups real fast. Archibald can:
- Let the user select a profile;
- Detect graphics cards;
- Install packages via PacMan;
- Enable systemd units;
- Add user to certain groups;
- Create configuration files;
- Change the user shell;
- Configure zram;
- Install aur helper.

It is best to run Archibald on a fresh Arch Linux manual installation, but minimal archinstall setups are ok too.

## How to use
Archibald includes a default configuration, so you can simply ```git clone``` this repo and run
```
cd Archibald
chmod +x archibald.py
sudo ./archibald.py
```
Configuration is found under Archibald/config/. More on it down below.

## Configuration
Once you get to edit Archibald's configuration, you'll see that it's pretty self explanatory, it comprehends:
- Dictionaries file, defines default package groups and driver sets. It also includes contents of default config files that can be deployed on the user's system (for example a standard logind.conf). It is best to not directly edit this file, since it's content is needed for Archibald and it's basic configuration to work.
- Defaults file, which contains profile objects, that will be parsed by Archibald to determine what to do. Here is an example profile:
```
# User defined profiles
# Read carefully any bad config could be catastrofic
# The order of profile childs is not relevant

ExampleProfile = classes.profile(
    name    = "Example",                            # Profile name                    | str, MANDATORY
    type    = "Example",                            # Target system to be prompt      | str, MANDATORY
    drivers = True,                                 # Install graphics drivers        | bool, can omit, default False
    pkgs    = packages.ex + packages.ex2 + .. OR pkgs = ["pkg1", "pkg2" ...]          | list, can omit, default []
    units   = ["test", "example"],                  # List of systemd units to enable | list, can omit, default None
    grops   = ["wheel", "example"],                 # List of user groups             | list, can omit, default None
    shell   = "/bin/exampleshell",                  # Custom shell binary             | str, can omit, default None
    files   = [                                     # Profile only config files       | list, can omit, default None
        classes.file(                                                       BELOW ONLY IF FILES ARE PRESENT
            name = "ExampleConfig",              # File name                       | str, Mandatory
            path = "example/path",               # File path                       | str, Mandatory
            text = "sometextto\nbe\nwritten"),   # Text                            | str, Mandatory
        classes.file( .... )])
```
As you can see profiles can also have as a child a list of file objects. This serves the purpose of letting Archibald create configuration files system wide for you. Since sudo is required, Archibald will run a chown on current user's homedir, to set newly created files and directories' ownership to you instead of root user.
