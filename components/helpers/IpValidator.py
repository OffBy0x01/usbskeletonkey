import re
import socket


# From https://stackoverflow.com/a/4017219


class IpValidator:
    @staticmethod
    def is_valid_ipv4_address(IP, iprange=False):
        """
        Checks that the string passed in entirely consists of an IPv4 address or a range of IP's

        Args:
        :param IP:      string that is being checked as a valid IP
        :param iprange: Will also allow for IP ranges to be valid

        :return: boolean indicating if the IP is valid, True for valid IP
        """

        ip_range = "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # This checks a number is within 0-255
        an_ipv4 = ip_range + "\." + ip_range + "\." + ip_range + "\." + ip_range  # This regex will check its a IP

        an_ipv4_range = an_ipv4 + "\/[0-2][0-9]|" + an_ipv4 + "\/3[0-2]"  # This checks IP ranges such as 192.168.0.0/24
        # The checks with this one are more lax. Still error prone
        # 192.168.0.0/24

        search = "\A" + an_ipv4 + "\Z"

        if iprange:
            search += "|\A" + an_ipv4_range + "\Z"

        check = re.search(search, IP)

        if check is None:
            return False
        else:
            return True

    @staticmethod
    def is_valid_ipv6_address(address):
        try:
            socket.inet_pton(socket.AF_INET6, address)

        # Address invalid
        except socket.error:
            return False

        # Address is valid
        return True
