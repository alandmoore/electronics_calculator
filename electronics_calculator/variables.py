"""Custom Variable classes"""
import tkinter as tk


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

    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except tk.TclError as e:

            if str(e) == "expected floating-point number but got \"\"":
                return 0
            raise e

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
