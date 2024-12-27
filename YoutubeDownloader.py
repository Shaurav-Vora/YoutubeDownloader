import tkinter as tk
from tkinter import ttk
import pyautogui
from pytubefix import YouTube, Channel, Playlist, Search


# Function to handle download type
def on_format_type(event):
    # Get the selected download type
    download_type = format_var.get()
    print(f"Selected download type: {download_type}")
    if download_type == "Audio":
        quality_dropdown.config(state="disabled")
    else:
        quality_dropdown.config(state="readonly")

# Function to handle video input type
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(foreground='grey')

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(foreground='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
        
def getVidLength(yt: YouTube):
    vid_length_seconds = yt.length
    vid_length_minutes = f"{int(vid_length_seconds / 60)}:{vid_length_seconds % 60:.2f}"
    return vid_length_minutes

def display_video_details_individual(url):
    yt = YouTube(url)
    yt_title = yt.title
    length = getVidLength(yt)
    return [(url, yt_title, length)]

def display_video_details_playlist(url):
    p = Playlist(url)
    all_vid_data = []
    for url in p.videos:
        my_url = url.watch_url
        yt = YouTube(my_url)
        yt_title = yt.title
        length = getVidLength(yt)
        all_vid_data.append((my_url, yt_title, length))
    return all_vid_data

def display_video_details_channel(url):
    c = Channel(url)
    all_vid_data = []
    for url in c.video_urls:
        my_url = url.watch_url
        yt = YouTube(my_url)
        yt_title = yt.title
        length = getVidLength(yt)
        all_vid_data.append((my_url, yt_title, length))
    return all_vid_data

def display_video_details_search(keywords):
    results = Search(keywords)
    all_vid_data = []
    for video in results.videos:
        if (len(all_vid_data) == 15):
            break
        my_url = video.watch_url
        yt = YouTube(my_url)
        yt_title = yt.title
        length = getVidLength(yt)
        all_vid_data.append((my_url, yt_title, length))
    return all_vid_data

def add_to_table(data):
    for idx, data in enumerate(data):
        treeview.insert("", "end", values=(idx+1, data[0], data[1], data[2]))

def on_search():
    radio_selected = radio_var.get()
    search_input = entry.get()
    if radio_selected == "URL":
        data = display_video_details_individual(search_input)
    elif radio_selected == "Playlist":
        data = display_video_details_playlist(search_input)
    elif radio_selected == "Channel":
        data = display_video_details_channel(search_input)
    else:
        data = display_video_details_search(search_input)

    add_to_table(data)

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
button_search = ttk.Button(root, text="Search",command=on_search)

add_placeholder(entry, "Enter link for individual URL, Playlist, Channel, or keywords")

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

# Bind event when dropdown value changes
format_dropdown.bind("<<ComboboxSelected>>", on_format_type)

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