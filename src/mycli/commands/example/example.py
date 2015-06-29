
__author__="UShareSoft"

from mycli.lib.argumentParser import ArgumentParser, ArgumentParserError
from mycli.lib.cmdMy import Cmd, CmdGlobal
from mycli.utils import *



class Example(Cmd, CmdGlobal):
        """This is an example"""
    
        cmd_name="example"
    
        def __init__(self):
                super(Example, self).__init__()

    
        def arg_test(self):
                doParser = ArgumentParser(prog=self.cmd_name+" test", add_help = True, description="This is the command text")
                return doParser   

        def do_test(self, args):
                printer.out("Test")
                printer.out("PASSED", printer.OK)
                    
        def help_test(self):
                doParser = self.arg_test()
                doParser.print_help()
