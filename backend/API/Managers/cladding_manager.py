from backend.Entities.Building.cladding import CladdingBuilder


def process_cladding_data(c_top: float, c_bot: float):
    cladding_builder = CladdingBuilder()
    cladding_builder.set_c_top(c_top)
    cladding_builder.set_c_bot(c_bot)
    return cladding_builder.get_cladding()
