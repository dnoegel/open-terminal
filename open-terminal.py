# coding: utf-8

from gi.repository import Nautilus, GObject, GConf


import os
import urllib
import subprocess

TERMINAL_KEY = '/desktop/gnome/applications/terminal/exec'

def uri_from_path(nautilus_file):
    """ Turn natuilus-file-uri into a valid path if possible"""
    
    if nautilus_file.get_uri_scheme() == 'file':
        return urllib.unquote(nautilus_file.get_uri()[7:])
    else:
        return ""

def get_default_terminal():
    """Get default terminal"""
    
    client = GConf.Client.get_default()
    return client.get_string(TERMINAL_KEY)

def run_terminal(path):
    """Change cwd to given directory and run terminal.
    
    Somehow changing cwd isn't the best solution, passing it as an
    argument to the terminal would do much better."""
    
    os.chdir(path)
    subprocess.call([get_default_terminal()])

class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def menu_activate_cb(self, menu, nautilus_file):
        run_terminal(uri_from_path(nautilus_file))

    def get_file_items(self, window, nautilus_files):
        if nautilus_files != [] and os.path.isdir(uri_from_path(nautilus_files[0])):
            item = Nautilus.MenuItem(
                name="showInTerminalExtension::Terminal hier öffnen",
                label="Terminal hier öffnen" ,
                tip="Terminal hier öffnen"
            )
            item.connect('activate', self.menu_activate_cb, nautilus_files[0])
            
            return item,
    
    def get_background_items(self, window, nautilus_file):
        item = Nautilus.MenuItem(
            name="showInTerminalExtension::Terminal hier öffnen",
            label="Terminal hier öffnen" ,
            tip="Terminal hier öffnen"
        )
        item.connect('activate', self.menu_activate_cb, nautilus_file)
        
        return item,
