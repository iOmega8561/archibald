# archibald
## Disclaimer
This is a personal project, it's not meant to be a production-ready application so use it carefully.

## What's this?
Archibald is a glorified script, meant to be used on a fresh system, that can help the user automate post-install procedures, such as installing a desktop environment or writing config files somewhere in the system.

## How to use
Archibald can be run either in arch-chroot or a booted system. It is meant to be run like a shell script, so it cannot be installed as a python module.
### Requirements
Python 3 must be installed and path-accessible.
A sudo user must be configured and used to run Archibald.
For NVIDIA users, please install the right kernel headers before running Archiabald, this is required to build nvidia drivers with dkms.
### When ready
Then you can simply ```git clone``` this repo and
```
cd archibald
chmod +x archibald.py
./archibald.py
```
Profiles are found under Archibald/profiles/. More on it down below.

## Configuration
Profiles can be created and dropped under archibald/profiles/, they must respect a specific set of attributes that will be parsed by Archibald at runtime. Here is an example.py profile:
```
deps     = ["a_profile", "another"]              # Profile dependencies            | list, can omit

name     = "Example"                             # Profile name                    | str, MANDATORY
        
drivers  = {                                     # Graphics drivers                | dict, can omit

    "A Gpu Manifacturer": ["driverpackage1", "mesasomething"]

}
    
pkgs     = packages.ex + packages.ex2 + .. OR pkgs = ["pkg1", "pkg2" ...]          | list, can omit
    
units    = ["test", "example"]                   # List of systemd units to enable | list, can omit
    
groups   = ["wheel", "example"]                  # List of user groups             | list, can omit
    
shell    = "/bin/somecustomshell"                # Custom shell binary             | str, can omit
    
aur      = ["aurpkg", "another"]                 # Install or not paru             | list, can omit

flatpaks = ["org.some.flatpak", "another"]       # Flatpak list                    | list, can omit

bash     = ["a command", "another command"]      # Bash arbitrary commands         | list, can omit

files    = {                                     # Profile only config files       | dict, can omit
        
    "filename": [
        "some/system/path/like/{home}",
        "somerandomtexttoputinyourfile"
    ]
}
```
