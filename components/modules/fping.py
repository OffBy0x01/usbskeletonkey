'''
`fping -a --random [Target]`
`-a: only shows Alive targets`
`-c / --count=N: send N pings to a target`
`-g: allows for targets, plural`
`-m: If scanning with a host name scan all associated IP's`
`-n / --name: performs a reverse DNS loookup`
`--random: makes the ips scan in no particular order (lowers suspicion)`
`-R: makes the packets sent contain random packet data`
`-s / --src=addr: Set source address`
'''
import subprocess

import re


def fping(target, ping_count=0, get_ips_from_dns=False, get_dns_name=False, contain_random_data=True,
          randomise_targets=False, source_address="self"):
    command = ["fping", "-a"]

    # Adding Flags
    if ping_count > 0:
        command += ["--count="+str(ping_count)]

    if get_dns_name:
        command += ["-n"]

    if randomise_targets:
        command += ["--random"]

    if contain_random_data:
        command += ["-R"]

    if source_address is not "self":
        command += ["--src="+source_address]

    # Adding Targets
    if ipIsValid(target):
        command += [target]

    elif ipIsValid(target, iprange=True):
        command += ["-g", target]

    elif target is list:
        for item in target:
            # if re.search("\A[a-z0-9]*\.[a-z0-9]*\.[a-z0-9]*\Z", target.lower()) and get_ips_from_dns:
            if get_ips_from_dns:
                if not re.search("\A[a-z0-9]*\.[a-z0-9]*\.[a-z0-9]*", item.lower()):
                    return "Error: Target in list is not a valid IP or hostname (Does not accept ranges here)"
            else:
                if not ipIsValid(item):
                    return "Error: Target in list is not a valid IP (Does not accept ranges here)"
        command += target

    elif re.search("\A[a-z0-9]*\.[a-z0-9]*\.[a-z0-9]*\Z", target.lower()) and get_ips_from_dns:
        command += ["-m"]
        command += [target]

    else:
        return "Error: Target is not a valid IP, Range or list"

    return subprocess.run(command, stderr=subprocess.PIPE).stderr.decode("utf-8")


def ipIsValid(IP, iprange=False):
    """
    Checks that the string passed in entirely consists of an IPv4 address or a range of IP's
    (fping has changed this from Tracert and arp. This will be checked)

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

    search = "\A" + an_ipv4 + "\Z"

    if iprange:
        search += "|\A" + an_ipv4_range + "\Z"

    check = re.search(search, IP)

    if check is None:
        return False
    else:
        return True
