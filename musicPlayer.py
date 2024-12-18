import os
import tkinter as tk
from tkinter import PhotoImage, filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
from controller import upload_file ,  login , signup , get_songs
import eyed3  # Add this import to handle MP3 metadata
from io import BytesIO
# Initialize pygame mixer
pygame.mixer.init()

# Login Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.config(width=1240,height=700,padx=530,pady=30,bg='#1C1C24')
        self.controller = controller

        # Add title label
        label = tk.Label(self, text="Login", font=("Arial", 20),bg="#151517",bd=1,fg="#FEFFFA",relief=tk.SUNKEN)
        label.pack(pady=50)

        # Username Label and Entry
        self.username_label = tk.Label(self, text="Username:",bg="#1C1C24",fg="#FEFFFA", font=("Arial", 12))
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = tk.Label(self, text="Password:",bg="#1C1C24",fg="#FEFFFA",font=("Arial", 12))
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        login_button = tk.Button(self, text="Login", font=("Arial", 14),bg="#FE0104",fg="#FEFFFA", command=self.login)
        login_button.pack(pady=20)

        # Link to Sign Up page
        signup_button = tk.Button(self, text="Don't have an account? Sign Up", font=("Arial", 12),bg="#1C1C24",fg="#FEFFFA", command=self.go_to_signup_page)
        signup_button.pack(pady=100)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # result = login(username,password)
        # Example validation (replace with your logic)
        if username == "a" and password == "p":
            messagebox.showinfo("Login", "Login successful!")
            self.controller.show_page(HomePage)  # Go to the HomePage
        # elif(result):
        #     messagebox.showinfo("Loginnnnnnnn", "Login successful!")
        #     self.controller.show_page(HomePage)  # Go to the HomePage
        else:
            messagebox.showerror("Login", "Invalid username or password")

    def go_to_signup_page(self):
        self.controller.show_page(SignupPage)
    def OnShow(self):
        print('onShow loginn')
    


