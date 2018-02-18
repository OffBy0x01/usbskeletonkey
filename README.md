USB Skeleton Key
=================

Skeleton Key is a physical pen-testing tool using a micro-controller

Features
---------

- NMAP
- Enumeration

Installation 
-------------

Install USB Skeleton Key by running:

	git clone usbskeletonkey
	run skeleton-key.py

Contribute
-----------

- Issue Traker: github.com/usbskeletonkey/usbskeletonkey/issues
- Source Code: github.com/usbskeletonkey/usbskeletonkey

Support
--------

If you are having any issues, please let us know.
We have a mailing list located at: usbskeletonkey@

License
--------

The project is licensed under the 

================
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

If Skeleton Key does not act in the way you expect - please update to the latest version available from
https://github.com/usbskeletonkey. If the problem persists do some research to determine if the error has already 
been discovered and addressed. Try seraching for the problem or error message on Google, if nothing comes up please
feel free to create an Issue on our tracker (https://github.com/usbskeletonkey) and/or may a bug report to
<usbskeletonkey@ >

If you are able to write a patch improving Nmap or fixing a bug, that is even better! Instructions for submitting 
patches or git pull requests are available from https://github.com/nmap/usbskeletonkey 

Author
-------

Andrew Calder 		<>
Corey Forbes		<>
Elis Richmond		<>
Jonathan Ross		<>
Michaela Stewart	<1501125@uad.ac.uk>