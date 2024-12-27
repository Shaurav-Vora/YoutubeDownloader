import tkinter as tk
from tkinter import ttk
import pyautogui

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")

# Label and dropdown to select audio or video
label_format = ttk.Label(root, text="Select format:")

format_var = tk.StringVar()
format_dropdown = ttk.Combobox(root, textvariable=format_var)
format_dropdown["values"] = ("Audio", "Video")
format_dropdown["state"] = "readonly"
format_var.set("Video")

# Radio buttons for video input
radio_var = tk.StringVar()

radio_url = ttk.Radiobutton(root, text="By URL", variable=radio_var, value="URL")
radio_playlist = ttk.Radiobutton(root, text="By Playlist", variable=radio_var, value="Playlist")
radio_channel = ttk.Radiobutton(root, text="By Channel", variable=radio_var, value="Channel")
radio_search = ttk.Radiobutton(root, text="By Search", variable=radio_var, value="Search")
radio_var.set("URL")

# Input url of video, playlist, channel, or search keywords
entry = ttk.Entry(root, width=50)
button_search = ttk.Button(root, text="Search")

# Table in form of treeview to display video details

columns = ("#","URL", "Title", "Length")

# Create the Treeview widget (table) with extended selection mode
treeview = ttk.Treeview(root, columns=columns, show="headings", selectmode="extended")

# Define column headings
treeview.heading("#", text="No.")
treeview.heading("URL", text="URL")
treeview.heading("Title", text="Title")
treeview.heading("Length", text="Length")

treeview.column("#", anchor="center", width=50, stretch=False)
treeview.column("URL", anchor="w", width=200)
treeview.column("Title", anchor="w", width=200)
treeview.column("Length", anchor="center", width=80, stretch=False)


# Label and dropdown to select video quality
label_quality = ttk.Label(root, text="Select quality:")

quality_var = tk.StringVar()
quality_dropdown = ttk.Combobox(root, textvariable=quality_var)
quality_dropdown["values"] = ("1080p", "720p")
quality_dropdown["state"] = "readonly"
quality_var.set("720p")

# filedialog to select download location
download_input = ttk.Entry(root, width=25)
button_location = ttk.Button(root, text="Choose location")

# download button
button_download = ttk.Button(root, text="Download")

# Grid layout
label_format.grid(row=1, column=0)
format_dropdown.grid(row=1, column=1)
radio_url.grid(row=2, column=0)
radio_playlist.grid(row=2, column=1)
radio_channel.grid(row=2, column=2)
radio_search.grid(row=2, column=3)
entry.grid(row=4, column=0, columnspan=3)
button_search.grid(row=4, column=3)
treeview.grid(row=5, column=0, columnspan=4, sticky="nsew")
label_quality.grid(row=6, column=0)
quality_dropdown.grid(row=6, column=1)
download_input.grid(row=7, column=0, columnspan=2)
button_location.grid(row=7, column=2)
button_download.grid(row=8, column=1)


# Start the main loop

# Set the window size
root.geometry("700x600")
root.mainloop()