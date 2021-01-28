"""A form to calculate parallel resistance"""
from .inverted_sums_widget import InvertedSumsForm


class ParallelResistanceForm(InvertedSumsForm):
    """Form to calculate parallel resistance"""

    measurement = "resistance"
    units = 'Ohms'
    default_prefix = 'kilo'
