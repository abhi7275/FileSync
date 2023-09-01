import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import organizer  # Import the algorithmic module

# Create a class to manage the GUI
class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        # Initialize the selected_option variable
        self.selected_option = tk.StringVar(value="by_type")

        # Create labels, buttons, and radio buttons
        self.source_label = tk.Label(root, text="Source Folder:")
        self.destination_label = tk.Label(root, text="Destination Folder:")

        self.source_entry = tk.Entry(root)
        self.destination_entry = tk.Entry(root)

        self.source_browse_button = tk.Button(root, text="Browse", command=self.browse_source_folder)
        self.destination_browse_button = tk.Button(root, text="Browse", command=self.browse_destination_folder)

        self.sort_by_type_radio = tk.Radiobutton(root, text="By Type", variable=self.selected_option, value="by_type")
        self.sort_by_creation_date_radio = tk.Radiobutton(root, text="By Creation Date", variable=self.selected_option,
                                                          value="by_creation_date")
        self.sort_by_modification_date_radio = tk.Radiobutton(root, text="By Modification Date",
                                                              variable=self.selected_option,
                                                              value="by_modification_date")
        self.duplicate_handling_radio = tk.Radiobutton(root, text="Duplicate File Handling",
                                                       variable=self.selected_option, value="duplicate_handling")

        self.organize_button = tk.Button(root, text="Organize Files", command=self.organize_files)
        # Create a treeview widget for the file system hierarchy
        self.file_tree = ttk.Treeview(root)
        self.file_tree.heading('#0', text='File System')

        # Place widgets in the grid layout
        self.setup_layout()

    def setup_layout(self):
        self.source_label.grid(row=0, column=0)
        self.source_entry.grid(row=0, column=1)
        self.source_browse_button.grid(row=0, column=2)
        self.destination_label.grid(row=1, column=0)
        self.destination_entry.grid(row=1, column=1)
        self.destination_browse_button.grid(row=1, column=2)

        # Add radio buttons to the layout
        self.sort_by_type_radio.grid(row=2, column=0, sticky=tk.W)
        self.sort_by_creation_date_radio.grid(row=2, column=1, sticky=tk.W)
        self.sort_by_modification_date_radio.grid(row=3, column=0, sticky=tk.W)
        self.duplicate_handling_radio.grid(row=3, column=1, sticky=tk.W)

        self.organize_button.grid(row=4, columnspan=3)
        self.file_tree.grid(row=5, columnspan=3)

    def browse_source_folder(self):
        source_folder = filedialog.askdirectory()
        if source_folder:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, source_folder)
            self.update_file_tree(source_folder)  # Update the file system tree

    def browse_destination_folder(self):
        destination_folder = filedialog.askdirectory()
        if destination_folder:
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, destination_folder)

    def organize_files(self):
        source_folder = self.source_entry.get()
        destination_folder = self.destination_entry.get()
        selected_option = self.selected_option.get()  # Get the selected option

        if selected_option == "by_type":
            organizer.organize_by_type(source_folder, destination_folder)
        elif selected_option == "by_creation_date":
            organizer.organize_by_creation_date(source_folder, destination_folder)
        elif selected_option == "by_modification_date":
            organizer.organize_by_modification_date(source_folder, destination_folder)
        elif selected_option == "duplicate_handling":
            organizer.identify_duplicates(source_folder, destination_folder)


    def update_file_tree(self, root_folder):
        self.file_tree.delete(*self.file_tree.get_children())  # Clear the existing tree

        # Define a helper function to populate the treeview recursively
        def populate_treeview(node, parent=""):
            for child_node in node.children:
                if child_node.is_folder:
                    child_id = self.file_tree.insert(parent, 'end', text=child_node.name)
                    populate_treeview(child_node, parent=child_id)
                else:
                    self.file_tree.insert(parent, 'end', text=child_node.name)

        root_node = organizer.build_file_system_tree(root_folder)  # Build the file system tree
        populate_treeview(root_node)

    def get_selected_option(self):
        # You can add code to determine the selected option based on radio buttons here
        # For now, return a placeholder value
        return "by_type"
