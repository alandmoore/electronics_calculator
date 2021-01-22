import tkinter as tk
from tkinter import ttk
from math import pi

from widgets import Numberbox


class PrefixNumberVar(tk.DoubleVar):
    """A number unit that can have an ISO prefix """

    prefixes = {
        'pico': 10 ** -12,
        'nano': 10 ** -9,
        'micro': 10 ** -6,
        'milli': 10 ** -3,
        '': 1,
        'kilo': 10 ** 3,
        'mega': 10 ** 6,
        'giga': 10 ** 9
    }

    def __init__(self, parent, *args, prefix='', **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.prefix = tk.StringVar(parent, value=prefix)

    def set(self, value, prefix=None, *args, **kwargs):
        if prefix is None:
            pass
        elif prefix not in self.prefixes:
            raise ValueError(f'Invalid Prefix: {prefix}')
        else:
            self.prefix.set(prefix)

        super().set(value, *args, **kwargs)

    def get_absolute(self):

        return self.get() * self.prefixes[self.prefix.get()]

    def set_absolute(self, value):
        """Set an absolute value with no prefix"""

        divisor = self.prefixes[self.prefix.get()]
        self.set(value / divisor)


class InputRow(tk.Frame):


    def __init__(self, parent, key, label, unit, value_var, select_var, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.key = key
        self.label = label
        self.unit = unit
        if not isinstance(value_var, PrefixNumberVar):
            raise TypeError('value_var must be a PrefixNumberVar')
        self.value_var = value_var
        self.select_var = select_var

        # build the UI
        ttk.Radiobutton(self, text='Select', value=self.key, variable=select_var).grid(row=0, column=0)
        ttk.Label(self, text=self.label).grid(row=0, column=1)
        Numberbox(self, textvariable=self.value_var, from_=0, increment=.01).grid(row=0, column=2)
        ttk.OptionMenu(self, self.value_var.prefix, self.value_var.prefix.get() , *list(value_var.prefixes.keys())).grid(row=0, column=3)
        ttk.Label(self, text=unit).grid(row=0, column=4)



class RCFrequencyForm(tk.Frame):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resistance_val = PrefixNumberVar(self, value=0.0, prefix='kilo')
        self.capacitance_val = PrefixNumberVar(self, value=0.0, prefix='nano')
        self.frequency_val = PrefixNumberVar(self, value=0.0, prefix='')
        self.select_var = tk.StringVar(self, value='F')
        self.error_string = tk.StringVar(self, value='')

        ttk.Label(self, text='RC Frequency Calculator').grid(row=0, column=0, columnspan=4)

        # Resistance
        InputRow(self, 'R', 'Resistance', 'Ohms', self.resistance_val, self.select_var).grid(row=1, column=0)

        # Capacitance
        InputRow(self, 'C', 'Capacitance', 'Farads', self.capacitance_val, self.select_var).grid(row=2, column=0)


        # Frequency
        InputRow(self, 'F', 'Frequency', 'Hertz', self.frequency_val, self.select_var).grid(row=3, column=0)

        # Error
        ttk.Label(self, textvariable=self.error_string).grid(row=10, column=0, columnspan=4)

        # Submit

        ttk.Button(self, text='Calculate', command=self.try_calculation).grid(row=99, column=0)


    def try_calculation(self):
        """Attempt to calculate the missing value"""

        self.error_string.set('')


        vals = {
            'R': self.resistance_val,
            'C': self.capacitance_val,
            'F': self.frequency_val
        }

        to_calculate = self.select_var.get()
        print(to_calculate)

        populated_vals = [var.get_absolute()  for key, var in vals.items() if key != to_calculate]
        try:
            calculated_value = (1 / (2 * pi * populated_vals[0] * populated_vals[1]))
        except ZeroDivisionError:
            self.error_string.set('Error: Values used for calculation cannot be zero.')
            return

        #calculated_value = round(calculated_value * 100) / 100
        vals[to_calculate].set_absolute(calculated_value)


    def reset(self):

        self.resistance_val.set(0, 'kilo')
        self.capacitance_val.set(0, 'nano')
        self.frequency_val.set(0, '')


if __name__ == '__main__':
    root = tk.Tk()
    rcf = RCFrequencyForm(root)
    rcf.pack()
    root.mainloop()
