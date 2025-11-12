import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

def show_splash_screen(root):
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    
    # Load the GIF file
    gif_path = "F:\\Mango Fruit Detection project\\GUI\\icons\\mango.gif"
    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif)]
    
    # Get the dimensions of the GIF
    gif_width, gif_height = gif.size
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    
    # Center the window
    x = (screen_width // 2) - (gif_width // 2)
    y = (screen_height // 2) - (gif_height // 2)
    splash.geometry(f"{gif_width}x{gif_height}+{x}+{y}")
    
    splash_label = tk.Label(splash, bg="#333333")
    splash_label.pack(expand=True)

    def update_frame(index):
        frame = frames[index]
        index += 1
        if index == len(frames):
            index = 0
        splash_label.config(image=frame)
        splash.after(50, update_frame, index)

    root.withdraw()
    splash.after(0, update_frame, 0)
    splash.after(3000, lambda: root.deiconify())
    splash.after(3000, splash.destroy)

    return splash
