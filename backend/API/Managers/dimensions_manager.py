from backend.Entities.Building.dimensions import BasicDimensionsBuilder, EaveRidgeDimensionsBuilder


def process_dimension_data(width: float, height: float = None, eave_height: float = None, ridge_height: float = None):
    if eave_height is None and ridge_height is None:
        dimensions_builder = BasicDimensionsBuilder()
        dimensions_builder.set_height(height)
        dimensions_builder.set_width(width)
    else:
        dimensions_builder = EaveRidgeDimensionsBuilder()
        dimensions_builder.set_width(width)
        dimensions_builder.set_height_eave(eave_height)
        dimensions_builder.set_height_ridge(ridge_height)
        dimensions_builder.compute_height()
    return dimensions_builder.get_dimensions()
