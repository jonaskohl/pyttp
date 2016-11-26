#!/usr/bin/env python

#               _   _ 
#              | | | |
#   _ __  _   _| |_| |_ _ __
#  | '_ \| | | | __| __| '_ \
#  | |_) | |_| | |_| |_| |_) |
#  | .__/ \__, |\__|\__| .__/
#  | |     __/ |       | |
#  |_|    |___/        |_|     Copyright 2016 Jonas Kohl

import os
import configparser
import socket
import sys
import webbrowser

from http.server import HTTPServer, CGIHTTPRequestHandler


class SettingsFile:
    settings_filename = "pyttp"
    settings_section_name = "Server"


class Config:  # Default values
    pyttp_version = ""
    port_number = 9012
    workspace = "html/"
    openbrowser = True

version = "1.0.21" # Do NOT change this value!


def pyttp():
    intro()
    print("Loading settings from file %s..." % (SettingsFile.settings_filename + ".cfg"))
    settingsfile_exist = os.path.isfile(SettingsFile.settings_filename + ".cfg")
    
    if settingsfile_exist:
        print("Settings file exists! Now loading...")
        c = get_config()
        apply_settings(config_section_map(SettingsFile.settings_section_name, c))
        if Config.pyttp_version != version:
            print("Warning: Versions do not match! (%s != %s)" % (Config.pyttp_version, version))
    else:
        print("Settings file does not exist! Creating default one...")
        create_default_settings(SettingsFile.settings_filename)

    print("Done!")

    print("Detected workspace " + Config.workspace + ".")

    workspace_exists = os.path.isdir(Config.workspace)
    if workspace_exists:
        print("Workspace is a directory")
        os.chdir(Config.workspace)
    else:
        print("Workspace does not exist (or is not a directory).\n  Creating directory set in config...")
        os.makedirs(Config.workspace)
        os.chdir(Config.workspace)
        print("Workspace created! Place your files inside of %s!" % Config.workspace)

    print("Starting web server on port " + str(Config.port_number) + "...")

    print("Checking if port %i is free..." % Config.port_number)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_free = sock.connect_ex(("127.0.0.1", Config.port_number))
    if port_free == 0:
        print("Port is occupied!")
        return
    else:
        print("Port is free")

    print("Server should now be accessible from %s!" % ("http://127.0.0.1:%i" % Config.port_number))
    print("Server requests will be displayed below:")
    
    if Config.openbrowser:
        webbrowser.open("http://127.0.0.1:%i" % Config.port_number, 0)

    serv = HTTPServer(('', Config.port_number), CGIHTTPRequestHandler)
    serv.serve_forever()


def intro():
    (width, height) = get_terminal_size()
    print("              _   _           ")
    print("             | | | |           Welcome to pyttp %s!" % version)
    print("  _ __  _   _| |_| |_ _ __     Copyright 2016 Jonas Kohl")
    print(" | '_ \| | | | __| __| '_ \   ")
    print(" | |_) | |_| | |_| |_| |_) |  ")
    print(" | .__/ \__, |\__|\__| .__/   ")
    print(" | |     __/ |       | |      ")
    print(" |_|    |___/        |_|       The log will be displayed below!")
    print("\n")


def get_config():
    c = configparser.ConfigParser()
    c.read("%s.cfg" % SettingsFile.settings_filename)
    return c


def apply_settings(configmap):
    Config.pyttp_version = configmap['pyttp version']
    Config.port_number = int(configmap['port'])
    Config.workspace = configmap['workspace']
    Config.openbrowser = parsebool(configmap['open browser on start'])


def get_terminal_size():
    import os
    env = os.environ

    def ioctl_gwinsz(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                 '1234'))
        except:
            return
        return cr

    cr = ioctl_gwinsz(0) or ioctl_gwinsz(1) or ioctl_gwinsz(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_gwinsz(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])


def config_section_map(section, config):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
        except:
            print("Exception while reading settings on %s!" % option)
            dict1[option] = None
    return dict1


def create_default_settings(filename):
    cfg = configparser.ConfigParser()
    cfgfile = open(filename + ".cfg", 'w')

    cfg.add_section('Server')
    cfg.set('Server', 'pyttp Version', str(version))
    cfg.set('Server', 'Port', str(Config.port_number))
    cfg.set('Server', 'Workspace', str(Config.workspace))
    cfg.set('Server', 'Open Browser On Start', str(Config.openbrowser))
    cfg.write(cfgfile)
    cfgfile.close()
    return True


def parsebool(v):
    if v.lower() in ("yes", "true", "t", "1", "on", "y"):
        return True
    elif v.lower() in ("no", "false", "f", "0", "off", "n"):
        return False
    else:
        raise ValueError("parsebool() Error: Passed value does not represent a boolean value!\nSupported values:\n" + 
                         "  True: \"yes\", \"true\", \"t\", \"1\", \"on\", \"y\"\n" +
                         "  False: \"no\", \"false\", \"f\", \"0\", \"off\", \"n\"")


def __main__():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--generatedefaultconfig":
            create_default_settings(SettingsFile.settings_filename + "_default")
            return
    pyttp()


# This is where the magic begins
__main__()
