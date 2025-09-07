import tkinter

from app.tkinter_uix import Theme

theme = Theme()


class Screen(tkinter.Frame):
    def __init__(
        self, master, bg=theme.app_color["background"], *args, **kwargs
    ):
        tkinter.Frame.__init__(self, master, bg=bg, *args, **kwargs)

    def show(self):
        self.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    def hide(self):
        self.pack_forget()


class ScreenManager:
    def __init__(self):
        self.active_screen = ""
        self.screens = {}

    def add_screen(self, master, name, *args, **kwargs):
        screen_widget = Screen(master, *args, **kwargs)
        self.screens[name] = screen_widget

    def switch_screen(self, name):
        if name in self.screens and name != self.active_screen:
            if self.active_screen:
                self.screens[self.active_screen]["screen"].hide()
                self.screens[self.active_screen]["state"] = "hide"

                self.screens[name]["screen"].show()
                self.screens[name]["state"] = "show"
                self.active_screen = name
            else:
                self.screens[name]["screen"].show()
                self.screens[name]["state"] = "show"
                self.active_screen = name



