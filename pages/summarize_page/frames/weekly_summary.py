
from pages.summarize_page.base_summarize import BaseSummarizePage
import ttkbootstrap as ttk

class WeeklySummaryFrame(BaseSummarizePage):
    def __init__(self, parent, today_summary=None):
        super().__init__(parent)
        self.labels = ["From Date", "Total Weekly Sales", "Total Weekly Profit", "Best-Selling Product", "Total Items Sold"]

        self.create_labels_and_values(self.labels)

        self.set_frame_title("Weekly Summarize")
        self.create_button(text="See Today Summary", cmd=today_summary)
        self.configure_child_grid(True)

