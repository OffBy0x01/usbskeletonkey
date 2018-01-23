
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

    def __init__(self, module_name, version, module_desc, fw_requirements, options, module_help, output_format):
        self.module_name = module_name
        self.version = version
        self.module_desc = module_desc
        self.fw_requirements = fw_requirements
        self.options = options
        self.module_help = module_help
        self.output_format = output_format

