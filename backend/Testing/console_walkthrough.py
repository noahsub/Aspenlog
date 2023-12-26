from backend.Constants.seismic_constants import SiteDesignation, SiteClass
from backend.Entities.location import Location

LINE = '_'*80

if __name__ == '__main__':
    print(LINE)
    print("ASPENLOG 2020 CONSOLE WALKTHROUGH")
    print(LINE)

    # Step 0
    print("Step #0")
    print(LINE)
    address = input("Address: ")
    print("Select site designation type:")
    for i, type in enumerate(['Vs30 (Xv)', 'Site Class (Xs)']):
        print(f'\t{i}: {type}')
    location = None
    match int(input("Selection: ")):
        case 0:
            xv = int(input("Vs30 Value [140, 3000] m/s: "))
            location = Location(address=address, site_designation=SiteDesignation.XV, xv=xv)
        case 1:
            print("Select site class: ")
            site_class_mapping = {}
            for i, type in enumerate(SiteClass):
                site_class_mapping[i] = type
                print(f'\t{i}: {type.value}')
            location = Location(address=address, site_designation=SiteDesignation.XS, xs=site_class_mapping[int(input("Selection: "))])
    print("Obtained Values: ")
    print(location)


