from json import loads
from datetime import datetime as dt
from tabulate import tabulate
from operator import itemgetter
from subprocess import Popen, DEVNULL
from os import path, makedirs, chdir
from shutil import rmtree
from ast import literal_eval as make_tuple

from requests import get

def run(package):

    AUR = "https://aur.archlinux.org"
    TMP = "/tmp/ah/"
   
    params = {
        "v": 5,
        "type": "search",
        "arg": package
    }

    if not path.exists(TMP):
        makedirs(TMP)

    r = get(f"{AUR}/rpc/", params=params)
    data = loads(r.text)
    if data.get("resultcount") == 0:
        print(f"Package {package} not found in AUR")
    else:
        for i in data.get("results"):
            if i["Name"] == package:
                if not path.exists(TMP+package):
                    pkg =  AUR + i["URLPath"]

                    if path.exists(TMP+package):
                        rmtree(TMP+package)

                    print(f"Downloading {package} source ...")
                    p = Popen(["wget", 
                                pkg,
                                "-O",
                                TMP+package+".tar.gz"], stdout=DEVNULL, stderr=DEVNULL)

                    p.wait()
                    rc = p.returncode
                else:
                    print(f"Downloading {package} source skipped")
                    rc = 0

                if rc == 0:
                    print(f"Unpacking source ...")
                    chdir(TMP)
                    p = Popen(["tar", 
                                "-xzf",
                                package+".tar.gz"])
                    p.wait()
                    rc = p.returncode
                
                if rc == 0:
                    print(f"Making from source ...")
                    chdir(TMP+package)
                    pkg_dep = None
                    make_dep = None
                    with open("PKGBUILD", "r") as f:
                        for i in f:
                            line = i.split("=")
                            if "depends" in line:
                                pkg_dep = ((line[1].strip())[1:-1].split(","))
                            if "makedepends" in line:
                                make_dep = (line[1].strip())[1:-1].split(",")
                    
                    deps = []

                    if pkg_dep:
                        print(f"Package Depends:")
                        for p in pkg_dep:
                            pkg = p.replace("\'", "")
                            p = Popen(["pacman", 
                                       "-Qi",
                                       pkg], stdout=DEVNULL, stderr=DEVNULL)
                            p.wait()
                            rc = p.returncode
                            status = "Installed" if rc == 0 else "Not Installed"
                            if status == "Not Installed":
                                deps.append(pkg)
                            print("- " + pkg + f" -- {status}")
                
                    if make_dep:
                        print(f"Package build Depends:")
                        for p in make_dep:
                            pkg = p.replace("\'", "")
                            p = Popen(["pacman", 
                                       "-Qi",
                                       pkg], stdout=DEVNULL, stderr=DEVNULL)
                            p.wait()
                            rc = p.returncode
                            status = "Installed" if rc == 0 else "Not Installed"
                            if status == "Not Installed":
                                deps.append(pkg)
                            print("- " + pkg + f" -- {status}")
                    
                    if not len(deps) == 0:
                        print(f"Packages nett to be install: {deps}")
                        conf = input("yes(y)/no(n)")
                        while True:
                            if conf == "n":
                                return 1
                            elif conf == "y":
                                print("Installing...")
                                # TODO Need made this if depended pkg not in pacman repo
                                break
                            else:
                                print("Input error -- yes(y)/no(n)")
                    
                    p = Popen(["makepkg", 
                               "-si"])
                    p.wait()
                    rc = p.returncode

                    if rc == 0:
                        print("Packages succefuly installed")
                    else:
                        print(f"Some error, code: {rc}")
                        return rc 


                
                return 0
    print(f"Package {package} not found in AUR")
