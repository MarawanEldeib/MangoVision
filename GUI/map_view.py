import tkinter as tk
import folium
from tkinter import Toplevel, messagebox
from folium import Map, Marker
from io import BytesIO
import webview
import requests

def show_map(lat, lon):
    # Create a map centered around the given coordinates
    folium_map = Map(location=[lat, lon], zoom_start=12)
    Marker(location=[lat, lon], popup='Image Location').add_to(folium_map)

    # Save the map as HTML content
    map_data = BytesIO()
    folium_map.save(map_data, close_file=False)
    return map_data.getvalue().decode()

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def display_map_in_app(root, lat, lon):
    if check_internet_connection():
        map_html = show_map(lat, lon)

        # Create a Toplevel window for the map
        map_window = Toplevel(root)
        map_window.title("Map View")
        map_window.geometry("800x600")

        # Create a WebView to display the map
        window = webview.create_window("Map View", html=map_html, width=800, height=600, resizable=True)
        
        # Start the webview without any additional parameters
        webview.start(gui='tkinter')

        # Destroy the Tkinter Toplevel window after webview closes
        map_window.destroy()
    else:
        if messagebox.askretrycancel("No Internet Connection", "Please connect to the internet and try again."):
            os.system('start ms-settings:network-status')
