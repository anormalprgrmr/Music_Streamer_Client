from tkinter import *
from tkinter import messagebox

class ScrollBar:

    # constructor
    def __init__(self, root, layout_frame, array1, array2):
        # create root window
        self.root = root

        # Create a profile button at the top left
        self.profile_button = Button(self.root, text="Profile", command=self.profile_action)
        self.profile_button.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Create the first scrollable area
        self.create_scrollable_area(layout_frame, array1, 0,action="song")
        
        # Create the second scrollable area
        self.create_scrollable_area(layout_frame, array2, 1,action= "playlist")

        # Configure grid weights for resizing
        layout_frame.grid_rowconfigure(0, weight=1)
        layout_frame.grid_columnconfigure(0, weight=1)  # Allow the left column to expand
        layout_frame.grid_columnconfigure(1, weight=0)  # Fixed width for the right column

        # Start the main loop
        self.root.mainloop()

    def create_scrollable_area(self, layout_frame, array, column_index,action):
        # Create a Frame widget to hold the scrollable area
        scrollable_frame = Frame(layout_frame, bg='gray', width=460, height=300)  # Fixed width for scrollable area
        scrollable_frame.grid(row=0, column=column_index, sticky='ns', padx=10, pady=10)  # Place on the right side

        # Create a vertical scrollbar
        v = Scrollbar(scrollable_frame)
        v.pack(side='right', fill='y')

        # Create a canvas to hold the scrollable frame
        canvas = Canvas(scrollable_frame, bg='Red')
        canvas.pack(side='left', fill='both', expand=True)

        # Attach the vertical scrollbar to the canvas
        v.config(command=canvas.yview)
        canvas.config(yscrollcommand=v.set)

        # Create a scrollable frame in the canvas
        scrollable_internal_frame = Frame(canvas, bg='white')
        canvas.create_window((0, 0), window=scrollable_internal_frame, anchor="nw")

        # Configure the scrollable frame to update the scroll region
        scrollable_internal_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        if(action == "song"):
            self.create_songs(scrollable_internal_frame, array)
        else:

            # Create buttons in the scrollable frame
            self.create_playlists(scrollable_internal_frame, array)

    def create_playlists(self, scrollable_frame, array):
        # Create buttons in the scrollable frame
        for i in range(len(array)):
            button_text = f"playlist {array[i]}"
            button = Button(scrollable_frame, text=button_text, command=lambda text=button_text: self.open_new_window(text), padx=100)
            number = Label(scrollable_frame, text=f"{i + 1}.", padx=50)
            number.grid(row=i, column=0)
            button.grid(row=i, column=1)
    def create_songs(self, scrollable_frame, array):
        # Create buttons in the scrollable frame
        for i in range(len(array)):
            button_text = f"song {array[i]}"
            button = Button(scrollable_frame, text=button_text, command=lambda text=button_text: self.open_new_window(text), padx=100)
            number = Label(scrollable_frame, text=f"{i + 1}.", padx=50)
            number.grid(row=i, column=0)
            button.grid(row=i, column=1)

    def open_new_window(self, button_name):
        # Create a new window with the name of the button
        new_window = Toplevel()
        new_window.title(button_name)
        label = Label(new_window, text=f"You clicked {button_name}!")
        label.pack(padx=20, pady=20)

    def profile_action(self):
        # Action for profile button
        messagebox.showinfo("Profile", "Profile button clicked!")

# create an object to ScrollBar class
root = Tk()
array1 = list(range(40))  # First array for the first scrollable area
array2 = list(range(50))  # Second array for the second scrollable area
root.title("Main Window")
root.geometry("920x600")  # Set the window size to 920x600
root.configure(bg='gray')  # Set the background color to gray
layout_frame = Frame(root, bg='gray')
layout_frame.grid(row=1, column=0, sticky='nsew')
s = ScrollBar(root, layout_frame, array1, array2)
