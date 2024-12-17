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

# Login Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Add title label
        label = tk.Label(self, text="Login", font=("Arial", 20))
        label.pack(pady=50)

        # Username Label and Entry
        self.username_label = tk.Label(self, text="Username:", font=("Arial", 12))
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = tk.Label(self, text="Password:", font=("Arial", 12))
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        login_button = tk.Button(self, text="Login", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.login)
        login_button.pack(pady=20)

        # Link to Sign Up page
        signup_button = tk.Button(self, text="Don't have an account? Sign Up", font=("Arial", 12), command=self.go_to_signup_page)
        signup_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Example validation (replace with your logic)
        if username == "admin" and password == "password":
            messagebox.showinfo("Login", "Login successful!")
            self.controller.show_page(HomePage)  # Go to the HomePage
        else:
            messagebox.showerror("Login", "Invalid username or password")

    def go_to_signup_page(self):
        self.controller.show_page(SignupPage)


# Signup Page
class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Add title label
        label = tk.Label(self, text="Sign Up", font=("Arial", 20))
        label.pack(pady=50)

        # Username Label and Entry
        self.username_label = tk.Label(self, text="Username:", font=("Arial", 12))
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = tk.Label(self, text="Password:", font=("Arial", 12))
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        # Confirm Password Label and Entry
        self.confirm_password_label = tk.Label(self, text="Confirm Password:", font=("Arial", 12))
        self.confirm_password_label.pack(pady=10)
        self.confirm_password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.confirm_password_entry.pack(pady=5)

        # Sign Up Button
        signup_button = tk.Button(self, text="Sign Up", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.signup)
        signup_button.pack(pady=20)

        # Link to Login page
        login_button = tk.Button(self, text="Already have an account? Login", font=("Arial", 12), command=self.go_to_login_page)
        login_button.pack(pady=10)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Check if password and confirm password match
        if password != confirm_password:
            messagebox.showerror("Signup", "Passwords do not match!")
            return

        # Example: Just a simple check for username and password (you should save this info in a database or file)
        if username == "" or password == "":
            messagebox.showerror("Signup", "Please fill in all fields.")
            return

        # Simulating saving the user data
        messagebox.showinfo("Signup", "Signup successful! You can now login.")
        self.controller.show_page(LoginPage)

    def go_to_login_page(self):
        self.controller.show_page(LoginPage)


# Home Page
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#1C1C24",bd=100,padx=10)
        top_frame = tk.LabelFrame(self, bg='#151517', bd=3, padx=0, relief=tk.SUNKEN)
        top_frame.grid(row=0,column=0,pady = 10 )
        layout_frame = tk.Frame(self, bg='#131315')
        layout_frame.grid()
        array1 = list(range(40))  # First array for the first scrollable area
        array2 = list(range(50))  
        self.create_scrollable_area(layout_frame, array1, 0, action="Songs")
        self.create_scrollable_area(layout_frame, array2, 1, action="Playlist")  # Changed column_index to 1 for better layout


        # Add title label
        label = tk.Label(top_frame, text="Welcome to the Music Player", font=("Arial", 20),bg="#151517",fg="#FEFFFA")
        label.grid(row=0,column=0,columnspan=3,sticky=tk.E + tk.W)

        # Button to navigate to the Music Player page
        button = tk.Button(self, text="Go to Music Player",bg="#151517",fg="#FEFFFA", command=self.go_to_music_player)
        button.grid(pady=20)

        # Button to navigate to the Upload page
        upload_button = tk.Button(self, text="Upload Music",bg="#151517",fg="#FEFFFA", command=self.go_to_upload_page)
        upload_button.grid(pady=20)
    def create_scrollable_area(self, layout_frame, array, column_index, action):
        scrollable_frame = tk.LabelFrame(layout_frame, text=action, bg='#151517', fg='#FEFFFA', border=10)  
        scrollable_frame.grid(row=0,column=column_index)  # Adjusted row index and padding

        # Create a vertical scrollbar
        v = tk.Scrollbar(scrollable_frame)
        v.pack(side='right', fill='y')

        # Create a canvas to hold the scrollable frame
        canvas = tk.Canvas(scrollable_frame, bg='#151517')
        canvas.pack(side='left', fill='both', expand=True)

        # Attach the vertical scrollbar to the canvas
        v.config(command=canvas.yview)
        canvas.config(yscrollcommand=v.set)

        # Create a scrollable frame in the canvas
        scrollable_internal_frame = tk.Frame(canvas, bg='#151517')
        canvas.create_window((0, 0), window=scrollable_internal_frame, anchor="nw")

        # Configure the scrollable frame to update the scroll region
        scrollable_internal_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        if action == "Songs":
            self.create_songs(scrollable_internal_frame, array)
        else:
            self.create_playlists(scrollable_internal_frame, array)

    def create_playlists(self, scrollable_frame, array):
        for i in range(len(array)):
            button_text = f"playlist {array[i]}"
            button = tk.Button(scrollable_frame, text=button_text, command=lambda text=button_text: self.open_new_window(text), padx=100, fg='#FEFFFA')
            button.configure(bg="#22222C")
            number = tk.Label(scrollable_frame, text=f"{i + 1}.", padx=5)
            number.grid(row=i, column=0)
            button.grid(row=i, column=1)

    def create_songs(self, scrollable_frame, array):
        for i in range(len(array)):
            button_text = f"song {array[i]}"
            button = tk.Button(scrollable_frame, text=button_text, command=lambda text=button_text: self.open_new_window(text), padx=100, fg='#FEFFFA', anchor="e")
            button.configure(bg="#22222C")
            number = tk.Label(scrollable_frame, text=f"{i + 1}.", padx=5)
            number.grid(row=i, column=0)
            button.grid(row=i, column=1)

    def open_new_window(self, button_name):
        new_window = tk.Toplevel()
        new_window.title(button_name)
        label = tk.Label(new_window, text=f"You clicked {button_name}!")
        label.pack(padx=20, pady=20)

    def profile_action(self):
        messagebox.showinfo("Profile", "Profile button clicked!")

    def go_to_music_player(self):
        self.controller.show_page(MusicPlayerPage)

    def go_to_upload_page(self):
        self.controller.show_page(UploadPage)



class MusicPlayerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=1240,height=700,padx=450,bg='#1C1C24')
        global songname
        songname = "madareto"

        self.is_playing = False
        self.song_length = 0
        self.music_file = "ss.mp3"  # Replace with the actual path to the music file
        self.manual_update = False  # Flag to detect manual updates on the scale
        top_frame = tk.LabelFrame(self, bg='#151517', bd=3, padx=0, relief=tk.SUNKEN)
        top_frame.grid(row=0,column=0,columnspan=3,pady = 100 )
        label = tk.Label(top_frame, text=songname, font=("Arial", 20),bg="#151517",fg="#FEFFFA")
        label.grid(row=0,column=0,columnspan=2,sticky=tk.E + tk.W)

        button_frame = tk.LabelFrame(self, bg='#1C1C24', bd=3, padx=0, relief=tk.SUNKEN)
        button_frame.grid(row=3,column=1,columnspan=3,pady = 10 )

        # Create widgets
        self.play_button = tk.Button(button_frame, text="Play", font=("Arial", 14),bg="#151517",fg="#FEFFFA", command=self.play_music)
        self.play_button.grid(row=3,column=0,padx=50)

        self.stop_button = tk.Button(button_frame, text="Stop", font=("Arial", 14),bg="#151517",fg="#FEFFFA", command=self.stop_music)
        self.stop_button.grid(row=3,column=2,padx=50)

        # Add cover image display
        self.cover_image_label = tk.Label(self,width=20,height=10)
        self.cover_image_label.grid(row=1,column=1)

        # Scale to display the song progress
        self.progress_scale = tk.Scale(self, from_=0, to=100, orient="horizontal", length=400, sliderlength=20)
        self.progress_scale.grid(row=2,column = 1,pady=10)
        # Bind to the release event
        self.progress_scale.bind("<ButtonRelease-1>", self.on_scale_release)
        self.progress_scale.bind("<Button-1>", self.on_scale_click)

        # Back to Home Button
        self.back_button = tk.Button(self, text="Back to Home", font=("Arial", 12), bg="#008CBA", fg="white", command=self.back_to_home)
        self.back_button.grid(row=4,column=1)

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
            self.cover_image_label1.config(image="")  # Clear cover image

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
            self.cover_image_label.grid_forget
            self.cover_image_label1 = tk.Label(self)
            self.cover_image_label1.grid(row=1,column=1)
            self.cover_image_label1.config(image=self.cover_image)
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
        
    def back_to_home(self):
        self.controller.show_page(HomePage)


# Main Application
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Beautiful Music Player with Page Navigation")
        self.geometry("1280x720")
        self.config(bg="#1C1C24")

        # Dictionary to store frames
        self.frames = {}

        # Create and store frames
        for F in (LoginPage,SignupPage, HomePage, MusicPlayerPage, UploadPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0,columnspan=3 ,sticky=tk.W+tk.E+tk.S)

        # Show the login page initially
        self.show_page(LoginPage)

    def show_page(self, page_class):
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_forget()

        # Show the selected frame
        page_name = page_class.__name__
        frame = self.frames[page_name]
        frame.grid(row=0,column =0)


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
