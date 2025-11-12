class Theme:
    def __init__(self):
        self.bg_color = "#f0f0f0"  # Background color
        self.button_color = "#4CAF50"
        self.button_text_color = "#ffffff"
        self.frame_bg_color = "#ffffff"
        self.title_font = ("Helvetica", 18, "bold")
        self.subtitle_font = ("Helvetica", 14)
        self.label_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 10)
        self.entry_font = ("Helvetica", 10)
        self.credit_text_color = "black"

    def apply_theme(self, root):
        root.configure(bg=self.bg_color)
