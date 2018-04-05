class TargetInfo:
    """
    To be used with Run to create a tuple of (TargetIP, TargetInfo) for each target ip
    """
    def __init__(self):
        self.RESPONDS_ICMP = False
        self.RESPONDS_ARP = False
        self.MAC_ADDRESS = ""
        self.ADAPTER_NAME = ""
        self.ROUTE = []
        self.OS_INFO = []
        self.SOFTWARE_INFO = []
        self.WORKGROUP = []
        self.DOMAIN = []  # USERS + GROUPS
        self.LOCAL = []  # USERS + GROUPS
        self.SESSIONS = []
        self.NBT_STAT = []
        self.SHARE_INFO = []  # include SMB info?
        self.PASSWD_POLICY = []
        self.PRINTER_INFO = []
        self.PORTS = []  # prolly formatted like this "PORT_NUMBER, SERVICE, STATUS"