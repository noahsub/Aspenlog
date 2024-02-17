from backend.Entities.Building.roof import RoofBuilder


def process_roof_data(w_roof: float, l_roof: float, slope: float, uniform_dead_load: float):
    roof_builder = RoofBuilder()
    roof_builder.set_w_roof(w_roof)
    roof_builder.set_l_roof(l_roof)
    roof_builder.set_slope(slope)
    roof_builder.compute_wall_slope()
    roof_builder.set_wp(uniform_dead_load)
    return roof_builder.get_roof()
