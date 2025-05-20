from datetime import datetime
from pages.summarize_page.base_summarize import BaseSummarizePage
import ttkbootstrap as ttk

class MonthlySummaryFrame(BaseSummarizePage):
    def __init__(self, parent):
        super().__init__(parent)

        self.labels = [f"Month Date", "Total Monthly Sales", "Total Monthly Profit",
                       "Best-Selling Product", "Month-over-Month Change"]


        self.create_labels_and_values(self.labels)
        self.set_frame_title(f"Monthly Summary")
        self.configure_child_grid(button=False)


