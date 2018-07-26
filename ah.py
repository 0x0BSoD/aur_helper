#!/usr/bin/env python
import argparse
from requests import get
import lib.search as search

parser = argparse.ArgumentParser()

parser.add_argument("action", choices=['install', 'search', 'info'], help="Awailable actions")
parser.add_argument("package_name", help="Name package placed in AUR")
# parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true", default=0)
parser.add_argument("-s", "--sort", help="For search, sort by 0 - Name, 2 - Update date, 3 - Votes", default=2)


args = parser.parse_args()

if args.action == "search":
    search.run(args.package_name, args.sort)

elif args.action == "install":
    pass
elif args.action == "info":
    pass

