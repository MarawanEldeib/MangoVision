import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
import os

# Importing your custom modules
from translations import translations
from splash_screen import show_splash_screen
from toolbar import create_menu
from themes import Theme
from icons_buttons import Icons
from map_view import display_map_in_app
from video_utils import (
    select_video_file, process_selected_video, display_video_frame,
    detect_mangoes_in_video, save_annotated_video, play_video,
    pause_video, stop_video, play_next_frame
)
from image_utils import process_selected_image, display_image, annotate_image, detect_mangoes_in_image, save_annotated_image
from ultralytics import YOLO  

class MangoVisionApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "en"
        self.model1 = self.load_model(r'F:\Mango Fruit Detection project\GUI\models\CQUniversity_dataset_sgd_aug\best.pt')
        self.model2 = self.load_model(r'F:\Mango Fruit Detection project\GUI\models\100_epochs_local_dataset\best.pt')
        self.current_model = self.model1
        self.confidence_threshold = 0.5
        self.summary = []
        self.current_gps_info = None
        self.is_video = False
        self.video_frames = []
        self.video_playing = False
        self.video_cap = None
        self.frame_interval = 2  # seconds
        
         # Add image_path to track the selected image path
        self.image_path = None

        # Theme and Icons
        self.theme = Theme()
        self.icons = Icons('F:\\Mango Fruit Detection project\\GUI\\icons\\')

        # Splash Screen
        show_splash_screen(self.root)

        # Initialize UI
        self.initialize_ui()

    def load_model(self, model_path):
        """Load the YOLO model from the specified path."""
        return YOLO(model_path)

    def get_text(self, key):
        """Get the translated text for the given key."""
        return translations[self.current_lang][key]

    def switch_language(self, lang):
        """Switch the application language."""
        self.current_lang = lang
        self.update_text()
        if self.summary:
            self.display_summary(self.summary)

    def update_text(self):
        """Update all text in the UI to match the current language."""
        self.root.title(self.get_text("title"))
        self.title_label.config(text=self.get_text("title"))
        self.subtitle_label.config(text=self.get_text("subtitle"))
        self.select_button.config(text=self.get_text("select_media"))
        self.detect_button.config(text=self.get_text("detect_mangoes"))
        self.save_button.config(text=self.get_text("save_results"))
        self.view_map_button.config(text=self.get_text("view_on_map"))
        self.clear_button.config(text=self.get_text("clear"))
        self.date_label_lbl.config(text=self.get_text("date"))
        self.time_label_lbl.config(text=self.get_text("time"))
        self.latitude_label.config(text=self.get_text("latitude"))
        self.longitude_label.config(text=self.get_text("longitude"))
        self.status_var.set(self.get_text("ready"))
        self.credit_label.config(text=self.get_text("created_by"), fg=self.theme.credit_text_color)
        self.model_menu.entryconfig(0, label=self.get_text("model_1"))
        self.model_menu.entryconfig(1, label=self.get_text("model_2"))
        self.threshold_menu.entryconfig(0, label=self.get_text("confidence_threshold"))
        self.image_frame.config(text=self.get_text("selected_media"))
        self.gps_frame.config(text=self.get_text("gps_coordinates"))
        self.datetime_frame.config(text=self.get_text("date_time"))
        self.summary_frame.config(text=self.get_text("detection_summary"))

    def initialize_ui(self):
        """Initialize the main UI components."""
        self.root.title(self.get_text("title"))
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        self.root.iconphoto(True, tk.PhotoImage(file='F:\\Final_year_project\\yolov8-env\\my_yolov8_app\\icons\\mango.png'))

        self.theme.apply_theme(self.root)

        # Create a main container
        self.main_container = tk.Frame(self.root, bg=self.theme.bg_color)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar
        self.v_scrollbar = ttk.Scrollbar(self.main_container, orient=tk.VERTICAL)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a canvas
        self.canvas = tk.Canvas(self.main_container, bg=self.theme.bg_color, yscrollcommand=self.v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure scrollbar
        self.v_scrollbar.config(command=self.canvas.yview)

        # Create a frame inside the canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.theme.bg_color)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        # Add the new frame to a window in the canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        create_menu(self)
        self.create_status_bar()
        self.create_main_layout()

    def create_status_bar(self):
        """Create the status bar at the bottom of the window."""
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.scrollable_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg=self.theme.bg_color)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set(self.get_text("ready"))

        self.credit_label = tk.Label(self.scrollable_frame, text=self.get_text("created_by"), font=("Helvetica", 10), bg=self.theme.bg_color, fg=self.theme.credit_text_color)
        self.credit_label.pack(side=tk.BOTTOM, pady=5)

    def create_main_layout(self):
        """Create the main layout with top and main frames."""
        self.top_frame = tk.Frame(self.scrollable_frame, bg=self.theme.bg_color, padx=10, pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.main_frame = tk.Frame(self.scrollable_frame, bg=self.theme.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.top_frame, text=self.get_text("title"), font=self.theme.title_font, bg=self.theme.bg_color)
        self.title_label.pack(side=tk.TOP, pady=5)

        self.subtitle_label = tk.Label(self.top_frame, text=self.get_text("subtitle"), font=self.theme.subtitle_font, bg=self.theme.bg_color)
        self.subtitle_label.pack(side=tk.TOP, pady=5)

        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        """Create the left frame containing image and control buttons."""
        self.left_frame = tk.Frame(self.main_frame, bg=self.theme.bg_color)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.image_frame = tk.LabelFrame(self.left_frame, text=self.get_text("selected_media"), padx=10, pady=10, bg=self.theme.frame_bg_color, font=self.theme.label_font, bd=2, relief=tk.GROOVE)
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.gps_frame = tk.LabelFrame(self.left_frame, text=self.get_text("gps_coordinates"), padx=10, pady=10, bg=self.theme.frame_bg_color, font=self.theme.label_font, bd=2, relief=tk.GROOVE)
        self.gps_frame.pack(fill=tk.X, pady=5, padx=10)

        self.latitude_label = tk.Label(self.gps_frame, text=self.get_text("latitude"), font=self.theme.label_font, bg=self.theme.frame_bg_color)
        self.latitude_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.latitude_entry = tk.Entry(self.gps_frame, font=self.theme.entry_font, state='readonly', width=20)
        self.latitude_entry.grid(row=0, column=1, padx=5, pady=5)

        self.longitude_label = tk.Label(self.gps_frame, text=self.get_text("longitude"), font=self.theme.label_font, bg=self.theme.frame_bg_color)
        self.longitude_label.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.longitude_entry = tk.Entry(self.gps_frame, font=self.theme.entry_font, state='readonly', width=20)
        self.longitude_entry.grid(row=0, column=3, padx=5, pady=5)

        self.view_map_button = tk.Button(self.gps_frame, text=self.get_text("view_on_map"), image=self.icons.map_icon, compound="top", command=self.view_on_map, font=self.theme.button_font, bg=self.theme.button_color, fg=self.theme.button_text_color, state=tk.DISABLED)
        self.view_map_button.grid(row=0, column=4, padx=5, pady=5, rowspan=2)

        self.datetime_frame = tk.LabelFrame(self.left_frame, text=self.get_text("date_time"), padx=10, pady=10, bg=self.theme.frame_bg_color, font=self.theme.label_font, bd=2, relief=tk.GROOVE)
        self.datetime_frame.pack(fill=tk.X, pady=5, padx=10)

        self.date_label_lbl = tk.Label(self.datetime_frame, text=self.get_text("date"), font=self.theme.label_font, bg=self.theme.frame_bg_color)
        self.date_label_lbl.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_label = tk.Entry(self.datetime_frame, font=self.theme.entry_font, state='readonly', width=20)
        self.date_label.grid(row=0, column=1, padx=5, pady=5)

        self.time_label_lbl = tk.Label(self.datetime_frame, text=self.get_text("time"), font=self.theme.label_font, bg=self.theme.frame_bg_color)
        self.time_label_lbl.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.time_label = tk.Entry(self.datetime_frame, font=self.theme.entry_font, state='readonly', width=20)
        self.time_label.grid(row=0, column=3, padx=5, pady=5)

        self.button_frame = tk.Frame(self.left_frame, bg=self.theme.bg_color)
        self.button_frame.pack(fill=tk.X, pady=5)

        self.create_placeholder_image()

        self.image_label = tk.Label(self.image_frame, bg=self.theme.frame_bg_color, image=self.placeholder_image)
        self.image_label.pack(padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(self.image_frame, orient=tk.HORIZONTAL, length=640, mode='determinate')
        self.progress_bar.pack(side=tk.BOTTOM, padx=5, pady=5)

        self.create_buttons()

    def create_placeholder_image(self):
        """Create a placeholder image with the text 'No Preview Available'."""
        self.placeholder_image = Image.new('RGB', (640, 360), color=(192, 192, 192))
        draw = ImageDraw.Draw(self.placeholder_image)
        font = ImageFont.load_default()  # Use default PIL font
        text = "No Preview Available"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        textwidth = text_bbox[2] - text_bbox[0]
        textheight = text_bbox[3] - text_bbox[1]
        width, height = self.placeholder_image.size
        x = (width - textwidth) / 2
        y = (height - textheight) / 2
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        self.placeholder_image = ImageTk.PhotoImage(self.placeholder_image)

    def create_buttons(self):
        """Create and place the control buttons."""
        commands = {
            'select': self.select_media,
            'detect': self.process_image_for_mango_detection,
            'save': self.save_detection_results,
            'play': self.play_video,
            'pause': self.pause_video,
            'stop': self.stop_video,
            'clear': self.clear_data,
        }

        self.select_button = tk.Button(self.button_frame, text=self.get_text("select_media"), image=self.icons.upload_icon, compound="top", command=commands['select'], font=self.theme.button_font, bg=self.theme.button_color, fg=self.theme.button_text_color)
        self.detect_button = tk.Button(self.button_frame, text=self.get_text("detect_mangoes"), image=self.icons.detect_icon, compound="top", command=commands['detect'], font=self.theme.button_font, bg=self.theme.button_color, fg=self.theme.button_text_color, state=tk.DISABLED)
        self.save_button = tk.Button(self.button_frame, text=self.get_text("save_results"), image=self.icons.save_icon, compound="top", command=commands['save'], font=self.theme.button_font, bg=self.theme.button_color, fg=self.theme.button_text_color, state=tk.DISABLED)
        self.clear_button = tk.Button(self.button_frame, text=self.get_text("clear"), image=self.icons.clear_icon, compound="top", command=commands['clear'], font=self.theme.button_font, bg="red", fg=self.theme.button_text_color)

        self.select_button.grid(row=0, column=0, padx=5, pady=5)
        self.detect_button.grid(row=0, column=1, padx=5, pady=5)
        self.save_button.grid(row=0, column=2, padx=5, pady=5)
        self.clear_button.grid(row=0, column=3, padx=5, pady=5)

        # Create video control buttons but initially hide them
        self.video_controls_frame = tk.Frame(self.image_frame, bg=self.theme.frame_bg_color)
        self.video_controls_frame.pack(fill=tk.X, padx=5, pady=5)

        self.play_button = tk.Button(self.video_controls_frame, text=self.get_text("play_video"), image=self.icons.play_icon, compound="left", command=commands['play'], font=self.theme.button_font, bg=self.theme.button_color, fg=self.theme.button_text_color, state=tk.DISABLED)
        self.pause_button = tk.Button(self.video_controls_frame, text=self.get_text("pause_video"), image=self.icons.pause_icon, compound="left", command=commands['pause'], font=self.theme.button_font, bg=self.theme.button_color, fg=self.theme.button_text_color, state=tk.DISABLED)
        self.stop_button = tk.Button(self.video_controls_frame, text=self.get_text("stop_video"), image=self.icons.stop_icon, compound="left", command=commands['stop'], font=self.theme.button_font, bg=self.theme.button_color, fg=self.theme.button_text_color, state=tk.DISABLED)

        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Hide the video control buttons initially
        self.video_controls_frame.pack_forget()

    def create_right_frame(self):
        """Create the right frame containing the detection summary."""
        self.right_frame = tk.Frame(self.main_frame, bg=self.theme.bg_color)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.summary_frame = tk.LabelFrame(self.right_frame, text=self.get_text("detection_summary"), padx=10, pady=10, bg=self.theme.frame_bg_color, font=self.theme.label_font, bd=2, relief=tk.GROOVE)
        self.summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.summary_canvas = tk.Canvas(self.summary_frame, bg=self.theme.frame_bg_color)
        self.summary_scrollbar = ttk.Scrollbar(self.summary_frame, orient="vertical", command=self.summary_canvas.yview)
        self.summary_inner_frame = tk.Frame(self.summary_canvas, bg=self.theme.frame_bg_color)

        self.summary_inner_frame.bind(
            "<Configure>",
            lambda e: self.summary_canvas.configure(
                scrollregion=self.summary_canvas.bbox("all")
            )
        )

        self.summary_canvas.create_window((0, 0), window=self.summary_inner_frame, anchor="nw")
        self.summary_canvas.configure(yscrollcommand=self.summary_scrollbar.set)

        self.summary_canvas.pack(side="left", fill="both", expand=True)
        self.summary_scrollbar.pack(side="right", fill="y")

    def select_media(self):
        """Open a file dialog to select an image or video file."""
        file_path = filedialog.askopenfilename(filetypes=[("Media files", "*.jpg;*.jpeg;*.png;*.mp4;*.avi")])
        if file_path:
            if file_path.lower().endswith(('.mp4', '.avi')):
                self.status_var.set(self.get_text("loading_video"))
                process_selected_video(self, file_path)
            else:
                self.status_var.set(self.get_text("loading_image"))
                process_selected_image(self, file_path)

    def process_image_for_mango_detection(self):
        """Process the selected image or video for mango detection."""
        self.status_var.set(self.get_text("detecting_mangoes"))
        start_time = time.time()
        if self.is_video:
            detect_mangoes_in_video(self)
        else:
            detect_mangoes_in_image(self)
        end_time = time.time()
        detection_time = end_time - start_time
        self.status_var.set(f"{self.get_text('detection_complete')} {self.get_text('detection_time')}{detection_time:.2f} seconds")

    def display_summary(self, summary):
        self.clear_summary()
        if summary:
            if self.is_video:
                summary_text = f"Total Mangoes Detected: {len(summary)}"
                tk.Label(self.summary_inner_frame, text=summary_text, font=self.theme.label_font, bg=self.theme.frame_bg_color, fg="black").pack(anchor='w')
            else:
                for item in summary:
                    summary_text = f"Mango {item['Mango No.']}: {item['Confidence Score']}"
                    tk.Label(self.summary_inner_frame, text=summary_text, font=self.theme.label_font, bg=self.theme.frame_bg_color, fg="black").pack(anchor='w')
                summary_text = f"Total Mangoes Detected: {len(summary)}"
                tk.Label(self.summary_inner_frame, text=summary_text, font=self.theme.label_font, bg=self.theme.frame_bg_color, fg="black").pack(anchor='w')
        else:
            tk.Label(self.summary_inner_frame, text=self.get_text("no_mangoes_detected"), font=self.theme.label_font, bg=self.theme.frame_bg_color, fg="black").pack(anchor='w')

    def save_detection_results(self):
        """Save the detection results."""
        try:
            if self.is_video:
                save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("AVI files", "*.avi")])
                if save_path:
                    save_annotated_video(self, save_path)
            else:
                save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
                if save_path:
                    save_annotated_image(self, save_path)
            if save_path:
                messagebox.showinfo(self.get_text("save_successful"), f"{self.get_text('results_saved_to')} {save_path}")
                self.status_var.set(self.get_text("results_saved"))
        except Exception as e:
            messagebox.showerror(self.get_text("error"), str(e))

    def view_on_map(self):
        """View the detected GPS coordinates on a map."""
        try:
            if self.current_gps_info:
                lat = self.current_gps_info['Latitude']
                lon = self.current_gps_info['Longitude']
                display_map_in_app(self.root, lat, lon)
        except Exception as e:
            messagebox.showerror(self.get_text("error"), str(e))

    def clear_data(self):
        self.image_label.config(image=self.placeholder_image)
        self.image_label.image = self.placeholder_image
        self.clear_exif_data()
        self.detect_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.clear_summary()
        self.status_var.set(self.get_text("data_cleared"))
        self.video_controls_frame.pack_forget()  # Hide video controls


    def clear_exif_data(self):
        """Clear EXIF data displayed in the UI."""
        self.latitude_entry.config(state=tk.NORMAL)
        self.latitude_entry.delete(0, tk.END)
        self.longitude_entry.config(state=tk.NORMAL)
        self.longitude_entry.delete(0, tk.END)
        self.date_label.config(state=tk.NORMAL)
        self.date_label.delete(0, tk.END)
        self.time_label.config(state=tk.NORMAL)
        self.time_label.delete(0, tk.END)

        self.latitude_entry.insert(0, "No Data")
        self.longitude_entry.insert(0, "No Data")
        self.date_label.insert(0, "No Data")
        self.time_label.insert(0, "No Data")

        self.latitude_entry.config(state='readonly')
        self.longitude_entry.config(state='readonly')
        self.date_label.config(state='readonly')
        self.time_label.config(state='readonly')

        self.view_map_button.config(state=tk.DISABLED)

    def clear_summary(self):
        """Clear the detection summary displayed in the UI."""
        for widget in self.summary_inner_frame.winfo_children():
            widget.destroy()

    # GUI.py
    def display_exif_data(self, exif_data):
        """Display EXIF data in the UI."""
        self.latitude_entry.config(state=tk.NORMAL)
        self.latitude_entry.delete(0, tk.END)
        self.longitude_entry.config(state=tk.NORMAL)
        self.longitude_entry.delete(0, tk.END)
        self.date_label.config(state=tk.NORMAL)
        self.date_label.delete(0, tk.END)
        self.time_label.config(state=tk.NORMAL)
        self.time_label.delete(0, tk.END)

        date, time = "No Data", "No Data"
        if exif_data['Date and Time']:
            date_time = exif_data['Date and Time'].values
            if date_time:
                date, time = date_time.split()
        self.date_label.insert(0, date)
        self.time_label.insert(0, time)
        self.date_label.config(state='readonly')
        self.time_label.config(state='readonly')

        self.current_gps_info = None
        if exif_data and exif_data["GPS Info"]:
            gps_info = exif_data["GPS Info"]
            self.latitude_entry.insert(0, gps_info['Latitude'])
            self.longitude_entry.insert(0, gps_info['Longitude'])
            self.current_gps_info = gps_info
            self.view_map_button.config(state=tk.NORMAL)
        else:
            self.latitude_entry.insert(0, "No Data")
            self.longitude_entry.insert(0, "No Data")
            self.view_map_button.config(state=tk.DISABLED)
        self.latitude_entry.config(state='readonly')
        self.longitude_entry.config(state='readonly')


    def play_video(self):
        """Play the video."""
        play_video(self)

    def pause_video(self):
        """Pause the video playback."""
        pause_video(self)

    def stop_video(self):
        """Stop the video playback and reset to the first frame."""
        stop_video(self)

    def play_next_frame(self):
        """Play the next frame in the video."""
        play_next_frame(self)

    def display_video_frame(self, frame_idx):
        """Display a specific frame of the video."""
        display_video_frame(self, frame_idx)

    def switch_model(self, model_number):
        """Switch the detection model."""
        if model_number == 1:
            self.current_model = self.model1
            self.status_var.set(self.get_text("model_1_selected"))
        else:
            self.current_model = self.model2
            self.status_var.set(self.get_text("model_2_selected"))

    def set_confidence_threshold(self):
        new_threshold = tk.simpledialog.askfloat(self.get_text("input"), self.get_text("enter_confidence_threshold"), minvalue=0.0, maxvalue=1.0)
        if new_threshold is not None:
            self.confidence_threshold = new_threshold
            self.status_var.set(f"{self.get_text('confidence_threshold_set')} {new_threshold}")
            self.detect_button.config(state=tk.NORMAL)  # Enable the detect button


if __name__ == "__main__":
    root = tk.Tk()
    app = MangoVisionApp(root)
    root.mainloop()
