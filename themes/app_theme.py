
from ttkbootstrap import Style
class AppTheme:
    def __init__(self):
        self.custom_app_themes()


    def custom_app_themes(self):
        style = Style()
        style.configure("info.Outline.TButton", font="Calibri 12 bold")
        style.configure("warning.Outline.TButton", font="Calibri 12 bold")