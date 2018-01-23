
import os
import re

from framework.helper.singleton import Singleton


@Singleton
class ModuleManager:

    def __init__(self):
        self.module_list = self.discover_modules()

    def discover_modules(self):
        # get the module paths from modules directory
        print("Looking for modules...")
        module_paths = os.listdir(self.module_path)

        # regex to look for .py files
        py = re.compile("\.py", re.IGNORECASE)
        module_paths = filter(py.search, module_paths)

        # identify module name from file path
        return [os.path.splitext(m)[0] for m in module_paths]

        # .__thisclass__ == current class
        # .__self_class__ == class of self argument (usually the child)
        # https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
