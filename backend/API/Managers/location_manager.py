from backend.Constants.seismic_constants import SiteDesignation, SiteClass
from backend.Entities.Location.location import LocationXvBuilder, LocationXsBuilder


def process_location_data(address: str, site_designation: str, seismic_value: int | str):
    site_designation = SiteDesignation.get_key_from_value(site_designation)
    if site_designation == SiteDesignation.XS:
        seismic_value = SiteClass.get_key_from_value(seismic_value)
    match site_designation:
        case SiteDesignation.XV:
            location_builder = LocationXvBuilder()
        case SiteDesignation.XS:
            location_builder = LocationXsBuilder()
    location_builder.set_address(address)
    location_builder.set_coordinates()
    location_builder.set_climatic_data()
    location_builder.set_seismic_data(seismic_value)
    return location_builder.get_location()
