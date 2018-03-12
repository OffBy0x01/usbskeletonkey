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


def arpScan(target, interface="usb0", source_ip="self", target_is_file=False,
            original_out=False, randomise_targets=False):
    """
    Makes use of the arp-scan command.
    By default makes use of the verbose and retry flags.

    Target can be a list of IP's or a single IP.
        This allows for passing in the lists (such as that which the configs stores)
    :param target: IPv4 address(s) e.g "192.168.0.1", "192.168.0.0/24", ["192.168.0.1", "192.168.0.2"]
    :param interface: String value for interface, defaults to usb0 but can make use of any interface that is available
    :param source_ip: String value that defaults to self but can be changed send packets with source being another address
    :param target_is_file: Binary value for when the user wishes to use a file containing addresses. Defaults False
    :param original_out: Binary value for whether the command gives out the command output without parsing. Defaults False
    :param randomise_targets: Binary Value for targets where they should not be scanned in the order given. Defaults False

    :return: output of the command to be parsed
    """
    command = ["arp-scan", "-v", "-I", interface, "-r", "3"]

    if randomise_targets:
        command += ['-R']

    if source_ip is not "self" and ipIsValid(source_ip):
        command += ["-s", source_ip]

    if target_is_file is True:
        if target is list:
            return "Error: A list of files cannot be scanned"

        command += ["-f", target]  # The target in this case should be the path to a target list file

    else:  # if target is not a file
        if type(target) is list:
            for current in target:
                if not ipIsValid(current, iprange=True):
                    return "Error: Target " + str(current) + " in list is not a valid IP"

            command += target

        elif type(target) is str:  # if target is just an IP
            if not ipIsValid(target, iprange=True):
                return "Error: Target is not a valid IP or Range"

            command += [target]

        else:
            return "Error: Target is not a string or list"

    output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")

    if original_out is True:
        return output

    output = output.splitlines()

    # Removing generalised information out
    del output[0:2]
    del output[-3:]

    outlist = [[]]  # was unable to change each line from a string to a list so moving each line as it becomes a list

    for line in output:
        # Splits where literal tabs exist (between the IP, MAC and Adapter Name)
        outlist += [line.split("\t")]

    return outlist  # Sorting via IP would be nice


def ipIsValid(IP, iprange=False):
    """
    Checks that the string passed in entirely consists of an IPv4 address or a range of IP's

    Args:
    :param IP:      string that is being checked as a valid IP
    :param iprange: Will also allow for IP ranges to be valid

    :return: boolean indicating if the IP is valid, True for valid IP
    """
    # Side note, might need IPv6 support. TODO Check this isn't an issue
    ip_range = "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # This checks a number is within 0-255
    an_ipv4 = ip_range + "\." + ip_range + "\." + ip_range + "\." + ip_range  # This regex will check its a IP

    an_ipv4_range = an_ipv4 + "\/[0-2][0-9]|" + an_ipv4 + "\/3[0-2]"  # This checks IP ranges such as 192.168.0.0/24
    # The checks with this one are more lax. Still error prone

    if iprange:
        check = re.search("\A" + an_ipv4 + "\Z|\A" + an_ipv4_range + "\Z", IP)
    else:
        check = re.search("\A" + an_ipv4 + "\Z", IP)

    if check is None:
        return False
    else:
        return True
