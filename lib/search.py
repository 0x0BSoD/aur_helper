import os

from json import loads
from datetime import datetime as dt
from tabulate import tabulate
from operator import itemgetter

from requests import get

def date_to_str(ds):
    return dt.fromtimestamp(ds).strftime("%Y-%m-%d")

def check_desc_ln(desc):
    rows, columns = os.popen('stty size', 'r').read().split()
    if len(desc) > int(columns)-55:
        desc = desc[:int(columns)-55] + "..."
    return desc

def run(package, sort):
    AUR = "https://aur.archlinux.org/rpc/"

    params = {
        "v": 5,
        "type": "search",
        "arg": package
    }

    r = get(AUR, params=params)
    data = loads(r.text)
    res = []
    if data.get("resultcount") == 0:
        print(f"Package {package} not found")
    else:
        res = [[i["Name"], check_desc_ln(i["Description"]), date_to_str(i["LastModified"]), i["NumVotes"]] for i in data.get("results")]

        res = sorted(res, key=itemgetter(int(sort)), reverse=True)

        print(tabulate(res, headers=["Name", "Description", "Last Update", "Votes"]))
