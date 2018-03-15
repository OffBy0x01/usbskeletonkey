 USB Skeleton Key
=================
Skeleton Key is a physical pen-testing framework that makes use of a Raspberry Pi micro-controller to provide a portable and streamline Enumeration/Exploitation capabilities

Features
---------
  * Enumeration
  * NMAP

Setup
-------------
When making use of the Pi we expect a specifically crafted Raspberry Pi Zero in order to provide status lights (Although this is optional).
The HAT we make use of by default is the [Blinkt kit](https://shop.pimoroni.com/products/blinkt) and we also make use of a [USB Stem kit](https://shop.pimoroni.com/products/zero-stem-usb-otg-connector) to provide a USB stick look and feel.

Install USB Skeleton Key by running:

	git clone usbskeletonkey
	run skeleton-key.py

Contribute
-----------

- [Issue Traker](github.com/usbskeletonkey/usbskeletonkey/issues)
- [Source Code](github.com/usbskeletonkey/usbskeletonkey)

Support
--------

If you are having any issues, please let us know.
We have a mailing list located at: <usbskeletonkey@temporarydomain.scot>

License
--------

The project is licensed under the 


skeleton-key.py
================

This part of the project acts as the UI and allows the user to configure 
module setting before deployment on a target system.

	#install project
	run skeleton-key.py
		select module
		configure module
	saved ready for deployment

Features
---------

- View all available modules installed
- Configure any module
- Use keyword commands to perform actions

Interface use
--------------
 
Modules are selected by a index number i.e. 1 or 4 in the following form:

--------------------
1	NMAP
2	Enumeration

--------------------

Once a module is selected - enter configuration mode of the selected module.
The following commands can be used to interact with configuration mode:

command				- Description of command
--------------------------------------------------------------------------------------------------
show				- shows all info on the current module
show [attribute]		- shows the info on the specified attribute of the current module
set				- displays instructions on how to use the set command
set [attribute]			- allows the user to enter a value to set the specified attribute 
				  for the current module
set [attribute] [value]		- sets the value for the specified attribute for the current module
exit 				- exits configuration mode

Examples
----------

show nmap			- Shows all information on the module NMAP
show nmap options		- Shows all information on the options of NMAP
set rhosts			- Enters input mode to enter a value for rhosts of current module
set rhosts 192.168.0.1		- Sets rhosts to 192.168.0.1 on the current module

Bugs
-----

Interface is not perfect therefore, will at times, throw errors. Many of these errors have been fixed or altered
but some may still creep in. For this, we ask that you report any bugs or even write a patch to fix them.

If Skeleton Key does not act in the way you expect - please update to the [latest version](https://github.com/usbskeletonkey). If the problem persists do some research to determine if the error has already 
been discovered and addressed. Try seraching for the problem or error message on Google, if nothing comes up please
feel free to create an [Issue](https://github.com/usbskeletonkey) and/or may a bug report to
<usbskeletonkey@temporarydomain.scot>

If you are able to write a patch improving Nmap or fixing a bug, that is even better!
Instructions for submitting patches or git pull requests are available [here](https://github.com/nmap/usbskeletonkey)


network.py
================
This framework component of Skeleton Key requries no user input and runs in the background. The script is never directly called by the user and is instead used to allow the following modules to operate:

	LIST OF MODULES (COME BACK TO)


Features
---------

- Turns the rapsberry pi into an "ethernet" adapter using USB OTG functionality (emulation of a network device)
- Uses code from the "poisiontap" project to allow for the pi to act as a DHCP server and capture network traffic:
	- Adds routes for all ipv4 addresses
	- Starts DHCP server and enables ipv4 forwarding
	- Binds port 80 to port 1337
	- Starts dnsspoof on port 53

Bugs
-----
As user interaction is pretty much non-existant with this componenent there is very little to worry about regarding bugs (that we have been able to find). Please note the following however:

- Due to how Linux and Mac systems interact with network devices the capturing of network traffic is only possible on Windows systems currently. (NEED TO RE-TEST THIS)

- Windows systems prioritise "new" ethernet network devices over existing ones, so unfortunately it is only possible to use network emulation to capture network traffic once during an attack. This is due to fact that the target system won't automatically connect to the "ethernet" adapter as the device will be known to the system after its first use.   


Authors
-------
[Andrew Calder](https://github.com/AR-Calder) <1503321@uad.ac.uk>

[Corey Forbes](https://github.com/yeroc-sebrof) <1500812@uad.ac.uk>

[Ellis Richmond](https://github.com/EGRichmond) <1501363@uad.ac.uk>

[Jonathan Ross](https://github.com/Joh98) <1500598@uad.ac.uk>

[Michaela Stewart](https://github.com/muicheka) <1501125@uad.ac.uk>
