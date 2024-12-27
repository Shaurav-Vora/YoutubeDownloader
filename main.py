from pytubefix import YouTube
import tkinter as tk
from tkinter import filedialog

def download_video(url, save_path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        high_res = streams.get_highest_resolution()
        high_res.download(output_path=save_path)
    except Exception as e:
        print(e)


def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")

    return folder

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    video_url = input("Enter a YouTube url: ")
    save_dir = open_file_dialog()
    
    if not save_dir:
        print("Invalid location")
    else:
        download_video(video_url,save_dir)