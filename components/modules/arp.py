'''
`arp-scan -v -I usb0 -R -r 5 <le host>`
<le host> can be an individual host or a range such as 192.168.0.12-192.168.0.21 OR 192.168.0.0/24
`-W` outputs as a PCAP
`-f <file>` will pull hosts to scan from a file if that is easier for us
`-t <ms>` will set timeout (Default 500ms which we may want to put up due to the spotty connection experienced over USB
`-b <multiplier>` will set the timeout multiplier between attempts (We might wanna turn this off?) default is 1.5
`-s <set source ip>` we may want to set the source IP as the machine we are plugged into to avoid suspicion and
                        intercept responses on said machine. Although the device would then attempt to send the packet
                        back to us so maybe not?

'''
import subprocess
import re

def arpScan(target, interface="usb0", sourceIP="self", targetIsAFile=False):
    """
    Makes use of the arp-scan command.
    By default makes use of the verbose, random and retry flag.

    Target can be a list of IP's or a single IP.
        This allows for passing in the lists that configs store
    """
    if targetIsAFile is True:
        if target is list:
            return "Error: A list of files cannot be scanned"

        target = "-f " + target  # The target in this case should be the path to a target list file

    else:  # if target is not a file
        if target is list:
            # TODO find pythonic method for making a list of ips into one long string
            concatTargets = str(None)
            for targets in target:
                if ipIsValid(target[targets]):  # check current IP is legit
                    concatTargets = concatTargets + target[targets]
                else:
                    return "Error: Target " + str(targets) + " in list is not a valid IP"

            target = concatTargets  # replace target for later

        else:  # if target is just an IP
            if not ipIsValid(target):
                return "Error: Target is not a valid IP"

    if targetIsAFile is True:
        target = "-f " + target  # The target in this case should be the path to a target list

    flags = "-v -I " + interface + " -R -r 5"

    if "self" is not sourceIP:
        flags = flags + ""

    return subprocess.run(["arp-scan", flags, target], stdout=subprocess.PIPE).stdout.decode('utf-8')


def ipIsValid(IP):
    """
    Checks that the string passed in entirely consists of an IPv4 address

    Args:
        IP:     string that is being checked as a valid IP

    returns:
                boolean indicating if the IP is valid
                    True for valid IP
    """
    # Side note, might need IPv6 support. TODO Check this isn't an issue
    ipRange = "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # Will accept only 0-255

    check = re.search("\A" + ipRange + "\." + ipRange + "\." + ipRange + "\." + ipRange + "\Z", IP)

    if None == check:
        return False
    else:
        return True
