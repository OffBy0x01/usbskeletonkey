import  os, re, configparser

class skeleton-key():

    #This hasn't been updated yet so ignore the init for now.
    def __init__():
        #initialize framework components
        interface = framework.ui()
        keyboard = framework.keyboard()
        network = framework.network()
        storage = framework.storage()
        io = framework.io()

        #get directory and check modules folder exists
        dir_path = os.path.dirname(os.path.realpath(__file__))

    def discover_modules(dir_path):
        #get the module paths from modules directory
        print("Looking for modules...")
        module_paths = os.listdir(dir_path+"/modules")

        #regex to look for .py files
        py = re.compile("\.py", re.IGNORECASE)
        module_paths = filter(py.search, module_paths)

        #identify module name from file path
        identify_module = lambda m: os.path.splitext(m)[0]
        return ([identify_module(m) for m in module_paths])

    def get_modules():
        if not module_list:
            module_list = discover_modules()


    def init_config():

        if not (os.path.exists(dir_path+"/modules")):
            #doesn't exist - user can fix themselves
            print("Error: "+dir_path+"\"modules\" directory does not exist!")
            exit()

        present_modules = get_modules(dir_path)

        #if no modules present exit
        if not present_modules:
            print("Error: No modules found!")
            exit()
        else:
            print('Configuring modules:')
            print(*present_modules, sep=',\n')

        #generate configuration file and add the required sections
        config = configparser.ConfigParser()
        config.read(dir_path+'/config.ini')
        config.add_section('components')
        config.add_section('modules')
        config.add_section('interface')
        config.add_section('general')

        #add to modules to config.ini:active_modules
        for mod in present_modules:
            config.set('modules', mod, "True")

        with open(dir_path+'/config.ini', 'w') as f:
            config.write(f)

        print('Done!')

