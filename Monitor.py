# -*- coding: utf-8 -*-
import os
import sys
from Gui import GuiMode
from Console import ConsoleMode
os.chdir(sys.path[0])

def main():
    if len(sys.argv) != 2:
        print("Usage: python monitor.py arg(1-console 2-GUI) ")
        #sys.exit(1)
    #arg = sys.argv[1]
    arg = '2'
    if arg=='1':
        ConsoleMode()
    elif arg=='2':
        GuiMode()
    else:
        print("please select console mode or GUI mode")

if __name__ == "__main__":
    main()
    

