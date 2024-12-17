import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
from controller import upload_file
import eyed3  # Add this import to handle MP3 metadata
from io import BytesIO
# Initialize pygame mixer
pygame.mixer.init()

# Home Page
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Add title label
        label = tk.Label(self, text="Welcome to the Music Player", font=("Arial", 20))
        label.pack(pady=50)

        # Button to navigate to the Music Player page
        button = tk.Button(self, text="Go to Music Player", command=self.go_to_music_player)
        button.pack(pady=20)

        # Button to navigate to the Upload page
        upload_button = tk.Button(self, text="Upload Music", command=self.go_to_upload_page)
        upload_button.pack(pady=20)

    def go_to_music_player(self):
        self.controller.show_page(MusicPlayerPage)

    def go_to_upload_page(self):
        self.controller.show_page(UploadPage)


class MusicPlayerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.is_playing = False
        self.song_length = 0
        self.music_file = "ss.mp3"  # Replace with the actual path to the music file
        self.manual_update = False  # Flag to detect manual updates on the scale

        # Create widgets
        self.play_button = tk.Button(self, text="Play", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.play_music)
        self.play_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="Stop", font=("Arial", 14), bg="#f44336", fg="white", command=self.stop_music)
        self.stop_button.pack(pady=10)

        # Add cover image display
        self.cover_image_label = tk.Label(self)
        self.cover_image_label.pack(pady=10)

        # Scale to display the song progress
        self.progress_scale = tk.Scale(self, from_=0, to=100, orient="horizontal", length=400, sliderlength=20)
        self.progress_scale.pack(pady=20)
        # Bind to the release event
        self.progress_scale.bind("<ButtonRelease-1>", self.on_scale_release)
        self.progress_scale.bind("<Button-1>", self.on_scale_click)

        # Back to Home Button
        self.back_button = tk.Button(self, text="Back to Home", font=("Arial", 12), bg="#008CBA", fg="white", command=self.back_to_home)
        self.back_button.pack(pady=10)

    def play_music(self):
        if not self.is_playing:
            if not os.path.exists(self.music_file):
                print(f"Error: Music file '{self.music_file}' not found.")
                return

            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play()
            self.is_playing = True

            # Get song length (in seconds)
            self.song_length = pygame.mixer.Sound(self.music_file).get_length()

            # Extract cover image from the MP3 file
            self.show_cover_image_from_mp3(self.music_file)

            # Start updating the scale (song progress)
            self.update_progress_scale()

    def stop_music(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.progress_scale.set(0)  # Reset progress scale
            self.cover_image_label.config(image="")  # Clear cover image

    def update_progress_scale(self):
        if self.is_playing:
            # Get the current position of the song (in seconds)
            current_time = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
            progress = (current_time / self.song_length) * 100  # Calculate progress as a percentage

            # Only update scale if the user hasn't manually changed it
            if not self.manual_update:
                self.progress_scale.set(progress)  # Update the scale

            # Continue updating the progress scale every 100ms
            self.after(100, self.update_progress_scale)  # Keep updating even if the song is near the end

    def show_cover_image(self, image_path):
        if not os.path.exists(image_path):
            print(f"Error: Cover image '{image_path}' not found.")
            return

        # Open and resize the image
        image = Image.open(image_path)
        image = image.resize((150, 150))  # Resize the image to fit the window
        self.cover_image = ImageTk.PhotoImage(image)

        # Display the cover image
        self.cover_image_label.config(image=self.cover_image)

    def show_cover_image_from_mp3(self, mp3_file):
        """Extract and show cover image from MP3 metadata"""
        audio_file = eyed3.load(mp3_file)

        # Check if there's any album art
        if audio_file.tag is not None and audio_file.tag.images:
            # Get the first image (usually album art)
            image_data = audio_file.tag.images[0].image_data

            # Open the image from binary data
            image = Image.open(BytesIO(image_data))
            image = image.resize((150, 150))  # Resize to fit the window

            # Convert to PhotoImage and display it
            self.cover_image = ImageTk.PhotoImage(image)
            self.cover_image_label.config(image=self.cover_image)
        else:
            print("No cover image found in MP3 metadata.")

    def on_scale_release(self, event):
        """When the user releases the scale, update the song's position"""
        self.manual_update = False  # Reset the flag when user releases the slider
        progress_percentage = float(self.progress_scale.get())
        new_pos = (progress_percentage / 100) * self.song_length  # Convert percentage to actual seconds
        pygame.mixer.music.set_pos(new_pos)  # Set the new position in the song

    def on_scale_click(self, event):
        """Flag that the user is manually adjusting the slider"""
        self.manual_update = True

    def back_to_home(self):
        self.controller.show_page(HomePage)

# Upload Page
class UploadPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        

        # Add title label
        label = tk.Label(self, text="Upload Music to Server", font=("Arial", 20))
        label.pack(pady=50)

        # Button to upload music
        upload_button = tk.Button(self, text="Select Music File", command=self.select_music_file)
        upload_button.pack(pady=20)

        # Label to show the selected file name
        self.selected_file_label = tk.Label(self, text="No file selected", font=("Arial", 12))
        self.selected_file_label.pack(pady=20)

        # Button to upload the selected file
        upload_to_server_button = tk.Button(self, text="Upload to Server", command=self.upload_file)
        upload_to_server_button.pack(pady=20)

        # Back to Home Button
        back_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_button.pack(pady=20)

        # Store the selected file path
        self.selected_file = None

    def select_music_file(self):
        """Open file dialog to select an MP3 file."""
        file_path = filedialog.askopenfilename(
            title="Select a Music File", 
            filetypes=[("MP3 Files", "*.mp3")]
        )
        if file_path:
            self.selected_file = file_path
            self.selected_file_label.config(text=f"Selected File: {os.path.basename(file_path)}")

    def upload_file(self):
        """Upload the selected file to the server."""
        print('uploooood')
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected!")
            return
        print(self.selected_file)
        upload_file(self.selected_file)
        # # Prepare the file for upload
        # files = {'file': open(self.selected_file, 'rb')}

        # # Specify the URL of the server endpoint
        # upload_url = "ws://localhost:3000/upload"  # Replace with your server URL

        # try:
        #     # Send the POST request with the file
        #     # response = requests.post(upload_url, files=files)
        #     if response.status_code == 200:
        #         messagebox.showinfo("Success", "File uploaded successfully!")
        #     else:
        #         messagebox.showerror("Error", "Failed to upload the file.")
        # except requests.exceptions.RequestException as e:
        #     messagebox.showerror("Error", f"Error during upload: {str(e)}")
        # finally:
        #     files['file'].close()

    def back_to_home(self):
        self.controller.show_page(HomePage)


# Main Application
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Beautiful Music Player with Page Navigation")
        self.geometry("500x400")

        # Dictionary to store frames
        self.frames = {}

        # Create and store frames
        for F in (HomePage, MusicPlayerPage, UploadPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page initially
        self.show_page(HomePage)

    def show_page(self, page_class):
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_forget()

        # Show the selected frame
        page_name = page_class.__name__
        frame = self.frames[page_name]
        frame.grid(row=0, column=0, sticky="nsew")


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
