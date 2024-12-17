from tkinter import *
from tkinter import messagebox

class ScrollBar:
    # constructor
    def __init__(self, root, main_frame, array1, array2):
        # create root window
        self.root = root
        self.root.geometry("1280x720")  # Fix the window size
        photo = PhotoImage(file="img\\sk.PNG")
        photo = photo.subsample(15, 15)

        top_frame = LabelFrame(main_frame, bg='#1C1C24', bd=3, padx=0, relief=SUNKEN)
        top_frame.place(x= 0,y=0,width= 1235,height=150 )

        layout_frame = Frame(main_frame, bg='#131315')
        layout_frame.pack(side=RIGHT )
        
        BOTTOM_frame = LabelFrame(main_frame,text="khhhhhhhh", bg='red',width=1235,bd = 4,height=40)
        BOTTOM_frame.place(x=0,y=655)



        # Profile button
        self.profile_button = Button(top_frame, text="Profile", command=self.profile_action)
        self.profile_button.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        search = Entry(top_frame, width=20)
        search.grid(row=0, column=1, padx=10)

        # SOSK label
        sosk = Label(root, image=photo, compound="top", bd=0)
        sosk.place(x=1090, y=20)  # Adjusting x position to fit within 1280 width

        # Create scrollable areas
        self.create_scrollable_area(layout_frame, array1, 0, action="Songs")
        self.create_scrollable_area(layout_frame, array2, 1, action="Playlist")  # Changed column_index to 1 for better layout

        # Start the main loop
        self.root.mainloop()

    def create_scrollable_area(self, layout_frame, array, column_index, action):
        scrollable_frame = LabelFrame(layout_frame, text=action, bg='#151517', fg='#FEFFFA', border=10)  
        scrollable_frame.grid(row=0,column=column_index)  # Adjusted row index and padding

        # Create a vertical scrollbar
        v = Scrollbar(scrollable_frame)
        v.pack(side='right', fill='y')

        # Create a canvas to hold the scrollable frame
        canvas = Canvas(scrollable_frame, bg='#151517')
        canvas.pack(side='left', fill='both', expand=True)

        # Attach the vertical scrollbar to the canvas
        v.config(command=canvas.yview)
        canvas.config(yscrollcommand=v.set)

        # Create a scrollable frame in the canvas
        scrollable_internal_frame = Frame(canvas, bg='#151517')
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
            button = Button(scrollable_frame, text=button_text, command=lambda text=button_text: self.open_new_window(text), padx=100, fg='#FEFFFA')
            button.configure(bg="#22222C")
            number = Label(scrollable_frame, text=f"{i + 1}.", padx=5)
            number.grid(row=i, column=0)
            button.grid(row=i, column=1)

    def create_songs(self, scrollable_frame, array):
        for i in range(len(array)):
            button_text = f"song {array[i]}"
            button = Button(scrollable_frame, text=button_text, command=lambda text=button_text: self.open_new_window(text), padx=100, fg='#FEFFFA', anchor="e")
            button.configure(bg="#22222C")
            number = Label(scrollable_frame, text=f"{i + 1}.", padx=5)
            number.grid(row=i, column=0)
            button.grid(row=i, column=1)

    def open_new_window(self, button_name):
        new_window = Toplevel()
        new_window.title(button_name)
        label = Label(new_window, text=f"You clicked {button_name}!")
        label.pack(padx=20, pady=20)

    def profile_action(self):
        messagebox.showinfo("Profile", "Profile button clicked!")

# create an object to ScrollBar class
root = Tk()
array1 = list(range(40))  # First array for the first scrollable area
array2 = list(range(50))  # Second array for the second scrollable area
root.title("Main Window")
root.configure(bg='#1C1C24')  # Set the background color
main_frame = LabelFrame(root, bg='#151517')
main_frame.place(x=10,y=10,width=1240,height= 700 )
s = ScrollBar(root, main_frame, array1, array2)
