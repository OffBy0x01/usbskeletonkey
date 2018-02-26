import subprocess


class NMAP:

    def __init__(self):
        self.target_is_a_file = True
        self.ip_list = "targets.txt"
        self.ip = "test"
        self.service_verbosity_level = "9"
        self.speed = "-T4"
        self.save_to_file = False
        self.file_name = " > temp.txt"
        self.command = ["nmap"]

    def check_if_file(self):
        if self.target_is_a_file:  # If there isn't a target list
            self.command = self.command + ["-iL", self.ip_list]  # Add the IP list to the command

        else:
            self.command = self.command + [self.ip]  # Add the IP address(es) to the command

        return

    def nmap_loud(self):

        self.command = ["nmap"]
        self.check_if_file()
        self.command = self.command + ["-sV", "--version-intensity", self.service_verbosity_level, self.speed, "-O"]

        if self.save_to_file:
            self.command.append(self.file_name)

        print(self.command)  # debug
        return subprocess.run(self.command, stdout=subprocess.PIPE).stdout.decode("utf-8")

    def nmap_quiet(self):

        self.command = ["nmap"]
        self.check_if_file()
        self.service_verbosity_level = "1"
        self.speed = "-T2"
        self.command = self.command + ["-sV", "--version-intensity", self.service_verbosity_level, self.speed, "-O",
                                       "-D"]
        if self.save_to_file:
            self.command.append(self.file_name)

        print(self.command)  # debug
        return subprocess.run(self.command, stdout=subprocess.PIPE).stdout.decode("utf-8")


test = NMAP()
test.nmap_loud()
test.nmap_quiet()
test.nmap_loud()













