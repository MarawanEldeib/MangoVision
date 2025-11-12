MangoVision GUI
MangoVision is a graphical user interface (GUI) application designed for mango fruit detection from aerial images and videos. This application utilizes the YOLO (You Only Look Once) model for object detection and provides various features for selecting media, detecting mangoes, viewing results, and saving annotated outputs.

Features
Media Selection: Select image or video files for processing.
Mango Detection: Detect mango fruits in selected media using YOLO models.
GPS Coordinates Extraction: Extract and display GPS coordinates from image metadata.
Results Annotation: Annotate detected mangoes in images and videos with bounding boxes and confidence scores.
Save Annotated Results: Save annotated images and videos to disk.
Language Support: Switch between English and Malay.
Map View: View detected GPS coordinates on a map.
Video Controls: Play, pause, and stop video playback within the GUI.
Installation

Create a virtual environment:
"python -m venv venv"

Activate the virtual environment:
On Windows:
"venv\Scripts\activate"

On macOS and Linux:
"source venv/bin/activate"

Install required dependencies:


pip install -r requirements.txt
Dependencies
opencv-python
numpy
Pillow
tkinter
requests
folium
pywebview
exifread
ultralytics

Usage
Run the application:
"python GUI.py"

Select Media:
Click on the "Select Image/Video" button to open a file dialog and choose the media file.

Detect Mangoes:
Click on the "Detect Mangoes" button to start the detection process. The status bar will display the progress.

View Results:
Annotated results will be displayed in the GUI. You can view the GPS coordinates if available.

Save Annotated Results:
Click on the "Save Results" button to save the annotated image or video. Choose the desired file format and location.

Video Controls:
Use the play, pause, and stop buttons to control video playback.

File Structure

GUI.py: Main file to run the MangoVision application.

translations.py: Contains translations for different languages.

toolbar.py: Manages the application menu and toolbar.

themes.py: Defines the visual theme for the application.

splash_screen.py: Displays a splash screen on application startup.

icon_buttons.py: Manages the icons and buttons in the GUI.

gps_utils.py: Utility functions for extracting GPS coordinates from images.

map_view.py: Displays the GPS coordinates on a map.

image_utils.py: Functions for processing and annotating images.

video_utils.py: Functions for processing, annotating, and playing videos.

Notes
Ensure all required libraries are installed in the virtual environment.
Make sure the model files and icons are placed in the correct directories as specified in the code.

Contact
For further assistance, contact Marawan Eldeib(marawandeep13@gmail.com).