#!/usr/bin/env python


from http.server import HTTPServer, CGIHTTPRequestHandler
import colorama
from colorama import Fore, Back, Style
import os


# THE FOLLOWING VARIABLES CAN BE EDITED BY THE USER
class Config:
    port_number = 9012  # The port for the server to listen on
    workspace = "doc/"  # The document root relative to the pyttp.py script


class pyttp:
    version = "1.0.0"

    def pyttp(self):
        self.intro()

        print("Detected workspace " + Fore.LIGHTYELLOW_EX + Config.workspace + Style.RESET_ALL + ".")
        os.chdir(Config.workspace)

        print("Starting web server on port " + Fore.LIGHTYELLOW_EX + str(Config.port_number) + Style.RESET_ALL + "...")

        serv = HTTPServer(('', Config.port_number), CGIHTTPRequestHandler)
        serv.serve_forever()

    @staticmethod
    def intro():
        colorama.init()
        # (width, height) = Util.get_terminal_size()
        print(Fore.LIGHTBLACK_EX, end="")  # Dark gray color
        print("*" * 65)
        print(Fore.LIGHTGREEN_EX, end="")  # Lime color
        print(" ")
        print(Fore.LIGHTGREEN_EX + "              _   _         ")
        print(
            Fore.LIGHTGREEN_EX + "             | | | |          " + Fore.LIGHTWHITE_EX +
            "Welcome to pyttp %s!" % pyttp.version)
        print(Fore.LIGHTGREEN_EX +
              "  _ __  _   _| |_| |_ _ __    " + Fore.WHITE + "Copyright 2016 Jonas Kohl")
        print(Fore.LIGHTGREEN_EX + " | '_ \| | | | __| __| '_ \   ")
        print(Fore.LIGHTGREEN_EX + " | |_) | |_| | |_| |_| |_) |  ")  # j+ Fore.WHITE + "Press Ctrl+C at any time to")
        print(Fore.LIGHTGREEN_EX + " | .__/ \__, |\__|\__| .__/   ")  # + Fore.WHITE + "stop the server!")
        print(Fore.LIGHTGREEN_EX + " | |     __/ |       | |    ")
        print(Fore.LIGHTGREEN_EX + " |_|    |___/        |_|      " + Fore.WHITE + "The log will be displayed below!")
        print("\n")
        print(Fore.LIGHTBLACK_EX, end="")  # Dark gray color
        print("*" * 65)
        print(Style.RESET_ALL, end="")
        print("\n")


class Util:
    def get_terminal_size(self):
        import os
        env = os.environ

        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct, os
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                     '1234'))
            except:
                return
            return cr

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

            ### Use get(key[, default]) instead of a try/catch
            # try:
            #    cr = (env['LINES'], env['COLUMNS'])
            # except:
            #    cr = (25, 80)
        return int(cr[1]), int(cr[0])


p = pyttp()
p.pyttp()
