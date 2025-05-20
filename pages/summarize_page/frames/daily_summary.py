
from pages.summarize_page.base_summarize import BaseSummarizePage
import ttkbootstrap as ttk

class DailySummaryFrame(BaseSummarizePage):
    def __init__(self, parent, week_button=None):
        super().__init__(parent)
        self.labels = ["Total Daily Sales", "Total Daily Profit", "Best-Selling Product", "Total Items Sold"]

        self.create_labels_and_values(self.labels)

        self.set_frame_title("Daily Summarize")
        self.create_button(text="See Last Week Summary", cmd=week_button)
        self.configure_child_grid(True)




