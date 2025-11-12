import cv2
from ultralytics import YOLO
import os
import tkinter as tk

# Use the model path from the GUI code
model_path = 'F:\Mango Fruit Detection project\Video detection\best.pt'  # Update if needed
model = YOLO(model_path)

def process_frame(frame):
    # Convert frame to RGB (YOLO expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run the model on the frame
    results = model.predict(source=rgb_frame)
    
    # Draw predictions on the frame
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            class_id = int(box.cls[0])
            label = f"Mango {confidence:.2f}"
            
            # Draw rectangle and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return frame

def process_video(input_video_path, output_video_path):
    # Open the video file
    video_capture = cv2.VideoCapture(input_video_path)
    
    # Get video properties
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Process the frame
        processed_frame = process_frame(frame)
        
        # Write the frame to the output video
        out.write(processed_frame)
    
    # Release everything if job is finished
    video_capture.release()
    out.release()
    cv2.destroyAllWindows()

# Define paths
input_video_path = "F:\Mango Fruit Detection project\GUI\mango.mp4"  # Update with your input video path
output_video_path = "F:\Mango Fruit Detection project\GUI\mango.mp4"  # Update with your desired output video path

# Process the video
process_video(input_video_path, output_video_path)

print("Video processing completed.")
