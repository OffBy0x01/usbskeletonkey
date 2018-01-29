
class ModuleDescriptor(object):
    """
    Desc:
        Module base class to provide metadata on individual modules
        All passed variables are required thus no default values

    Args:
        module_name:        module name
        version:            version number
        module_desc:        module description
        fw_requirements:    required framework components
        options:            module specific arguments
        module_help:        module specific help output
        output_format:      list of definable output formats e.g. ["XML","plaintext"]

    """

    def __init__(self, module_name, module_desc, options, fw_requirements, output_format, version=1, module_help ="You're on your own buddy!"):
        self.module_name = module_name
        self.module_desc = module_desc

        self.options = {
            "enabled": False
        }.update(options)

        self.fw_requirements = {
            "keyboard": False,
            "network": False,
            "storage": False
            }.update(fw_requirements)

        self.output_format = {
            "success": bool
        }.update(output_format)

        self.version = version
        self.module_help = module_help



