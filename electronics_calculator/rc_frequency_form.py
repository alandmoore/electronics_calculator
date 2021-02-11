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
        self.vars = dict()
        self.vars['R'] = PrefixNumberVar(self, value=0.0, prefix='kilo')
        self.vars['C'] = PrefixNumberVar(self, value=0.0, prefix='nano')
        self.vars['F'] = PrefixNumberVar(self, value=0.0, prefix='')
        self.select_var = tk.StringVar(self)
        self.error_string = tk.StringVar(self, value='')

        self.select_var.trace_add('write', self._output_selected)

        instructions = (
            'Select the value to be entered in the right column, '
            '\nthen enter the other two values.'
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
        self.input_row(2, 'R', 'Resistance', 'Ohms')

        # Capacitance
        self.input_row(3, 'C', 'Capacitance', 'Farads')

        # Frequency
        self.input_row(4, 'F', 'Frequency', 'Hertz')

        # Error
        ttk.Label(self, textvariable=self.error_string).grid(row=10, sticky='ew', columnspan=5)

        # set traces:
        for var in self.vars.values():
            var.trace_add('write', self._try_calculation)
            var.prefix.trace_add('write', self._try_calculation)
        self.select_var.trace_add('write', self._try_calculation)

        # Set default.  Doing this here so triggers can happen
        self.select_var.set('F')

    def input_row(self, row, key, label, unit):
        """Create an input row"""

        # build the UI
        ttk.Radiobutton(
            self,
            text=label,
            value=key,
            variable=self.select_var
        ).grid(row=row, column=0, sticky='ew')
        self.inputs[key] = Numberbox(
            self,
            textvariable=self.vars[key],
            from_=0,
            increment=.01
        )
        self.inputs[key].grid(row=row, column=2, sticky='ew')
        ttk.OptionMenu(
            self,
            self.vars[key].prefix,
            self.vars[key].prefix.get() , *list(self.vars[key].prefixes.keys())
        ).grid(row=row, column=3, sticky='ew')
        ttk.Label(self, text=unit).grid(row=row, column=4, sticky='ew')


    def _try_calculation(self, *_):
        """Attempt to calculate the missing value"""

        to_calculate = self.select_var.get()
        populated_vals = [var.get_absolute()  for key, var in self.vars.items() if key != to_calculate]
        try:
            calculated_value = (1 / (2 * pi * populated_vals[0] * populated_vals[1]))
        except ZeroDivisionError:
            # one of the values is zero, so just set the answer 0
            self.vars[to_calculate].set_absolute(0)
            return

        #calculated_value = round(calculated_value * 100) / 100
        self.vars[to_calculate].set_absolute(calculated_value)


    def _reset(self):
        """Reset the form to default"""

        self.vars['R'].set(0, 'kilo')
        self.vars['C'].set(0, 'nano')
        self.vars['F'].set(0, '')

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
