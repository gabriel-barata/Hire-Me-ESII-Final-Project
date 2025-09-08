from tkinter import Label as _Label

from app.tkinter_uix import Theme

theme = Theme()


class Label(_Label):
    def __init__(self, master, *args, **kwargs):
        _Label.__init__(
            self,
            master,
            font=("Verdana", 12),
            bg=theme.app_color["background"],
            fg=theme.app_color["foreground"],
            *args,
            **kwargs,
        )
