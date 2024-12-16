from asyncio import sleep
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame

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

    def go_to_music_player(self):
        self.controller.show_page(MusicPlayerPage)


# Music Player Page
class MusicPlayerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.is_playing = False
        self.song_length = 0
        self.music_file = "ss.mp3"  # Replace with the actual path to the music file

        # Create widgets
        self.play_button = tk.Button(self, text="Play", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.play_music)
        self.play_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="Stop", font=("Arial", 14), bg="#f44336", fg="white", command=self.stop_music)
        self.stop_button.pack(pady=10)

        # Add cover image display
        self.cover_image_label = tk.Label(self)
        self.cover_image_label.pack(pady=10)

        # Progress bar to display the song progress
        self.progress_bar = ttk.Progressbar(self, length=400, mode="determinate")
        self.progress_bar.pack(pady=20)
        self.progress_bar.bind("<ButtonRelease-1>", self.on_progress_bar_click)

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

            # Show the cover image
            self.show_cover_image("your_album_cover.jpg")  # Replace with actual image file

            # Start updating progress bar
            self.update_progress_bar()

    def stop_music(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.progress_bar['value'] = 0  # Reset progress bar
            self.cover_image_label.config(image="")  # Clear cover image

    def update_progress_bar(self):
        if self.is_playing:
            # pass
            # Get the current position of the song (in seconds)
            current_time = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
            progress = (current_time / self.song_length) * 100  # Calculate progress as a percentage
            self.progress_bar['value'] = progress

            # Continue updating the progress bar if the song is still playing
            # if current_time < self.song_length:
            #     self.after(100, self.update_progress_bar)  # Update every 100ms

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

    def on_progress_bar_click(self, event):
        # Get the position where the user clicked on the progress bar
        click_position = event.x
        progress_percentage = (click_position / self.progress_bar.winfo_width()) * 100
        print('sss ',progress_percentage)
        # Set the music position based on the clicked position
        pygame.mixer.music.set_pos((progress_percentage / 100) * self.song_length)

        # Start updating the progress bar from the new position
        # current_time = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
        # progress = (current_time / self.song_length) * 100  # Calculate progress as a percentage
        # self.progress_bar['value'] = progress_percentage
        self.update_progress_bar()
        # print(current_time)
        print(self.song_length)
        # print(progress)

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
        for F in (HomePage, MusicPlayerPage):
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
