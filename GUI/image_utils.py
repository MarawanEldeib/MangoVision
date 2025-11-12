import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw,ImageFont
import numpy as np
import cv2
import os
from gps_utils import extract_gps_and_datetime


from gps_utils import extract_gps_and_datetime

def process_selected_image(app, file_path):
    app.is_video = False
    app.video_frames = []
    app.video_cap = None
    app.image_path = file_path  # Set image_path to the selected image file path

    try:
        # Load and display the image
        image = Image.open(file_path)
        image.thumbnail((640, 360))
        img = ImageTk.PhotoImage(image)
        app.image_label.config(image=img)
        app.image_label.image = img
        app.status_var.set(app.get_text("image_loaded"))
        app.detect_button.config(state=tk.NORMAL)
        app.save_button.config(state=tk.DISABLED)

        # Extract and display GPS and datetime data
        exif_data = extract_gps_and_datetime(file_path)
        app.display_exif_data(exif_data)
        
    except Exception as e:
        messagebox.showerror(app.get_text("error"), str(e))
        app.status_var.set(app.get_text("error"))



def display_image(app, image_path):
    image = Image.open(image_path)
    image.thumbnail((640, 360))
    img = ImageTk.PhotoImage(image)
    app.image_label.config(image=img)
    app.image_label.image = img
    app.image_label.image_path = image_path

def annotate_image(app, image_path, valid_detections):
    image = cv2.imread(image_path)
    for box, conf in valid_detections:
        x1, y1, x2, y2 = map(int, box.tolist())
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    detected_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    detected_image.thumbnail((640, 360))
    return ImageTk.PhotoImage(detected_image)

def detect_mangoes_in_image(app):
    if not app.image_path:
        messagebox.showerror(app.get_text("error"), "No image selected.")
        return

    app.status_var.set(app.get_text("detecting_mangoes"))
    try:
        image = Image.open(app.image_path)
        original_image = image.copy()  # Keep a copy of the original image
        # Perform detection on the image using the model
        results = app.current_model.predict(source=app.image_path)
        boxes = results[0].boxes.xyxy
        confidences = results[0].boxes.conf
        valid_detections = [(box, conf) for box, conf in zip(boxes, confidences) if conf >= app.confidence_threshold]
        app.summary = [{'Mango No.': i + 1, 'Confidence Score': f"{conf:.2f}", 'Box Coordinates': box.tolist()} for i, (box, conf) in enumerate(valid_detections)]

        # Annotate the image
        draw = ImageDraw.Draw(image)
        font_path = "arial.ttf"  # Path to a .ttf font file
        font_size = 20  # Adjust font size as needed
        font = ImageFont.truetype(font_path, font_size)
        for i, (box, conf) in enumerate(valid_detections):
            x1, y1, x2, y2 = map(int, box.tolist())
            draw.rectangle([x1, y1, x2, y2], outline="red", width=6)
            label = f"{conf:.2f}"
            draw.text((x1, y1 - font_size), label, fill="red", font=font)

        # Resize the image back to fit the display size (640, 360)
        image.thumbnail((640, 360))
        img = ImageTk.PhotoImage(image)
        app.image_label.config(image=img)
        app.image_label.image = img

        app.display_summary(app.summary)
        app.status_var.set(app.get_text("detection_complete"))
        app.detect_button.config(state=tk.DISABLED)
        app.save_button.config(state=tk.NORMAL)

        app.annotated_image = original_image  # Store the annotated image
    except Exception as e:
        messagebox.showerror(app.get_text("error"), str(e))
        app.status_var.set(app.get_text("error"))


def save_annotated_image(app, save_path):
    try:
        annotated_image = app.annotated_image
        if annotated_image:
            draw = ImageDraw.Draw(annotated_image)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()
                
            for item in app.summary:
                x1, y1, x2, y2 = map(int, item['Box Coordinates'])
                draw.rectangle([x1, y1, x2, y2], outline="red", width=6)
                label = f"{item['Confidence Score']}"
                text_bbox = draw.textbbox((0, 0), label, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                draw.text((x1, y1 - text_height), label, fill="red", font=font)
            annotated_image.save(save_path)
            messagebox.showinfo(app.get_text("save_successful"), f"{app.get_text('results_saved_to')} {save_path}")
            app.status_var.set(app.get_text("results_saved"))
        else:
            messagebox.showerror(app.get_text("error"), "No annotated image to save.")
    except Exception as e:
        messagebox.showerror(app.get_text("error"), str(e))