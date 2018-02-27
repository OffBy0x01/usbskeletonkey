import socket

# From https://stackoverflow.com/a/4017219

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False

        return address.count('.') == 3

    # Address invalid
    except socket.error:
        return False

    # Address is valid
    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)

    # Address invalid
    except socket.error:
        return False

    # Address is valid
    return True