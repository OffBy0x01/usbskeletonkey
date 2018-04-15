#Responder
===========
Responder.py is one of the modules that has been developed for Skeleton Key.

Responder Features
---------
- Attempts to capture the password hash of the system that Skeleton Key is connected to using Spiderlabs' Responder.
	- Spiderlabs' Responder exploits a loophole in DNS name resolution that allows any host on a network to respond to local DNS requests if the user's required resource is unknown.
	- It captures password hashes by fooling a target system into believing that Skeleton Key is a SMB server.



Responder Usage
---------
- This module requires the use of the network framework component. If any error is thrown by this component upon initialisation then Responder.py will not continue to run and will be exited.
- The responder module is required to have a "time to live" set i.e. how long the tool will run for. This value defaults to 60 seconds and can be set via skeleton's CLI to any value equal to or greater than 60 seconds.

Responder Bugs/Issues
---------
- Responder is extremely unreliable when it comes to the capturing of password hashes, with reports that it is only successful ~10/20% of the time.
- Responder can only be used to capture password hashes on Windows systems.
- Due to some unknown reason Responder won't run correctly unless the USB gadget "g_ether" kernel has been enabled and disabled at least once before running the tool.
	- This has been accounted for in the source code of the module.
- On first time use Responder usually creates "Responder.db" where password hashes are intially stored. Due to some unknown reason this file is never created automatically for Skeleton Key.
	- This has been accounted for in the source code of the module by creating and populating the .db file before first time use.
	
