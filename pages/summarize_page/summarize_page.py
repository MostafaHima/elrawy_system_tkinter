from pages.summarize_page.frames.daily_summary import DailySummaryFrame
from pages.summarize_page.frames.monthly_report import MonthlyReportFrame
from pages.summarize_page.frames.monthly_summary import MonthlySummaryFrame
from pages.summarize_page.frames.yearly_summary import YearlySummaryFrame
from pages.summarize_page.frames.weekly_summary import WeeklySummaryFrame

from logic.summarize_logic.daily_summarize_logic import DailyLogic
from logic.summarize_logic.weekly_summarize_logic import weeklyLogic
from logic.summarize_logic.monthly_summarize_logic import MonthlyLogic
from logic.summarize_logic.yearly_summarize_logic import YearlyLogic
from logic.summarize_logic.monthly_report_logic import MonthlyReportLogic

import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

class SummarizePage(tk.Frame):
    def __init__(self, root, on_back):
        super().__init__(root)

        self.on_back = on_back

        self.grid_columnconfigure(index=(0, 1), weight=1, uniform="a")
        self.grid_rowconfigure(index=0, weight=1, uniform="a")
        self.grid_rowconfigure(index=(1, 2), weight=4, uniform="a")

        self.set_main_title()
        self._back_button(self.on_back)

        self.daily = DailySummaryFrame(self, self._switch_to_weekly_frame)
        self.weekly = WeeklySummaryFrame(self, self._switch_to_daiy_frame)
        self.monthly_report = MonthlyReportFrame(self, month_cmd=self._load_montly_report_summary)
        self.monthly = MonthlySummaryFrame(self)
        self.yearly = YearlySummaryFrame(self)

        self.daily.frame.grid(row=1, column=0, sticky="nswe", pady=20, padx=20)
        self.weekly.frame.grid(row=1, column=0, sticky="nswe", pady=20, padx=20)

        self.monthly_report.frame.grid(row=2, column=1, sticky="nswe", padx=20, pady=20)
        self.monthly.frame.grid(row=1, column=1, sticky="nswe", pady=20, padx=20)
        self.yearly.frame.grid(row=2, column=0, sticky="nswe", pady=20, padx=20)

        self.daily.frame.tkraise()

    def load_summarizes_data(self):
        self.daily.frame.tkraise()
        self._load_daily_summary()
        self._load_monthly_summary()
        self._load_yearly_summary()



    def _load_daily_summary(self):
        daily_vars = self.daily.vars
        DailyLogic(daily_vars)

    def _load_monthly_summary(self):
        montly_vars = self.monthly.vars
        MonthlyLogic(montly_vars)

    def _load_yearly_summary(self):
        yearly_vars = self.yearly.vars
        YearlyLogic(yearly_vars)

    def _load_montly_report_summary(self):
        self.monthly_report.get_selected_month()

        report_vars = self.monthly_report.vars
        month_var = self.monthly_report.month_var

        MonthlyReportLogic(report_vars, month_var)

    def _load_weekly_summary(self):
        weekly_vars = self.weekly.vars
        weeklyLogic(weekly_vars)



    def _switch_to_weekly_frame(self):
        self.weekly.frame.tkraise()
        self._load_weekly_summary()

    def _switch_to_daiy_frame(self):
        self.daily.frame.tkraise()





    def set_main_title(self):
            title = ttk.Label(self, text="Summarzie Page", style="warning", font=("cailbri", 24, 'bold'))
            title.grid(row=0, column=0, columnspan=2)

    def _back_button(self, command=None):
        """
        Places a back button with an icon to navigate back.
        """
        icon_path = r"E:\Tkinter Projects\Elrawy_bookstore\assets\back_icon.png"  # الأفضل جعله نسبي
        icon = Image.open(icon_path)
        resized_icon = icon.resize((50, 50), Image.Resampling.LANCZOS)
        back_image = ImageTk.PhotoImage(resized_icon)

        back_btn = ttk.Button(
            self,
            image=back_image,
            command=command,
            style="darkly.Outline",
            cursor="hand2"
        )
        back_btn.image = back_image  # prevent garbage collection
        back_btn.grid(row=0, column=0, padx=15, sticky="w")