from PIL import Image, ImageTk
import tkinter as tk

class Icons:
    def __init__(self, icons_path):
        icon_size = (30, 30)
        self.upload_icon = ImageTk.PhotoImage(Image.open(icons_path + 'cloud-upload.png').resize(icon_size, Image.LANCZOS))
        self.detect_icon = ImageTk.PhotoImage(Image.open(icons_path + 'object.png').resize(icon_size, Image.LANCZOS))
        self.save_icon = ImageTk.PhotoImage(Image.open(icons_path + 'folder-download.png').resize(icon_size, Image.LANCZOS))
        self.map_icon = ImageTk.PhotoImage(Image.open(icons_path + 'map.png').resize(icon_size, Image.LANCZOS))
        self.play_icon = ImageTk.PhotoImage(Image.open(icons_path + 'play.png').resize(icon_size, Image.LANCZOS))
        self.pause_icon = ImageTk.PhotoImage(Image.open(icons_path + 'pause.png').resize(icon_size, Image.LANCZOS))
        self.stop_icon = ImageTk.PhotoImage(Image.open(icons_path + 'stop.png').resize(icon_size, Image.LANCZOS))
        self.clear_icon = ImageTk.PhotoImage(Image.open(icons_path + 'clear.png').resize(icon_size, Image.LANCZOS))

    def create_buttons(self, frame, commands, theme):
        select_button = tk.Button(frame, text="Select Image/Video", image=self.upload_icon, compound="top", command=commands['select'], font=theme.button_font, bg=theme.button_color, fg=theme.button_text_color)
        detect_button = tk.Button(frame, text="Detect Mangoes", image=self.detect_icon, compound="top", command=commands['detect'], font=theme.button_font, bg=theme.button_color, fg=theme.button_text_color, state=tk.DISABLED)
        play_button = tk.Button(frame, text="Play", image=self.play_icon, compound="top", command=commands['play'], font=theme.button_font, bg=theme.button_color, fg=theme.button_text_color, state=tk.DISABLED)
        pause_button = tk.Button(frame, text="Pause", image=self.pause_icon, compound="top", command=commands['pause'], font=theme.button_font, bg=theme.button_color, fg=theme.button_text_color, state=tk.DISABLED)
        stop_button = tk.Button(frame, text="Stop", image=self.stop_icon, compound="top", command=commands['stop'], font=theme.button_font, bg=theme.button_color, fg=theme.button_text_color, state=tk.DISABLED)
        save_button = tk.Button(frame, text="Save Results", image=self.save_icon, compound="top", command=commands['save'], font=theme.button_font, bg=theme.button_color, fg=theme.button_text_color, state=tk.DISABLED)
        clear_button = tk.Button(frame, text="Clear", image=self.clear_icon, compound="top", command=commands['clear'], font=theme.button_font, bg="red", fg=theme.button_text_color)
        
        return select_button, detect_button,play_button,stop_button,pause_button, save_button, clear_button
