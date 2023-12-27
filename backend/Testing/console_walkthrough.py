# from backend.Constants.seismic_constants import SiteDesignation, SiteClass
# from backend.Entities.location import Location
#
# LINE = '_'*80
#
# if __name__ == '__main__':
#     print(LINE)
#     print("ASPENLOG 2020 CONSOLE WALKTHROUGH")
#     print(LINE)
#
#     # Step 0
#     print("Step #0")
#     print(LINE)
#     address = input("Address: ")
#     print("Select site designation type:")
#     for i, type in enumerate(['Vs30 (Xv)', 'Site Class (Xs)']):
#         print(f'\t{i}: {type}')
#     location = None
#     match int(input("Selection: ")):
#         case 0:
#             xv = int(input("Vs30 Value [140, 3000] m/s: "))
#             location = Location(address=address, site_designation=SiteDesignation.XV, xv=xv)
#         case 1:
#             print("Select site class: ")
#             site_class_mapping = {}
#             for i, type in enumerate(SiteClass):
#                 site_class_mapping[i] = type
#                 print(f'\t{i}: {type.value}')
#             location = Location(address=address, site_designation=SiteDesignation.XS, xs=site_class_mapping[int(input("Selection: "))])
#     print("Obtained Values: ")
#     print(location)
import json
import os
from enum import Enum


import typer
from rich import print
from backend.Constants.seismic_constants import SiteClass, SiteDesignation
from backend.Entities.location import Location
from rich.prompt import Prompt


def choice(prompt: str, options):
    print(f"[bold green]Select[bold /green] [bold white]{prompt}[/bold white]: ")
    mapping = {}
    for i, option in enumerate(options):
        mapping[i] = option
        print(f"  [bold red]{i}[/bold red]: [white]{option.value}[/white]")
    selection = int(input("Selection: "))
    print(f"  → [bold yellow]{mapping[selection]}[/bold yellow]")
    return mapping[selection]


def create_save_file():
    if not os.path.exists('save.json'):
        with open('save.json', 'w') as f:
            json.dump({}, f)


def serialize(name: str, obj):
    # save obj to save.json under name
    with open('save.json', 'r') as f:
        data = json.load(f)
        data[name] = obj.__dict__
    with open('save.json', 'w') as f:
        json.dump(data, f)


def deserialize(name: str):
    # get obj from save.json under name
    with open('save.json', 'r') as f:
        data = json.load(f)
        return data[name]


def skip_step(step: int, func):
    confirm = typer.confirm(f"Would you like to skip Step #{step}?")
    if confirm:
        pass
    else:
        func()

LOCATION = None

def step_0():
    address = typer.prompt("Address")
    site_designation_type = choice(prompt="site designation type", options=SiteDesignation)
    match site_designation_type:
        case SiteDesignation.XV:
            xv = int(Prompt.ask("[blue]Enter[/blue] Vs30 value measured in situ between 140 - 3000 m/s"))
            LOCATION = Location(address=address, site_designation=SiteDesignation.XV, xv=xv)
        case SiteDesignation.XS:
            xs = choice(prompt="Site Class", options=SiteClass)
            LOCATION = Location(address=address, site_designation=SiteDesignation.XS, xv=xs)
    serialize('location', LOCATION)



if __name__ == '__main__':
    create_save_file()
    skip_step(0, step_0)
