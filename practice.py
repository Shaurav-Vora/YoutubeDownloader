import tkinter as tk
from tkinter import ttk
from pytubefix import YouTube, Channel

def getVidLength(yt: YouTube):
    vid_length_seconds = yt.length
    vid_length_minutes = f"{int(vid_length_seconds / 60)}:{vid_length_seconds % 60:.2f}"
    return vid_length_minutes

# Fetch video data
c = Channel("https://www.youtube.com/@shrutii.8282")
all_vid_data = []

for url in c.video_urls:
    my_url = url.watch_url
    yt = YouTube(my_url)
    yt_title = yt.title
    length = getVidLength(yt)
    all_vid_data.append((my_url, yt_title, length))
    # print((my_url, yt_title, length))
    # print()


# Function to handle multiple row selection
def on_rows_select():
    # Get the selected items
    selected_items = treeview.selection()
    if selected_items:
        # Iterate through selected rows and print their values
        for item in selected_items:
            row_data = treeview.item(item)["values"]
            print(f"Selected Row: {row_data}")


# Create the main window
root = tk.Tk()
root.title("YouTube Video List")

# Define the column names for the table
columns = ("#", "Title", "Length")

# Create the Treeview widget (table) with extended selection mode
treeview = ttk.Treeview(root, columns=columns, show="headings", selectmode="extended")

# Button
button = ttk.Button(root,text="Download",command = on_rows_select)

# Define column headings
treeview.heading("#", text="URL")
treeview.heading("Title", text="Title")
treeview.heading("Length", text="Length")

# Insert the data into the table
for idx, data in enumerate(all_vid_data):
    treeview.insert("", "end", values=(data[0], data[1], data[2]))


# Grid layout for Treeview
treeview.grid(row=0, column=0, columnspan=3, sticky="nsew")
button.grid(row=1,column=0)

# Adjust column and row weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Start the Tkinter event loop
root.mainloop()