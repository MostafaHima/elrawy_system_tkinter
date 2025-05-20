from pages.summarize_page.base_summarize import BaseSummarizePage


class YearlySummaryFrame(BaseSummarizePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_labels_and_values(["Current Year", "Total Sales", "Total Profit", "Average Monthly Sales"])
        self.set_frame_title("Yearly Summary")

        self.configure_child_grid(button=False)

