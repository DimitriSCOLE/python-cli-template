# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import json
import sys
import re
import traceback
from os.path import expanduser
import os
import urllib

from uforge.objects.uforge import *
import download_utils
import printer

__author__="UShareSoft"


def extract_id(uri):
        elements = uri.split("/");
        return elements[len(elements) - 1];                

def query_yes_no(question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        valid = {"yes":True,   "y":True,  "ye":True,
                 "no":False,     "n":False}
        if default == None:
                prompt = " [y/n] "
        elif default == "yes":
                prompt = " [Y/n] "
        elif default == "no":
                prompt = " [y/N] "
        else:
                raise ValueError("invalid default answer: '%s'" % default)

        while True:
                printer.out(question + prompt)
                choice = raw_input().lower()
                if default is not None and choice == '':
                        return valid[default]
                elif choice in valid:
                        return valid[choice]
                else:
                        printer.out("Please respond with 'yes' or 'no' "\
                                     "(or 'y' or 'n').\n")
                             
                             
def remove_special_chars(string):
        return (re.sub('[-]', '_', string)).lower()

def is_uforge_exception(e):
        if len(e.args)>=1 and type(e.args[0]) is UForgeError:
                return True

def get_uforge_exception(e):
    if len(e.args)>=1 and type(e.args[0]) is UForgeError:
        return "UForge Error '"+str(e.args[0].statusCode)+"' with method: "+e.args[0].requestMethod+" "+e.args[0].requestUri+"\n"+"Message:\n\t"+e.args[0].get_localizedErrorMsg().message


def print_uforge_exception(e):
        if len(e.args)>=1 and type(e.args[0]) is UForgeError:
                printer.out(get_uforge_exception(e), printer.ERROR)
        else:
                traceback.print_exc()
                
def oder_list_object_by(objects, attribute):
        if type(attribute) is str:
                return sorted(objects, key=lambda x: getattr(x, attribute).lower(), reverse=False)
                
        return objects
    
def get_uforge_url_from_ws_url(ws_url):
        if ws_url[-1:]!='/':
                return ws_url.rpartition('/')[0]
        else:
                return ws_url[:-1].rpartition('/')[0]
            
def get_home_dir():
        return expanduser("~")