# Signup Page
class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.config(width=1240,height=700,padx=530,pady=30,bg='#1C1C24')
        self.controller = controller

        # Add title label
        label = tk.Label(self, text="Sign Up", font=("Arial", 20),bg="#151517",fg="#FEFFFA",bd=1,relief=tk.SUNKEN)
        label.pack(pady=50)

        # Username Label and Entry
        self.username_label = tk.Label(self, text="Username:", font=("Arial", 12),bg="#1C1C24",fg="#FEFFFA")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = tk.Label(self, text="Password:", font=("Arial", 12),bg="#1C1C24",fg="#FEFFFA")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        # Confirm Password Label and Entry
        self.confirm_password_label = tk.Label(self, text="Confirm Password:", font=("Arial", 12),bg="#1C1C24",fg="#FEFFFA")
        self.confirm_password_label.pack(pady=10)
        self.confirm_password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.confirm_password_entry.pack(pady=5)

        # Sign Up Button
        signup_button = tk.Button(self, text="Sign Up", font=("Arial", 14),bg="#FE0104",fg="#FEFFFA", command=self.signup)
        signup_button.pack(pady=20)

        # Link to Login page
        login_button = tk.Button(self, text="Already have an account? Login", font=("Arial", 12), command=self.go_to_login_page,bg="#151517",fg="#FEFFFA")
        login_button.pack(pady=100)

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
        print('before')
        result = signup(username,password)
        print('agter')
        if(result):
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
        self.config(width=1400,height=700,padx=5,bg='#1C1C24')

        self.columnconfigure(tuple(range(60)), weight=1)
        self.rowconfigure(tuple(range(30)), weight=1)
        print('initttttttttttt')
        self.songs = []
        self.playlists = []

        top_frame = tk.LabelFrame(self, bg='#1A1A20', bd=3, padx=2, relief=tk.SUNKEN,height=500)
        top_frame.grid(row=0,column=0,columnspan=4 ,sticky="news",pady=10)

        profile_button= tk.Button(top_frame, text="oooo",bg="#FEFFFA", command=self.profile_action,width=10)
        profile_button.grid(row=0,column=0,padx=20,sticky="news",pady=10)

        search_bar = tk.Entry(top_frame)
        search_bar.grid(row=0,column=1,padx=20,pady=10)

        plceholder_label = tk.Label(top_frame,text="",bg='#1A1A20')
        plceholder_label.grid(row=0,column=2,padx=400,pady=10)

        self.sosk_image_photo = PhotoImage(file="sk.PNG")
        # self.sosk_image_photo = self.sosk_image_photo.subsample(20, 20)
        sosk_image = tk.Label(top_frame, image=self.sosk_image_photo,bd=0)
        sosk_image.grid(row=0, column=3,pady=15)

        
        search_bar.insert(index=0,string="this dont work")
        
    def OnShow(self):

        self.songs.clear()
        self.playlists.clear()

        result = get_songs()
        print('ressssssult is : ',result)

        for i in result['hi']:
            self.songs.append(i)
        print('adssadsa ',self.songs)

        layout_frame = tk.Frame(self, bg='#131315')
        layout_frame.grid(row=1,column=0,columnspan=3,pady=20)
        array1 = list(range(40))  # First array for the first scrollable area
        array2 = list(range(50))  
        self.create_scrollable_area(layout_frame, array1, 0, action="Songs")
        self.create_scrollable_area(layout_frame, array2, 1, action="Playlist")  # Changed column_index to 1 for better layout


        # Add title label
        label = tk.Label(layout_frame, text="Welcome to the Music Player", font=("Arial", 20),bg="#151517",fg="#FEFFFA",bd=3)
        label.grid(row=0,column=0,columnspan=3,sticky=tk.E + tk.W)

        # Button to navigate to the Music Player page
        button = tk.Button(layout_frame, text="Go to Music Player",bg="#151517",fg="#FEFFFA", command=self.go_to_music_player)
        button.grid(row=1,column=0,pady=30)

        # Button to navigate to the Upload page
        upload_button = tk.Button(layout_frame, text="Upload Music",bg="#151517",fg="#FEFFFA", command=self.go_to_upload_page)
        upload_button.grid(row=1,column=1,pady=30)
        BOTTOM_frame = tk.LabelFrame(layout_frame,text="playing", bg="#22222C",fg="#FEFFFA",height=5,width=1240)
        BOTTOM_frame.grid(row=4,column=0,columnspan=3)
        stop_button = tk.Button(BOTTOM_frame, text="stop",bg="#151517",fg="#FEFFFA", command=self.go_to_music_player)
        stop_button.grid(row=0,column=2,padx=95,pady=10)
        play_button = tk.Button(BOTTOM_frame, text="play",bg="#151517",fg="#FEFFFA", command=self.go_to_upload_page)
        play_button.grid(row=0,column=1,padx=400,pady=10)
        cover_label = tk.Label(BOTTOM_frame,text="kh")
        cover_label.grid(row=0,column=0,padx=95,pady=10)
    
    def create_scrollable_area(self, layout_frame, array, column_index, action):
        scrollable_frame = tk.LabelFrame(layout_frame, text=action, bg='#151517', fg='#FEFFFA', border=10)  
        scrollable_frame.grid(row=2,column=column_index,pady=30,padx=30)  # Adjusted row index and padding

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
        add_button = tk.Button(scrollable_frame, text="+",command= self.create_new_playlist, padx=100, fg='#FEFFFA')
        add_button.configure(bg="#22222C")
        add_button.grid(row=1, column=1)
        for i in range(1,len(self.playlists)):
            button_text = f"playlists {array[i]}"
            button = tk.Button(scrollable_frame, text=button_text, command=lambda text=button_text: self.open_new_window(text), padx=100, fg='#FEFFFA')
            button.configure(bg="#22222C")
            number = tk.Label(scrollable_frame, text=f"{i}.", padx=5)
            number.grid(row=i, column=0)
            button.grid(row=i, column=1)

    def create_new_playlist(self):
        new_window = tk.Toplevel()
        new_window.title("helo")
        label = tk.Label(new_window, text="pick a name for your play list")
        label.grid(row = 0,column=0,padx=20, pady=20)
        entry = tk.Entry(new_window)
        entry.grid(row = 1,column=0,padx=20, pady=20)
        self.playlists.append(entry.get)
        submit = tk.Button(new_window,text="submit",command=quit)
        submit.grid(row=2,column=0,padx=20,pady=20)


    def create_songs(self, scrollable_frame, array):
        for i in range(len(self.songs)):
            print(f'i is {i} and {self.songs[i]}')
            button_text = f"song {self.songs[i]['title']}"
            button = tk.Button(scrollable_frame, text=button_text, command=lambda text=button_text: self.open_new_window(text), padx=100, fg='#FEFFFA', anchor="e")
            button.configure(bg="#22222C")
            add_button = tk.Button(scrollable_frame, text="+", padx=5, fg='#FEFFFA', anchor="e")
            add_button.configure(bg="#22222C")
            number = tk.Label(scrollable_frame, text=f"{i + 1}.", padx=5)
            number.grid(row=i, column=0)
            button.grid(row=i, column=1)                
            add_button.grid(row=i, column=1)   
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
        self.progress_scale = tk.Scale(self, from_=0, to=100, orient="horizontal", bg="#151517",fg="#FEFFFA",length=400, sliderlength=20)
        self.progress_scale.grid(row=2,column = 1,pady=10)
        # Bind to the release event
        self.progress_scale.bind("<ButtonRelease-1>", self.on_scale_release)
        self.progress_scale.bind("<Button-1>", self.on_scale_click)

        # Back to Home Button
        self.back_button = tk.Button(self, text="Back to Home", font=("Arial", 12),bg="#151517",fg="#FEFFFA", command=self.back_to_home)
        self.back_button.grid(row=4,column=1)
    def OnShow(self):
        print('onShow')
    
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
        self.config(width=1240,height=700,padx=450,bg='#1C1C24')
        self.controller = controller
        top_frame = tk.LabelFrame(self, bg='#151517', bd=3, padx=0, relief=tk.SUNKEN)
        top_frame.grid(row=0,column=0,columnspan=3,pady = 100 )
        label = tk.Label(top_frame, text="Upload Music to Server", font=("Arial", 20),bg="#151517",fg="#FEFFFA")
        label.grid(row=0,column=0,columnspan=2,sticky=tk.E + tk.W)
        button_frame = tk.LabelFrame(self, bg='#1C1C24', bd=3, padx=0, relief=tk.SUNKEN)
        button_frame.grid(row=1,column=0,columnspan=3,pady = 10 )

        # Button to upload music
        upload_button = tk.Button(button_frame, text="Select Music File",bg="#151517",fg="#FEFFFA", command=self.select_music_file)
        upload_button.grid(row=2,column =0,pady=20)

        # Label to show the selected file name
        self.selected_file_label = tk.Label(button_frame, text="No file selected",bg="#151517",fg="#FEFFFA", font=("Arial", 12))
        self.selected_file_label.grid(row=3,column =0,pady=20)

        # Button to upload the selected file
        upload_to_server_button = tk.Button(button_frame, text="Upload to Server", bg="#151517",fg="#FEFFFA",command=self.upload_file)
        upload_to_server_button.grid(row=4,column =0,pady=20)

        # Back to Home Button
        back_button = tk.Button(button_frame, text="Back to Home",bg="#151517",fg="#FEFFFA", command=self.back_to_home)
        back_button.grid(row=5,column =0,pady=20)

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
        self.title("sosk koshte shode")
        self.geometry("1280x720")
        self.config(bg="#1C1C24")

        # main_frame = tk.LabelFrame(self, bg='#1C1C24', bd=3, padx=0, relief=tk.SUNKEN)
        # main_frame.place(x= 0,y=0,width= 1235,height=700 )

        
        # top_frame = tk.LabelFrame(main_frame, bg='#1C1C24', bd=3, padx=0, relief=tk.SUNKEN)
        # top_frame.place(x= 0,y=0,width= 1235,height=150 )

        # layout_frame = tk.Frame(main_frame, bg='#131315')
        # layout_frame.pack(side=tk.RIGHT )
        
        # BOTTOM_frame = tk.LabelFrame(main_frame,text="khhhhhhhh", bg='red',width=1235,bd = 4,height=40)
        # BOTTOM_frame.place(x=0,y=655)



        # # Profile button
        # self.profile_button = tk.Button(top_frame, text="Profile")
        # self.profile_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Dictionary to store frames
        self.frames = {}

        # Create and store frames
        for F in (LoginPage,SignupPage, HomePage, MusicPlayerPage, UploadPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=1, column=0 ,sticky=tk.W+tk.E+tk.S+tk.N)

        # Show the login page initially
        self.show_page(LoginPage)

    def show_page(self, page_class):
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_forget()

        # Show the selected frame
        page_name = page_class.__name__
        frame = self.frames[page_name]
        frame.grid(row=0,column =0,sticky="nsew")
        if hasattr(frame, 'OnShow'):
            frame.OnShow()


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
