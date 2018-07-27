#!/usr/bin/env python
import argparse
import lib.search as search
import lib.info as info
import lib.install as install

parser = argparse.ArgumentParser()

parser.add_argument("action", choices=['install', 'search', 'info'], help="Awailable actions")
parser.add_argument("package_name", help="Name package placed in AUR")
parser.add_argument("-s", "--sort", help="For search, sort by 0 - Name, 2 - Update date, 3 - Votes", default=2)


args = parser.parse_args()

if args.action == "search":
    search.run(args.package_name, args.sort)

elif args.action == "install":
    install.run(args.package_name)
    
elif args.action == "info":
    info.run(args.package_name)
