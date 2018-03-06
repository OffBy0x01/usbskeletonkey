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


def arpScan(target, interface="usb0", sourceIP="self", targetIsAFile=False, originalOut=False):
    """
    Makes use of the arp-scan command.
    By default makes use of the verbose, random and retry flags.

    Target can be a list of IP's or a single IP.
        This allows for passing in the lists (such as that which the configs stores)
    :param target:          IPv4 address(s) e.g "192.168.0.1", "192.168.0.0/24", ["192.168.0.1", "192.168.0.2"]
    :param interface:       Defaults to usb0 but can make use of any interface that is available
    :param sourceIP:        Defaults to self but, for in the niche case its useful, can be changed to another address
    :param targetIsAFile:   Defaults to False but, when the user wishes to use a file containing addresses this flag can
                                be set to true and the target can instead be a path to the file.
    :param originalOut: If the user wants the original command output this should be changed to true

    :return: output of the command to be parsed
    """
    command = ["arp-scan", "-v", "-I", interface, "-R", "-r", "3"]

    if sourceIP is not "self" and ipIsValid(sourceIP):
        command = command + ["-s", sourceIP]

    if targetIsAFile is True:
        if target is list:
            return "Error: A list of files cannot be scanned"

        command = command + ["-f", target]  # The target in this case should be the path to a target list file

    else:  # if target is not a file
        if type(target) is list:
            for current in target:
                if not ipIsValid(current, iprange=True):
                    return "Error: Target " + str(current) + " in list is not a valid IP"

            command = command + target

        elif type(target) is str:  # if target is just an IP
            if not ipIsValid(target, iprange=True):
                return "Error: Target is not a valid IP or Range"

            command = command + [target]

        else:
            return "Error: Target is not a string or list"

    output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")

    if originalOut is True:
        return output

    output = output.splitlines()

    del output[:5]  # Delete first 6 lines
    del output[-1:-2]  # Delete last two lines?1

    for line in output:
        line.strip().split(" ")  # TODO this leaves the device name in multiple items and below is a disgusting fix
        re_concat = ""  # Could fix this by making my own string but working out the length of the IP is the only issue
        for item in line[2:]:
            re_concat += item + " "
        line[2] = re_concat.strip()

    return output[0:2]


def ipIsValid(IP, iprange=False):
    """
    Checks that the string passed in entirely consists of an IPv4 address or a range of IP's

    Args:
    :param IP:      string that is being checked as a valid IP
    :param iprange: Will also allow for IP ranges to be valid

    :return: boolean indicating if the IP is valid, True for valid IP
    """
    # Side note, might need IPv6 support. TODO Check this isn't an issue
    ipRange = "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # This checks a number is within 0-255
    anIPv4 = ipRange + "\." + ipRange + "\." + ipRange + "\." + ipRange  # This regex will check its a IP

    anIPv4Range = anIPv4 + "\/[0-2][0-9]|" + anIPv4 + "\/3[0-2]"  # This checks IP ranges such as 192.168.0.0/24
    # The checks with this one are more lax. Still error prone

    if iprange:
        check = re.search("\A" + anIPv4 + "\Z|\A" + anIPv4Range + "\Z", IP)
    else:
        check = re.search("\A" + anIPv4 + "\Z", IP)

    if check is None:
        return False
    else:
        return True
