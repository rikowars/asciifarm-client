

import argparse
import getpass
import json
import os
import os.path

from . import loaders


defaultAdresses = {
    "abstract": "rustifarm",
    "unix": "asciifarm.socket",
    "inet": "localhost:9021",
}

def parse_args(argv):

    parser = argparse.ArgumentParser(description="The client to AsciiFarm. Run this to connect to to the server.", epilog="""
    Gameplay information:
        Walk around and explore the rooms.
        Kill the goblins and plant the seeds.

    ~troido""", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-n', '--name', help='Your player name (must be unique!). Defaults to username on inet sockets and tildename on unix socket (including abstract). Apart from the tilde in a tildename all characters must be unicode letters, numbers or connection puctuation. The maximum size of a name is 256 bytes when encoded as utf8', default=None)
    parser.add_argument("-a", "--address", help="The address of the socket. When the socket type is 'abstract' this is just a name. When it is 'unix' this is a filename. When it is 'inet' is should be in the format 'address:port', eg 'localhost:8080'. Defaults depends on the socket type")
    parser.add_argument("-s", "--socket", help="the socket type. 'unix' is unix domain sockets, 'abstract' is abstract unix domain sockets and 'inet' is inet sockets. ", choices=["abstract", "unix", "inet"], default="abstract")
    parser.add_argument('-k', '--keybindings', help='The file with the keybinding configuration. This file is a JSON file.', default="default")
    parser.add_argument('-c', '--characters', help='The file with the character mappings for the graphics. If it is either of these names: {} it will be loaded from the charmaps directory.'.format(list(loaders.standardCharFiles.keys())), default="default")
    parser.add_argument('-o', '--logfile', help='All game messages will be written to this file.', default=None)
    parser.add_argument('--reset-style', help='Reset the style when it changes. Useful on some terminals', action="store_true")
    parser.add_argument('--blink-bright-background', help='Use blink attribute to make background brighter. Useful for terminals that don\'t have bright backgrounds usually. Implies --reset-style', action="store_true")
    
    colourGroup = parser.add_mutually_exclusive_group()
    colourGroup.add_argument('-l', '--colours', '--colors', help='enable colours! :)', action="store_true")
    colourGroup.add_argument('-b', '--nocolours', '--nocolors', help='disable colours! :)', action="store_true")
    
    args = parser.parse_args(argv)
    
    charmap = loaders.loadCharmap(args.characters)
    
    keybindings = loaders.loadKeybindings(args.keybindings)
    
    address = args.address
    if address is None:
        address = defaultAdresses[args.socket]
    if args.socket == "abstract":
        address = '\0' + address
    elif args.socket == "inet":
        hostname, sep, port = address.partition(':')
        address = (hostname, int(port))
    
    colours = True
    if args.colours:
        colours = True
    elif args.nocolours:
        colours = False
    
    name = args.name
    if name is None:
        username = getpass.getuser()
        if args.socket == "unix" or args.socket == "abstract":
            name = "~"+username
        else:
            name = username
    
    return (name, args.socket, address, keybindings, charmap, colours, args.logfile, {"always_reset": args.reset_style, "blink_bright_background": args.blink_bright_background})
