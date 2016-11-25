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

from http.server import HTTPServer, CGIHTTPRequestHandler

import colorama
from colorama import Fore, Back, Style


class SettingsFile:
    settings_filename = "server"
    settings_section_name = "Server"


class Config:  # Default values
    port_number = 9012
    workspace = "doc/"


class Pyttp:
    version = "1.0.11"

    def pyttp(self):
        self.intro()
        print("Loading settings from file %s..." % (Fore.LIGHTYELLOW_EX + SettingsFile.settings_filename + ".cfg" + Style.RESET_ALL))
        settingsfile_exist = os.path.isfile(SettingsFile.settings_filename + ".cfg")
        
        if settingsfile_exist:
            print(Fore.GREEN + "Settings file exists! Now loading..." + Style.RESET_ALL)
            c = self.get_config()
            self.apply_settings(Util.config_section_map(SettingsFile.settings_section_name, c))
        else:
            print(Fore.YELLOW + "Settings file does not exist! Creating default one..." + Style.RESET_ALL)
            Util.create_default_settings(SettingsFile.settings_filename)

        print(Fore.GREEN + "Done!" + Style.RESET_ALL)

        print("Detected workspace " + Fore.LIGHTYELLOW_EX + Config.workspace + Style.RESET_ALL + ".")

        workspace_exists = os.path.isdir(Config.workspace)
        if workspace_exists:
            print(Fore.GREEN + "Workspace is a directory" + Style.RESET_ALL)
            os.chdir(Config.workspace)
        else:
            print(Fore.YELLOW + "Workspace does not exist (or is not a directory).\n  Creating directory set in config..." + Style.RESET_ALL)
            os.makedirs(Config.workspace)
            os.chdir(Config.workspace)
            # return

        print("Starting web server on port " + Fore.LIGHTYELLOW_EX + str(Config.port_number) + Style.RESET_ALL + "...")

        print("Checking if port %s is free..." % (Fore.LIGHTYELLOW_EX + ("%i" % Config.port_number) + Style.RESET_ALL))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_free = sock.connect_ex(("127.0.0.1", Config.port_number))
        if port_free == 0:
            print(Fore.LIGHTRED_EX + "Port is occupied!" + Style.RESET_ALL)
            return
        else:
            print(Fore.GREEN + "Port is free" + Style.RESET_ALL)

        print("Server should now be accessible from %s!" % (Fore.LIGHTMAGENTA_EX + ("http://127.0.0.1:%i" % Config.port_number) + Style.RESET_ALL))

        print("Requests will be displayed " + Fore.LIGHTCYAN_EX + "cyan" + Style.RESET_ALL + "!")
        print(Fore.LIGHTCYAN_EX)

        serv = HTTPServer(('', Config.port_number), CGIHTTPRequestHandler)
        serv.serve_forever()

    @staticmethod
    def intro():
        colorama.init()
        (width, height) = Util.get_terminal_size()
        B = Back.LIGHTBLACK_EX + " " + Back.BLACK
        print(Back.LIGHTBLACK_EX, end="")  # Dark gray color
        print(" " * width)  # 65)
        print(Back.BLACK, end="")
        print(Fore.LIGHTGREEN_EX, end="")  # Lime color
        print((" " * 30) + B)
        print(Fore.LIGHTGREEN_EX + "              _   _           " + B)
        print(
            Fore.LIGHTGREEN_EX + "             | | | |          " + B + Fore.LIGHTWHITE_EX +
            " Welcome to pyttp %s!" % Pyttp.version)
        print(Fore.LIGHTGREEN_EX +
              "  _ __  _   _| |_| |_ _ __    " + B + Fore.WHITE + " Copyright 2016 Jonas Kohl")
        print(Fore.LIGHTGREEN_EX + " | '_ \| | | | __| __| '_ \   " + B)
        print(Fore.LIGHTGREEN_EX + " | |_) | |_| | |_| |_| |_) |  " + B)  # j+ Fore.WHITE + "Press Ctrl+C at any time to")
        print(Fore.LIGHTGREEN_EX + " | .__/ \__, |\__|\__| .__/   " + B, end="")  # + Fore.WHITE + "stop the server!")
        print(Back.LIGHTBLACK_EX, end="")  # Dark gray color
        print(" " * (width - 31))  # 65)
        print(Back.BLACK, end="")
        print(Fore.LIGHTGREEN_EX + " | |     __/ |       | |      " + B)
        print(Fore.LIGHTGREEN_EX + " |_|    |___/        |_|      " + B + Fore.WHITE + " The log will be displayed below!")
        print((" " * 30) + B)
        print((" " * 30) + B)
        print(Back.LIGHTBLACK_EX, end="")  # Dark gray color
        print(" " * width)  # 65)
        print(Back.BLACK, end="")
        print(Style.RESET_ALL, end="")
        print("\n")

    @staticmethod
    def get_config():
        c = configparser.ConfigParser()
        c.read("%s.cfg" % SettingsFile.settings_filename)
        return c

    @staticmethod
    def apply_settings(configmap):
        Config.port_number = int(configmap['port'])
        Config.workspace = configmap['workspace']


class Util:
    @staticmethod
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

    @staticmethod
    def config_section_map(section, config):
        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
            except:
                print(Fore.LIGHTRED_EX + ("Exception while reading settings on %s!" % option) + Style.RESET_ALL)
                dict1[option] = None
        return dict1

    @staticmethod
    def create_default_settings(filename):
        cfg = configparser.ConfigParser()
        cfgfile = open(filename + ".cfg", 'w')

        cfg.add_section('Server')
        cfg.set('Server', 'Port', str(Config.port_number))
        cfg.set('Server', 'Workspace', Config.workspace)
        cfg.write(cfgfile)
        cfgfile.close()
        return True


p = Pyttp()
p.pyttp()
