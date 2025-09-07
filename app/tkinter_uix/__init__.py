import yaml
from app.utils.variables import APP_FOLDER

THEMES_FOLDER = APP_FOLDER / "tkinter_uix/themes"


class Theme:
    def __init__(self, name="default"):
        with open(
            str(THEMES_FOLDER / f"{name}.yaml"), "r", encoding="UTF-8"
        ) as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
            
        self.app_color = self.data["App"]
        self.btn_color = self.data["Button"]
        self.entry_color = self.data["Entry"]
        self.navbar_color = self.data["Navbar"]