'''
	mycli
'''

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import argparse
import getpass
import base64
import httplib2
import os
import sys


from lib.cmdMy import Cmd, CmdUtils
from lib.argumentParser import MyArgumentParser, ArgumentParser, ArgumentParserError
import commands
from uforge.application import Api
from utils import *


__author__ = "UShareSoft"
__license__ = "Apache License 2.0"





class CmdBuilder(object):
        @staticmethod
	def generateCommands(class_):
		# Create subCmds if not exist
		if not hasattr(class_, 'subCmds'):
			class_.subCmds = {}
                        
		# Add commands                
		example = commands.example.Example()
		class_.subCmds[example.cmd_name] = example
                

## Main cmd
class Mycli(Cmd):
#	subCmds = {
#		'tools': CmdUtils
#	}
	def __init__(self):
		super(Mycli, self).__init__()
		self.prompt = 'mycli> '
                
        def do_exit(self, args):
                return True
            
        def do_quit(self, args):
                return True
        
       
        def arg_batch(self):
                doParser = ArgumentParser("batch", add_help = True, description="Execute mycli batch command from a file (for scripting)")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--file', dest='file', required=True, help="mycli batch file commands")
                return doParser      
            
        def do_batch(self, args):
                try:
                        doParser = self.arg_batch()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        with open(doArgs.file) as f:             
                                for line in f:
                                        try:
                                                self.run_commands_at_invocation([line])
                                        except:
                                                printer.out("bad command '"+line+"'", printer.ERROR)
                                        print "\n"
                                        
                except IOError as e:
                        printer.out("File error: "+str(e), printer.ERROR)
                        return
                except ArgumentParserError as e:
                        printer.out("In Arguments: "+str(e), printer.ERROR)
                        self.help_batch()
                
        def help_batch(self):
                doParser = self.arg_batch()
                doParser.print_help()
                

	def cmdloop(self, args):
		if len(args):
			code = self.run_commands_at_invocation([str.join(' ', args)])
			sys.exit(code)
		else:
			self._cmdloop() 



def generate_base_doc(app, hamm_help):
        myactions=[]
        cmds= sorted(app.subCmds)
        for cmd in cmds:
                myactions.append(argparse._StoreAction(
                 option_strings=[],
                 dest=str(cmd),
                 nargs=None,
                 const=None,
                 default=None,
                 type=str,
                 choices=None,
                 required=False,
                 help=str(app.subCmds[cmd].__doc__),
                 metavar=None))
        
        return myactions
    
def set_globals_cmds(subCmds):
        for cmd in subCmds:
                if hasattr(subCmds[cmd], 'set_globals'):
                        subCmds[cmd].set_globals(api, username, password)
                        if hasattr(subCmds[cmd], 'subCmds'):
                                set_globals_cmds(subCmds[cmd].subCmds)


#Generate mycli base command + help base command
CmdBuilder.generateCommands(Mycli)
app = Mycli()
myactions=generate_base_doc(app, hamm_help="")


# Args parsing
mainParser = MyArgumentParser(add_help=False)
MyArgumentParser.mycli_actions=myactions
mainParser.add_argument('-a', '--url', dest='url', type=str, help='the server URL endpoint to use', required = False)
mainParser.add_argument('-u', '--user', dest='user', type=str, help='the user name used to authenticate to the server', required = False)
mainParser.add_argument('-p', '--password', dest='password', type=str, help='the password used to authenticate to the server', required = False)
mainParser.add_argument('-v', action='version', help='displays the current version of the mycli tool', version="%(prog)s version '"+constants.VERSION+"'")
mainParser.add_argument('-h', '--help', dest='help', action='store_true', help='show this help message and exit', required = False)
mainParser.set_defaults(help=False)
mainParser.add_argument('cmds', nargs='*', help='Hammr cmds')
mainArgs, unknown = mainParser.parse_known_args()


if mainArgs.help and not mainArgs.cmds:
        mainParser.print_help()
        exit(0)

if mainArgs.user is not None and mainArgs.url is not None:
        if not mainArgs.password:
                mainArgs.password = getpass.getpass()
        username=mainArgs.user
        password=mainArgs.password
        url=mainArgs.url
        sslAutosigned=True
else:
        mainParser.print_help()
        exit(0)




#UForge API instanciation
client = httplib2.Http(disable_ssl_certificate_validation=sslAutosigned, timeout=constants.HTTP_TIMEOUT)
#activate http caching
#client = httplib2.Http(generics_utils.get_mycli_dir()+os.sep+"cache")
headers = {}
headers['Authorization'] = 'Basic ' + base64.encodestring( username + ':' + password )
api = Api(url, client = client, headers = headers)
set_globals_cmds(app.subCmds)

if mainArgs.help and len(mainArgs.cmds)>=1:
        argList=mainArgs.cmds + unknown;
        argList.insert(len(mainArgs.cmds)-1, "help")
        app.cmdloop(argList)
elif mainArgs.help:
        app.cmdloop(mainArgs.cmds + unknown + ["-h"])
else:
        app.cmdloop(mainArgs.cmds + unknown)
