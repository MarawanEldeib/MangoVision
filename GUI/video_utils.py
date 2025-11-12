import cv2
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

def select_video_file(app):
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if file_path:
        process_selected_video(app, file_path)

def process_selected_video(app, file_path):
    app.is_video = True
    app.video_frames = []
    app.annotated_frames = []  # Add this line
    app.video_cap = cv2.VideoCapture(file_path)
    if not app.video_cap.isOpened():
        messagebox.showerror(app.get_text("error"), app.get_text("video_load_error"))
        return

    total_frames = int(app.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    app.progress_bar["maximum"] = total_frames

    while True:
        ret, frame = app.video_cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        app.video_frames.append(frame)
        app.progress_bar["value"] += 1
        app.root.update_idletasks()

    app.display_video_frame(0)
    app.status_var.set(app.get_text("video_loaded"))
    app.detect_button.config(state=tk.NORMAL)
    app.save_button.config(state=tk.DISABLED)

    # Show video control buttons
    app.video_controls_frame.pack(fill=tk.X, padx=5, pady=5)
    app.play_button.config(state=tk.NORMAL)
    app.pause_button.config(state=tk.DISABLED)
    app.stop_button.config(state=tk.DISABLED)

def display_video_frame(app, frame_idx):
    if frame_idx < len(app.video_frames):
        frame = app.video_frames[frame_idx]
        frame = Image.fromarray(frame)  # Ensure Image is imported from PIL
        frame.thumbnail((640, 360))
        img = ImageTk.PhotoImage(frame)
        app.image_label.config(image=img)
        app.image_label.image = img

def detect_mangoes_in_video(app):
    app.summary = []
    app.annotated_frames = []  # Add this line
    frame_idx = 0
    app.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    total_frames = int(app.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = app.video_cap.get(cv2.CAP_PROP_FPS)
    frame_interval_in_frames = int(fps * app.frame_interval)

    for idx in range(total_frames):
        ret, frame = app.video_cap.read()
        if not ret:
            break
        if idx % frame_interval_in_frames == 0:
            results = app.current_model.predict(source=frame)
            boxes = results[0].boxes.xyxy
            confidences = results[0].boxes.conf
            valid_detections = [(box, conf) for box, conf in zip(boxes, confidences) if conf >= app.confidence_threshold]
            frame_summary = [{'Mango No.': i + 1, 'Frame': idx, 'Confidence Score': f"{conf:.2f}", 'Box Coordinates': box.tolist()} for i, (box, conf) in enumerate(valid_detections)]
            app.summary.extend(frame_summary)
            for i, (box, conf) in enumerate(valid_detections):
                x1, y1, x2, y2 = map(int, box.tolist())
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red color
                label = f"{conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # Red color
        app.annotated_frames.append(frame)  # Store the annotated frame
        app.progress_bar["value"] = idx
        app.root.update_idletasks()

    app.display_summary(app.summary)
    app.status_var.set(app.get_text("detection_complete"))
    app.detect_button.config(state=tk.DISABLED)
    app.save_button.config(state=tk.NORMAL)
    play_video(app)  # Play the video with detections in GUI

def save_annotated_video(app, save_path):
    # Determine the codec based on the file extension
    if save_path.endswith(".mp4"):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    elif save_path.endswith(".avi"):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    else:
        messagebox.showerror(app.get_text("error"), "Unsupported file format")
        return

    out = cv2.VideoWriter(save_path, fourcc, app.video_cap.get(cv2.CAP_PROP_FPS), (app.annotated_frames[0].shape[1], app.annotated_frames[0].shape[0]))
    for frame in app.annotated_frames:  # Save annotated frames
        out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    out.release()
    messagebox.showinfo(app.get_text("save_successful"), f"{app.get_text('results_saved_to')} {save_path}")
    app.status_var.set(app.get_text("results_saved"))


def play_video(app):
    app.video_playing = True
    if app.video_cap.get(cv2.CAP_PROP_POS_FRAMES) == app.video_cap.get(cv2.CAP_PROP_FRAME_COUNT):
        app.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart if at the end
    play_next_frame(app)
    app.play_button.config(state=tk.DISABLED)
    app.pause_button.config(state=tk.NORMAL)
    app.stop_button.config(state=tk.NORMAL)

def pause_video(app):
    app.video_playing = False
    app.play_button.config(state=tk.NORMAL)
    app.pause_button.config(state=tk.DISABLED)

def stop_video(app):
    app.video_playing = False
    app.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    app.display_video_frame(0)
    app.play_button.config(state=tk.NORMAL)
    app.pause_button.config(state=tk.DISABLED)
    app.stop_button.config(state=tk.DISABLED)

def play_next_frame(app):
    if app.video_playing and app.video_cap:
        frame_idx = int(app.video_cap.get(cv2.CAP_PROP_POS_FRAMES))
        if frame_idx < len(app.annotated_frames):
            frame = app.annotated_frames[frame_idx]
        else:
            ret, frame = app.video_cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                app.annotated_frames.append(frame)
        if frame_idx < len(app.annotated_frames):
            frame = app.annotated_frames[frame_idx]
            frame = Image.fromarray(frame)
            frame.thumbnail((640, 360))
            img = ImageTk.PhotoImage(frame)
            app.image_label.config(image=img)
            app.image_label.image = img
            app.root.after(int(1000 / app.video_cap.get(cv2.CAP_PROP_FPS)), lambda: play_next_frame(app))
        else:
            app.stop_video()
