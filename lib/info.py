from json import loads
from datetime import datetime as dt
from tabulate import tabulate
from operator import itemgetter

from requests import get

def date_to_str(ds):
    return dt.fromtimestamp(ds).strftime("%Y-%m-%d")

def check_desc_ln(desc):
    if len(desc) > 80:
        desc = desc[:77] + "..."
    return desc

def run(package):

    headers = ["Name",
               "Version",
               "Description",
               "Maintainer",
               "Maintainer URL",
               "Votes",
               "Added to AUR",
               "Last Updated",
               "URL to tar.gz"]

    AUR = "https://aur.archlinux.org"

    params = {
        "v": 5,
        "type": "search",
        "arg": package
    }

    r = get(f"{AUR}/rpc/", params=params)
    data = loads(r.text)
    if data.get("resultcount") == 0:
        print(f"Package {package} not found in AUR")
    else:
        for i in data.get("results"):
            if i["Name"] == package:
                pkg = [
                    i["Name"], i["Version"], i["Description"],
                    i["Maintainer"], i["URL"], i["NumVotes"],
                    date_to_str(i["FirstSubmitted"]),
                    date_to_str(i["LastModified"]),
                    AUR + i["URLPath"]
                ]

                for i in enumerate(headers):
                    spaces = ' '*(15 - len(i[1]))
                    print(f"{headers[i[0]]}{spaces}:{pkg[i[0]]}")
                return 0
    print(f"Package {package} not found in AUR")
