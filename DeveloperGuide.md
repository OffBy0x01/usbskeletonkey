![Skeleton Key Logo][LOGO]

# Skeleton Key Developers Guide
1. Framework info
    1. Building Blocks
        * Debug
        * FwComponentGadget
        * Module Manager
        * Module Desc
    2. Framework items
        * Keyboard
        * Networking
        * Storage
2. Module info
    * Enumeration
    * KeyInject
    * Responder
    * Storage
3. Helpers
    * Blinkt
    * Format
    * IpValidator


## Framework info
The Skeleton Key framework is believed to have access to all of the components it can/should need the use of;
however there is more that could be made available as and when it may seem relevant.

As we are aware this is the case we have made the effort to keep the Framework modular to allow for future expansion.
Any future expansion would require an understanding of the Building blocks in play for all Framework components in order to correctly expand.
If you are just requiring an understanding of the current framework to develop a module then this section of the guide can be avoided.


### Building Blocks
The following should be used when considering creating framework components of any type.

#### Debug
This Class mostly makes use of the interface to display the debug messages when Skeleton Key is in debug mode.
It has other features that can be used to check that all methods have completed and a print out of the rough structure of a list.
This class provides the bare-bones of whats needed to ensure correct module/framework execution and Debug faulty execution.
Skeleton key will correctly handle any crashes so to test modules they can just be executed and each step of the way assigned a debug output.

#### FwComponentGadget
text

#### Module Manager
text

#### Module Descriptor
text


### Framework Items
text

#### Keyboard
text

#### Networking
text

#### Storage
text


## Module info
For anyone interested in developing a module, although you could have skeleton key do what you want without making use of any other section of what's available just so you can have your module execute in the load order.
In that case however, you may wish to make a framework component or helper that your module makes use of just so other objects in future could benefit from what you have available.

Modules that can be made is entirely up to you.
As this is the highest level you can work at this provides you the wealth of framework components and helpers that we have created to fit our need that may hopefully fit yours too.
Below is examples of what modules exist, what components/helpers they make use of and some extended information that may not be in the docstring.

#### Enumeration
text

#### KeyInject
text

#### Responder
text

#### Storage Module
text


## Helpers
Helpers are simple classes that do not interact with the framework directly which can be used to help a module perform better.
They should be relatively simple to work with and provide snippets of code that may be useful for any module or framework component.

#### Blinkt
This helper adds support for the light strip for the Pi GPIO HAT, Blinkt.
Providing users methods to interact with the Blinkt that has been correctly exception handled to avoid any dependency issues.
This helper is not able to confirm what HAT is currently on the Pi so it relies on only being called where relevant.
An example of the previous can be seen in the Enumerate module where it will not be called when the flag is disabled in the configs.

The functions that Blinkt provides are:
- unset_pixel - 
This sets the pixel to 0, 0, 0 for RGB
- set_pixel - 
This enables the pixel at the integer value passed in
- clear - 
This method clears all the LED's
- new_brightness - 
Sets the brightness to a float value within the range 0<=n<=1
- new_colors/new_colours - 
Changes the colour that is used with the set_pixel method
- progressive_pixels - 
This is a method that takes the current task and the total number of tasks and lights up the appropriate led on the 0-7 scale.


#### Format
This helper provides text colours and _**formatting**_ in the CLI.
It has been incorporated into both Debug messages and the Skeleton-Key interface.

A list of the available formatting options are:
- color
    - primary
    - secondary
    - success
    - warning
    - danger
    - info
- decoration
    - bold
    - underline
- format_clear

Formatting will remain until the format_clear is used but when Debug makes use of these options it always will use the clear at the end of each line.

#### IpValidator
This class has two functions that can be utilised to check if an IP address is valid.
You can check for a IPv4 or 6 address;
The IPv4 check can also be used to search for a range e.g. 192.168.0.0/24


######Fin.

[LOGO]: key.png
