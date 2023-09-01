import tkinter as tk
import gui  # Import the GUI module
from gui import  FileOrganizerGUI
if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.title("File Organizer")
    root.mainloop()
