'''
`traceroute -i usb0`
`-r` bypass normal routing tables for faster paths (Could this skip any IDS?)
`--back` prints the hops back when there's a difference. -r will prob have a different path back
`-n` skip mapping to host names on display (this might be doing extra activity on the network)
'''
import subprocess
import re


def traceRoute(target, interface="usb0", bypass_routing_tables=False, hop_back_checks=True,
               map_host_names=True, original_out=False):
    """
    Makes use of the traceroute command.
    No default flags are in use that the user cannot access via output

    Args:
    :param target: takes in a IPv4 target (Cannot Take a list)
    :param interface: Defaults to usb0 but can make use of any interface that is available
    :param bypass_routing_tables: Allows for traceroute to take the most direct approach bypassing routing tables
    :param hop_back_checks: Confirms that packets taken by the response follow the same path
    :param map_host_names: In the event that mapping host names to IP makes noise this can be disabled
    :param original_out: If the user wants the original command output this should be changed to true

    :return: list of ip lists for each hop. Often single item list but keeps consistent for accessing
    """
    command = ["traceroute", "-i", interface]  # start with command items that are required

    # Add command arguments where appropriate
    if bypass_routing_tables:
        command += ["-r"]

    if hop_back_checks:
        command += ["--back"]

    if not map_host_names:
        command += ["-n"]

    if type(target) is str:
        if ipIsValid(target):
            command += [target]
    else:
        return "Error: Wrong type"  # Trace route is not able to target multiple hosts

    # Running command
    output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")

    if original_out is True:  # If user doesnt want output parsed
        return output

    # Parsing output
    output = output.splitlines()

    del output[0]

    output_out = []

    if map_host_names:
        for line in output:
            results = []  # init var to store current results
            line = line.split()
            del line[0]

            for item in line:
                # If item looks like a domain or the first three octets of an IP address
                if re.search("[a-z0-9]*\.[a-z0-9]*\.[a-z0-9]*", item.lower()):  # Would compiling a re be better here?
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
