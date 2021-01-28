"""Widget to calculate Frequency of RC filter circuits"""

import tkinter as tk
from tkinter import ttk
from math import pi

from .widgets import Numberbox
from .variables import PrefixNumberVar




class RCFrequencyForm(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(4, weight=1)
        self.resistance_val = PrefixNumberVar(self, value=0.0, prefix='kilo')
        self.capacitance_val = PrefixNumberVar(self, value=0.0, prefix='nano')
        self.frequency_val = PrefixNumberVar(self, value=0.0, prefix='')
        self.select_var = tk.StringVar(self)
        self.error_string = tk.StringVar(self, value='')

        self.select_var.trace_add('write', self._output_selected)

        instructions = (
            'Select the value to be entered in the right column, '
            '\nthen enter the other two values and hit "Calculate".'
        )
        ttk.Label(self, text=instructions).grid(
            row=0,
            sticky='ew',
            ipadx=10,
            ipady=10,
            columnspan=5
        )

        # Table header
        headerfont = 'Arial 10 bold'
        ttk.Label(self, text='Calculate', font=headerfont).grid(row=1, column=0, sticky='ew')
        ttk.Label(self, text='Value', font=headerfont).grid(row=1, column=2, sticky='ew')
        ttk.Label(self, text='Prefix', font=headerfont).grid(row=1, column=3, sticky='ew')
        ttk.Label(self, text='Units', font=headerfont).grid(row=1, column=4, sticky='ew')

        # track inputs for disabling
        self.inputs = dict()
        # Resistance
        self.input_row(2, 'R', 'Resistance', 'Ohms', self.resistance_val)

        # Capacitance
        self.input_row(3, 'C', 'Capacitance', 'Farads', self.capacitance_val)

        # Frequency
        self.input_row(4, 'F', 'Frequency', 'Hertz', self.frequency_val)

        # Error
        ttk.Label(self, textvariable=self.error_string).grid(row=10, sticky='ew', columnspan=5)

        # Submit
        ttk.Button(
            self,
            text='Calculate',
            command=self.try_calculation
        ).grid(row=99, column=4, sticky='w')

        self.select_var.set('F')

    def input_row(self, row, key, label, unit, value_var):
        """Create an input row"""
        if not isinstance(value_var, PrefixNumberVar):
            raise TypeError('value_var must be a PrefixNumberVar')
        # build the UI
        ttk.Radiobutton(
            self,
            text=label,
            value=key,
            variable=self.select_var
        ).grid(row=row, column=0, sticky='ew')
        self.inputs[key] = Numberbox(
            self,
            textvariable=value_var,
            from_=0,
            increment=.01
        )
        self.inputs[key].grid(row=row, column=2, sticky='ew')
        ttk.OptionMenu(
            self,
            value_var.prefix,
            value_var.prefix.get() , *list(value_var.prefixes.keys())
        ).grid(row=row, column=3, sticky='ew')
        ttk.Label(self, text=unit).grid(row=row, column=4, sticky='ew')


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
        """Reset the form to default"""

        self.resistance_val.set(0, 'kilo')
        self.capacitance_val.set(0, 'nano')
        self.frequency_val.set(0, '')

    def _output_selected(self, *_):

        selected = self.select_var.get()

        for key, inp in self.inputs.items():
            if key == selected:
                inp.configure(state='disabled')
            else:
                inp.configure(state='normal')


if __name__ == '__main__':
    root = tk.Tk()
    rcf = RCFrequencyForm(root)
    rcf.pack()
    root.mainloop()
