#!/home/hicham/Hicham/Python/VidSnapper/venv/bin/python3

import customtkinter as ctk  # Importing CustomTkinter for modern, customizable widgets
import tkinter as tk  # Importing standard Tkinter for basic GUI functionality
from pytubefix import YouTube  # Importing YouTube from pytubefix for downloading YouTube videos

# System Settings
ctk.set_default_color_theme("green")  # Set the default color theme to blue

# Function to change between light and dark mode
def change_mode():
    if mode_switch.get() == 1:  # If the switch is turned on
        ctk.set_appearance_mode("dark")  # Set the appearance to dark mode
    else:
        ctk.set_appearance_mode("light")  # Otherwise, set the appearance to light mode

# Callback function to update the progress during the download
def on_progress(stream, chunk, bytes_remaining) -> None:
    filesize = stream.filesize  # Get the total filesize of the stream
    bytes_received = (filesize - bytes_remaining)  # Calculate the received bytes
    percentage = int(bytes_received / filesize)  # Calculate the percentage of download completed
    finished.configure(text=f"{percentage * 100} %")  # Update the label with the download percentage
    finished.update()  # Update the label in the GUI
    progress.set(percentage)  # Update the progress bar
    print(percentage)  # Print the percentage in the console for debugging

# Function to download the video or audio
def download():
    url = link.get()  # Get the URL from the input field
    if url == "":  # If the URL field is empty
        finished.configure(text="Input The URL Please!", text_color="red")  # Show error message
    else:
        try:
            yt = YouTube(url=url, on_progress_callback=on_progress)  # Initialize YouTube object with progress callback
            title.configure(text=yt.title)  # Set the title label to the video's title
            if combobox.get() == "Mp4":  # If the selected format is Mp4
                ys = yt.streams.get_highest_resolution()  # Get the highest resolution video stream
                ys.download(output_path="./Mp4")  # Download the video to the Mp4 directory
            else:
                ys = yt.streams.get_audio_only()  # Get the audio-only stream
                ys.download(output_path="./Mp3", mp3=True)  # Download the audio as an mp3 to the Mp3 directory
        except Exception as e:  # Handle any errors that occur during the download
            finished.configure(text="Error In The URL !", text_color="red")  # Show error message in GUI
            print(f"Error: {e}")  # Print the error in the console for debugging

# Create the main application window
app = ctk.CTk()
app.geometry("480x480")  # Set the size of the window
app.title("VidSnapper")  # Set the title of the window

# Main Frame
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=20, fill="both", expand=True)  # Add padding and make the frame expandable

# Mode Switch (Light/Dark Mode)
mode_switch = ctk.CTkSwitch(master=frame, text="Dark Mode", command=change_mode)
mode_switch.grid(row=0, column=0, padx=20, pady=10, sticky="w")  # Position the switch with padding

# Title Label
title = ctk.CTkLabel(frame, text="Insert A YouTube Link", font=("Arial", 20, "bold"))
title.grid(row=1, column=0, columnspan=2, pady=(20, 10), sticky="nsew")  # Position and style the title label

# Link Input
link = ctk.CTkEntry(frame, placeholder_text="Paste your link here")
link.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")  # Input field for YouTube link

# Format Selection Label
combobox_label = ctk.CTkLabel(frame, text="Select Format:")
combobox_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="e")  # Label for format selection

# Format Selection Combobox
options = ["Mp4", "Mp3"]  # Options for download format
combobox = ctk.CTkComboBox(frame, values=options)
combobox.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="w")  # Dropdown menu for selecting format

# Progress Bar Label
progress_label = ctk.CTkLabel(frame, text="Download Progress:")
progress_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="e")  # Label for the progress bar

# Progress Bar
progress = ctk.CTkProgressBar(frame)
progress.grid(row=4, column=1, padx=20, pady=(10, 0), sticky="w")  # Progress bar for download status
progress.set(0)  # Initialize progress bar to 0

# Finished Downloading Message
finished = ctk.CTkLabel(frame, text="", font=("Arial", 18,  "bold"))
finished.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")  # Label to display download completion

# Download Button
download_button = ctk.CTkButton(frame, text="Download", command=download)
download_button.grid(row=6, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")  # Button to start download

# Responsive resizing settings
app.columnconfigure(0, weight=1)  # Make the main window responsive horizontally
app.rowconfigure(0, weight=1)  # Make the main window responsive vertically
frame.columnconfigure(0, weight=1)  # Allow frame columns to expand
frame.columnconfigure(1, weight=1)  # Allow frame columns to expand

# Run the application
app.mainloop()  # Start the Tkinter event loop
