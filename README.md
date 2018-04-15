![Skeleton Key Logo][LOGO]

USB Skeleton Key
=================
Skeleton Key is a physical pen-testing framework that makes use of a Raspberry Pi micro-controller to provide a portable and streamline Enumeration/Exploitation capabilities

Features
---------
  * Enumeration
  * Responder
  * Keyboard Emulation
  * Ducky Script Interpretation

Setup
-------------
When making use of the Pi we expect a specifically crafted Raspberry Pi Zero in order to provide status lights (Although this is optional).
The HAT we make use of by default is the [Blinkt kit][BLINKT] and we also make use of a [USB Stem kit][USBSTEM] to provide a USB stick look and feel.

Install USB Skeleton Key by running:
```commandline
git clone usbskeletonkey
run skeleton-key.py
```

Contribute
-----------
- [Issue Tracker][ISSUES]
- [Source Code][PROJECT]

Support
--------
If you are having any issues, please create an issue with a detailed explanation of the encountered problem.

License
--------
The project is licensed under the

See the [Legal Disclaimer][LEGAL] for information on this projects legal bounds


skeleton-key.py
================
This part of the project acts as the UI and allows the user to configure module setting before deployment on a target system.

Install Project

1. run skeleton-key.py
    2. select module
    3. configure module
4. saved ready for deployment


Interface Features
---------
- View all installed modules
- Configure any installed module
- Set the load order for enabled modules


Interface use
--------------
Modules are selected by a index number in the following form:

    --------------------
    1   Enumerate
    2   Ducky Script
    3   Responder
    4   SomeOtherModule
    --------------------

Once a module is selected, configuration mode for said module is entered.
The following commands can be used to interact with configuration mode:

    command				- Description of command
    --------------------------------------------------------------------------------------------------
    show				        - shows all info on the current module
    show [attribute]		    - shows the info on the specified attribute of the current module e.g. options
    set				            - displays instructions on how to use the set command
    set [attribute]			    - allows the user to enter a value to set the specified attribute for the current module
    set [attribute] [value]	    - sets the value for the specified attribute for the current module
    order                       - displays instructions on how to use the order command
    order [index] [index]       - move module at from current index to target index
    order [index] [direction]   - move module by one position \<up/down\>
    exit 				        - exits configuration mode


Examples
----------
show Enumerate			- Shows all information on the module Enumerate

show Enumerate options		- Shows all information on the options of Enumerate

set port_targets  		- Enters input mode to enter a value for port_targets of current module

set port_targets 55-1000	- Sets port_targets to the range 55-1000 on the current module

Interface Bugs
-----
Interface is not perfect therefore, will at times, throw errors.
Many of these errors have been fixed or altered but some may still creep in.
For this, we ask that you report any bugs or even write a patch to fix them.

If Skeleton Key does not act in the way you expect - please update to the [latest version][PROJECT].
If the problem persists do some research to determine if the error has already been discovered and addressed.
Try searching for the problem or error message on Google, if nothing comes up please feel free to create an [Issue][ISSUES]


network.py
===========
The network emulation framework component of Skeleton Key allows the device to emulate a connected network cable and force a victim to send network data to Skeleton Key for capturing. As this component is completely headless it doesn't require any user interaction to function.


Network Features
---------
- Turn the raspberry pi into an "ethernet" adapter using USB OTG functionality (emulation of a network device).
	- This interface is recognised as usb0 on the Skeleton Key.
	- Specific adapters can be emulated by setting the "vendor_id" and "product_id".
	- Host will attempt to use Skeleton Key for all network communication. Note this will cause the victim to lose internet connectivity.

Network Bugs
-----
As the network component mostly uses Bash editing of configuration files on a known fixed install issues are rare, however, do note:

- Due to how target systems may be configured for driver installation Skeleton Key may fail to be recognised. As a result "vendor_id" and "product_id" may need to be edited to recognised values for network.py to function. 



keyboard.py
===========
This framework component of Skeleton Key requries ducky scripts to operate. The functionality of Keyboard can be accessed through the Ducky Script Module by Users, or directly by Module Developers.

The way keyboard works is similar for both developers and users. Users will select a ducky script file through the interface which will then be used with keyboard.py, while developers can send a ducky script string containing their desired action to keyboard.

Keyboard Features
---------
- Turns the rapsberry pi into a USB Rubber Ducky (emulation of a Keyboard device)
- Can be used to enter text or perform complex key insertions
- Accepts ducky script and some things not supported in ducky script:
	- WIN SHIFT S  performs the same as WIN-SHIFT S
	- CTRL ALT DEL performs the same as CTRL-ALT-DELETE

Keyboard Bugs
-----
The ducky interpreter currently doesn't support F Numbers e.g. F12



Responder.py
===========
Responder.py is an offensive module contained within Skeleton Key which acts as a front end for Spider Lab's Responder tool for capturing user credentials.

Responder Features
---------
- Attempts to capture the password hash of the system that Skeleton Key is connected to using Spiderlabs' Responder.
	- Spiderlabs' Responder exploits a loophole in DNS name resolution that allows any host on a network to respond to local DNS requests if the user's required resource is unknown.
	- It captures password hashes by fooling a target system into believing that Skeleton Key is the SMB server that the victim is looking for which it then attempts to authenticate with.


Responder Usage
---------
- This module requires the use of the network framework component. Should network.py fail to initialise then Responder.py will not continue to run and will be exited.
- The responder module is required to have a "time to live" set i.e. how long the tool will run for. This value defaults to 60 seconds and can be set via skeleton's CLI to any value equal to or greater than 60 seconds (Recommended to be set in excess of 600 seconds for successful operation).

Responder Bugs/Issues
---------
- Responder relies on a specific set of conditions to be met for success and as such can be unreliable (~20% success rate).
- Responder can only be used to capture password hashes for SMB shares (Windows systems will attempt with logged in user account).
	
	
Authors
-------
[Andrew Calder](https://github.com/AR-Calder) - [Email](1503321@uad.ac.uk)

[Corey Forbes](https://github.com/yeroc-sebrof) - [Email](1500812@uad.ac.uk)

[Ellis Richmond](https://github.com/EGRichmond) - [Email](1501363@uad.ac.uk)

[Jonathan Ross](https://github.com/Joh98) - [Email](1500598@uad.ac.uk)

[Michaela Stewart](https://github.com/muicheka) - [Email](1501125@uad.ac.uk)

[LOGO]: key.png
[BLINKT]: https://shop.pimoroni.com/products/blinkt "Pimoroni Link to Blinkt kit"
[USBSTEM]: https://shop.pimoroni.com/products/zero-stem-usb-otg-connector "Pimoroni Link to USB Stem"
[PROJECT]: https://github.com/AR-Calder/usbskeletonkey "Skeleton Key Project"
[ISSUES]: https://github.com/AR-Calder/usbskeletonkey/issues "Skeleton Key Issues Page"
[LEGAL]: LEGAL%20DISCLAIMER.pdf
