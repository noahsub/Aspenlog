from backend.Entities.Seismic.seismic_factor import SeismicFactorBuilder
from backend.algorithms.seismic_load_algorithms import get_seismic_factor_values


def process_seismic_load_data(ar: float, rp: float, cp: float):
    seismic_factor_builder = SeismicFactorBuilder()
    get_seismic_factor_values(seismic_factor_builder, ar, rp, cp)
