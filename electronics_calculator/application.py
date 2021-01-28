"""Main window and application object definition"""
import tkinter as tk
from tkinter import ttk
from tkinter import font

from .rc_frequency_form import RCFrequencyForm
from .parallel_resistance import ParallelResistanceForm
from .series_capacitance import SeriesCapacitanceForm


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #####################
        # Mainwindow config #
        #####################
        self.title('Electronics Calculator')
        self.geometry('640x480')
        self.configure(bd=20)

        ###############
        # Style fixes #
        ###############
        self.style = ttk.Style()
        # use 'alt' theme

        self.style.theme_use('alt')

        # bigger font
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(
            family='Arial',
            size=12,
        )

        # Don't grey disabled text, it's too hard to read
        self.style.map(
            'TSpinbox',
            foreground=[('disabled', 'black')]
        )

        ###############
        # Main Layout #
        ###############
        ttk.Label(
            self,
            text='Electronics Calculator',
            font='Arial 16 bold',
            anchor='center'
        ).pack(anchor='center', fill='x', pady=(0, 10))
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=True, fill='both')

        #enable keyboard nav of tabs
        self.tabs.enable_traversal()

        # Add calculators
        rc = RCFrequencyForm(self.tabs)
        self.tabs.add(rc, text='RC frequency calculator', padding=10)

        pr = ParallelResistanceForm(self.tabs)
        self.tabs.add(pr, text='Parallel Resistance', padding=10)

        sc = SeriesCapacitanceForm(self.tabs)
        self.tabs.add(sc, text='Series Capacitance', padding=10)
