"""Form to calculate series capacitance"""

from .inverted_sums_widget import InvertedSumsForm

class SeriesCapacitanceForm(InvertedSumsForm):
    measurement = 'capacitance'
    units = 'Farads'
    default_prefix = 'nano'
