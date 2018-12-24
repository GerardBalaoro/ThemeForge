"""ThemeForge Executable Script
"""


from core import *
import ui, tools

if __name__ == '__main__':
    from argparse import *
    import os

    parser = ArgumentParser(description='Theme Compiler for Android-Based Operating Systems')
    parser.add_argument('path', metavar='PATH', type=str, help='path to `forge.json` (will use existing config) or directory (will initialize new workspace)')
    parser.add_argument('-b', '--build', metavar='FILE PATH', help='build and compile theme to specified file path', default=None)
    parser.add_argument('-u', '--unpack', metavar='FILE PATH', help='unpack a compiled theme from specified file path', default=None)
    
    args = parser.parse_args()

    if not os.path.exists(args.path):
        os.mkdir(args.path)

    theme = Theme(args.path)

    if args.build is not None:
        theme.build(os.path.realpath(args.build))
    elif args.unpack is not None:
        theme.unpack(os.path.realpath(args.unpack))