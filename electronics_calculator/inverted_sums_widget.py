"""A form to calculate inverted sums

Can be used for parallel resistance or series capacitance.
"""

import tkinter as tk
from tkinter import ttk
from .variables import PrefixNumberVar
from .widgets import Numberbox


class ValueEntryTable(tk.Frame):
    """Entry table for Values"""

    def __init__(self, *args, units='', default_prefix='', starting_rows=2, result_var=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = result_var or PrefixNumberVar(self)
        self.units = units
        self.default_prefix = default_prefix
        self.result.prefix.trace_add('write', self._calculate)

        self.value_vars = list()
        self.container = tk.Canvas(self, borderwidth=0, height=150)

        self.table = tk.Frame(self.container)
        self.container.create_window((0,0), window=self.table, anchor='nw', tag='self.table')
        self.scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL,
            command=self.container.yview
        )
        self.container.configure(yscrollcommand=self.scrollbar.set)
        # place widgets
        self.container.grid(row=0, column=0, sticky='EW')
        self.scrollbar.grid(row=0, column=1, sticky='NSE')
        self.columnconfigure(0, weight=1)
        self.table.bind('<Configure>', self._onTableConfigure)

        for _ in range(starting_rows):
            self._add_value_row()

        buttons = tk.Frame(self)
        buttons.grid(row=1, column=0, sticky='w')
        ttk.Button(buttons, text='More', command=self._add_value_row).pack(side='left', ipadx=5)

    def _onTableConfigure(self, event):
        # Update the scrollregion since the bounding box has changed
        self.container.configure(scrollregion=self.table.bbox('all'))

    def _add_value_row(self):
        """Add an input row for a value"""

        var = PrefixNumberVar(self, value=0.0, prefix=self.default_prefix)
        self.value_vars.append(var)

        next_row = self.table.grid_size()[1]
        ttk.Label(self.table, text=f'{next_row+1}.', anchor='w').grid(row=next_row, column=0)
        Numberbox(self.table, textvariable=var, from_=0, increment=.01).grid(row=next_row, column=1)
        ttk.OptionMenu(self.table, var.prefix, self.default_prefix, *list(PrefixNumberVar.prefixes.keys())).grid(row=next_row, column=2)
        ttk.Label(self.table, text=self.units).grid(row=next_row, column=3)

        var.trace_add('write', self._calculate)
        var.prefix.trace_add('write', self._calculate)

    def _calculate(self, *_):
        """Calculate the parallel resistance"""
        # Get the absolute values of each resistance > 0
        rvals = [
            rv.get_absolute()
            for rv in self.value_vars
            if rv.get_absolute() > 0
        ]

        # if no rvals, just set the result to 0
        if not rvals:
            self.result.set_absolute(0)
            return

        # Calculate:  1/R_total = (1/R1 + 1/R2 + 1/R3 ...)
        rtotal = 1 / sum([1/r for r in rvals])

        self.result.set_absolute(rtotal)


class InvertedSumsForm(tk.Frame):
    """Form to calculate parallel resistance"""

    measurement = 'Something'
    units = 'somethings'
    default_prefix = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        instructions = (
            f'Enter as many {self.measurement} values as needed, '
            '\nthey will be calculated as you add them.'
            f'\nHit "More" to add another {self.measurement} entry.  '
            f'\nValues of 0 will be ignored. '
        )
        ttk.Label(self, text=instructions).grid(row=0, column=0, sticky='ew', ipadx=10, ipady=10)

        self.result = PrefixNumberVar(self, value=0.0, prefix=self.default_prefix)
        self.numbertable = ValueEntryTable(
            self,
            units=self.units,
            default_prefix=self.default_prefix,
            starting_rows=3,
            result_var=self.result
        )
        self.numbertable.grid(row=1, column=0, sticky='NSEW')


        outputformat = tk.Frame(self, pady=20)
        outputformat.grid(row=3, sticky='ew')
        ttk.Label(outputformat, text='Answer: ').pack(side='left')
        Numberbox(outputformat, state='disabled', textvariable=self.result, width=20).pack(side='left')
        ttk.OptionMenu(outputformat, self.result.prefix, self.default_prefix, *list(PrefixNumberVar.prefixes.keys())).pack(side='left')
        ttk.Label(outputformat, text=self.units).pack(side='left')
