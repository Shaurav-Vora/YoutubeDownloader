import tkinter as tk
from tkinter import ttk
from pytubefix import YouTube, Channel, Playlist, Search
from tkinter import filedialog

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
    
def choose_location():
    folder = filedialog.askdirectory()
    if folder:
        download_input.delete(0, tk.END)
        download_input.insert(0, folder)
    return folder

def download_video():
    selected_items = treeview.selection()
    if selected_items:
        for item in selected_items:
            row_data = treeview.item(item)["values"]
            url = row_data[1]
            save_path = download_input.get()
            if not save_path:
                save_path = choose_location()
            if save_path:
                download_selected_video(url, save_path)
    else:
        selected_items = treeview.get_children()
        for item in selected_items:
            row_data = treeview.item(item)["values"]
            url = row_data[1]
            save_path = download_input.get()
            if not save_path:
                save_path = choose_location()
            if save_path:
                download_selected_video(url, save_path)

def download_selected_video(url, save_path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(file_extension="mp4")
        if quality_var.get() == "Best quality":
            res = streams.get_highest_resolution()
        else:
            res = streams.get_lowest_resolution()
        res = streams.get_highest_resolution()
        res.download(output_path=save_path)
    except Exception as e:
        print(e)

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")

# Style Configuration
style = ttk.Style()
style.configure("TLabel", padding=6, font=("Arial", 10))
style.configure("TButton", padding=6, font=("Arial", 10))
style.configure("TEntry", padding=6, font=("Arial", 10))
style.configure("TCombobox", padding=6, font=("Arial", 10))
style.configure("TRadiobutton", padding=6, font=("Arial", 10))
style.configure("Treeview", font=("Arial", 10))
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

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
button_search = ttk.Button(root, text="Search", command=on_search)

add_placeholder(entry, "Enter link for individual URL, Playlist, Channel, or keywords")

# Table in form of treeview to display video details

columns = ("#", "URL", "Title", "Length")

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

# Add Scrollbars
scrollbar = ttk.Scrollbar(root, orient="vertical", command=treeview.yview)
treeview.configure(yscroll=scrollbar.set)
scrollbar.grid(row=5, column=4, sticky="ns")

# Label and dropdown to select video quality
label_quality = ttk.Label(root, text="Select quality:")

quality_var = tk.StringVar()
quality_dropdown = ttk.Combobox(root, textvariable=quality_var)
quality_dropdown["values"] = ("Best quality", "Lowest quality")
quality_dropdown["state"] = "readonly"
quality_var.set("Best quality")

# filedialog to select download location
download_input = ttk.Entry(root, width=25)
button_location = ttk.Button(root, text="Choose location", command=choose_location)

# download button
button_download = ttk.Button(root, text="Download", command=download_video)

# Bind event when dropdown value changes
format_dropdown.bind("<<ComboboxSelected>>", on_format_type)

# Grid layout
label_format.grid(row=0, column=0, padx=10, pady=5, sticky="w")
format_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")
radio_url.grid(row=1, column=0, padx=10, pady=5, sticky="w")
radio_playlist.grid(row=1, column=1, padx=10, pady=5, sticky="w")
radio_channel.grid(row=1, column=2, padx=10, pady=5, sticky="w")
radio_search.grid(row=1, column=3, padx=10, pady=5, sticky="w")
entry.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
button_search.grid(row=2, column=3, padx=10, pady=10, sticky="ew")
treeview.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
label_quality.grid(row=4, column=0, padx=10, pady=5, sticky="w")
quality_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky="w")
download_input.grid(row=4, column=2, columnspan=2, padx=10, pady=5, sticky="ew")
button_location.grid(row=4, column=2, padx=10, pady=5, sticky="w")
button_download.grid(row=6, column=1, padx=10, pady=10)

# Configure grid weights for better layout management
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(3, weight=1)

# Set the window size
root.geometry("800x600")
root.mainloop()