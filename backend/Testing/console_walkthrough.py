# from backend.Constants.seismic_constants import SiteDesignation, SiteClass
# from backend.Entities.location import Location
#

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

import jsonpickle
import typer
from rich import print
from backend.Constants.seismic_constants import SiteClass, SiteDesignation
from backend.Entities.location import Location
from rich.prompt import Prompt

TERM_SIZE = os.get_terminal_size()


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
    # save obj to save.json under name using jsonpickle
    with open('save.json', 'r') as f:
        data = json.load(f)
        data[name] = jsonpickle.encode(obj)
    with open('save.json', 'w') as f:
        json.dump(data, f, indent=4)


def deserialize(name: str):
    # get obj from save.json under name
    # it should not return the string representation, but the actual object
    with open('save.json', 'r') as f:
        data = json.load(f)
        return jsonpickle.decode(data[name])


def skip_step(step: int):
    print_line()
    confirm = typer.confirm(f"Would you like to skip Step #{step}?")
    if confirm:
        match step:
            case 0:
                print_line()
                print_obtained_values(deserialize('location'))
    else:
        match step:
            case 0:
                step_0()



def print_obtained_values(obj):
    print("[bold red]Obtained Values: [/bold red]")
    lst = str(obj).split('\n')
    for i in range(len(lst)):
        print(f"  {lst[i]}")


def print_line():
    print('─' * (TERM_SIZE.columns - 1))


LOCATION = None


def step_0():
    global LOCATION
    print_line()
    address = Prompt.ask("[blue]Enter[/blue] Address")
    site_designation_type = choice(prompt="site designation type", options=SiteDesignation)
    match site_designation_type:
        case SiteDesignation.XV:
            xv = int(Prompt.ask("[blue]Enter[/blue] Vs30 value measured in situ between 140 - 3000 m/s"))
            LOCATION = Location(address=address, site_designation=SiteDesignation.XV, xv=xv)
        case SiteDesignation.XS:
            xs = choice(prompt="Site Class", options=SiteClass)
            LOCATION = Location(address=address, site_designation=SiteDesignation.XS, xs=xs)
    serialize('location', LOCATION)
    print_obtained_values(LOCATION)


if __name__ == '__main__':
    print_line()
    print("ASPENLOG 2020 CONSOLE WALKTHROUGH")

    create_save_file()
    skip_step(0)

