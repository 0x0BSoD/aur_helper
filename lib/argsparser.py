import argparse

parser = argparse.ArgumentParser()

parser.add_argument("action", help="install | search")

# group = parser.add_mutually_exclusive_group()
# group.add_argument("search", help="Search info about package placed in AUR")
# group.add_argument("install", help="Install package placed in AUR")

parser.add_argument("package_name", help="Name package placed in AUR")
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true", default=0)

args = parser.parse_args()
