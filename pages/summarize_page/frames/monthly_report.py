
from pages.summarize_page.base_summarize import BaseSummarizePage
from logic.summarize_logic.download_data import DownLoadData
from tkinter import ttk
import ttkbootstrap as ttk
import calendar


class MonthlyReportFrame(BaseSummarizePage):
    def __init__(self, parent, month_cmd):
        super().__init__(parent)
        self.month_var = ttk.StringVar()
        self.month_cmd = month_cmd
        self.download_state = None

        self.download_cmd = DownLoadData(month_var=self.month_var, root=self.parent)

        self.create_labels_and_values(["", "Month", "Total Sales", "Total Profit", "Best-Selling Product", "Total Items Sold"])
        self.set_frame_title("Monthly Report\n")
        self.create_button(text="Download Raw Data", cmd=self.download_cmd.run_to_save, state=self.download_state)
        self.configure_child_grid(True, )
        self.menu_button()

        self.vars["month"].set("")
        self.vars["best_selling_product"].set("")


    def menu_button(self):
        self.menu = ttk.Menubutton(self.frame, cursor="hand2", direction="left",
                              style="success.Outline", takefocus=False, text="Select a Month",)

        self.menu.grid(row=1, column=0, columnspan=2)
        menu_menu = ttk.Menu(self.menu, tearoff=0, cursor="hand2",)
        for i in range(1, 13):
            menu_menu.add_radiobutton(label=calendar.month_name[i],
                                      font=("calibri", 12, "bold"),
                                      variable=self.month_var,
                                      value=f"0{i}",
                                      command=self.month_cmd)

        self.menu["menu"] = menu_menu

    def get_selected_month(self):
        self.menu['text'] = calendar.month_name[int(self.month_var.get())]


