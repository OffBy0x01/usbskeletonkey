'''
`traceroute -i usb0`
`-r` bypass normal routing tables for faster paths (Could this skip any IDS?)
`--back` prints the hops back when there's a difference. -r will prob have a different path back
`-n` skip mapping to host names on display (this might be doing extra activity on the network)
'''
import subprocess
import re


def traceRoute(target, interface="usb0", bypassRoutingTables=False, hopBackChecks=True, mapHostNames=True, originalOut=False):
    """
    Makes use of the traceroute command.
    No default flags are in use that the user cannot access via output

    Args:
    :param target: takes in a IPv4 target
    :param interface: Defaults to usb0 but can make use of any interface that is available
    :param bypassRoutingTables: Allows for traceroute to take the most direct approach bypassing routing tables
    :param hopBackChecks: Confirms that packets taken by the response follow the same path
    :param mapHostNames: In the event that mapping host names to IP makes noise this can be disabled
    :param originalOut: If the user wants the original command output this should be changed to true

    :return: list of ip lists for each hop. Often single item list but keeps consistent for accessing
    """
    command = ["traceroute", "-i", interface]  # start with command items that are required

    # Add command arguments where appropriate
    if bypassRoutingTables:
        command = command + ["-r"]

    if hopBackChecks:
        command = command + ["--back"]

    if not mapHostNames:
        command = command + ["-n"]

    if type(target) is str:
        if ipIsValid(target):
            command = command + [target]
    else:
        return "Error: Wrong type"  # Trace route is not able to target multiple hosts

    output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")

    if originalOut is True:
        return output

    output = output.splitlines()

    del output[0]

    output_out = []

    if mapHostNames:
        for line in output:
            results = []  # init var to store current results
            line = line.split()
            del line[0]

            for item in line:
                # If item looks like a domain or the first three octets of an IP address
                if re.search("[a-z0-9]*\.[a-z0-9]*\.[a-z0-9]*", item.lower()):
                    results += [item.strip("\(\)")]  # Remove any brackets and add to results for this line

            if ipIsValid(results[0]):  # If the "Host name" is an IP
                results = results[::2]  # Grab every other variable

            output_out += [results]  # Add results from this line
    else:
        for line in output:
            results = []  # init var to store current results
            line = line.split()
            del line[0]

            for item in line:
                if ipIsValid(item):
                    results += [item]
            output_out += [results]

    return output_out


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
