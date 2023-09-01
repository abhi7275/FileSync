import os
import shutil
import datetime
import hashlib
# Define a class for the file system node
class FileSystemNode:
    def __init__(self, name, is_folder=True):
        self.name = name  # Name of the node (folder or file)
        self.is_folder = is_folder  # Indicates whether it's a folder or file
        self.children = []  # List to store child nodes


# Define a function to build the file system tree
def build_file_system_tree(root_folder):
    # Create the root node representing the root folder
    root_node = FileSystemNode(root_folder, is_folder=True)

    # Traverse the file system under the root folder using os.walk
    for root, dirs, files in os.walk(root_folder):
        current_node = root_node  # Start from the root node
        relative_path = os.path.relpath(root, root_folder)  # Calculate relative path

        # Split relative path into folder names
        folders = relative_path.split(os.path.sep)

        # Iterate through each folder in the relative path
        for folder in folders:
            # Check if a child node with this name already exists
            child_node = next((child for child in current_node.children if child.name == folder), None)

            if child_node is None:
                # If it doesn't exist, create a new folder node
                child_node = FileSystemNode(folder, is_folder=True)
                current_node.children.append(child_node)  # Add it as a child

            current_node = child_node  # Move to the child node for the next iteration

        # Add file nodes as children of the current node
        for file in files:
            current_node.children.append(FileSystemNode(file, is_folder=False))

    return root_node  # Return the root node representing the entire file system tree


# Define a function to populate the treeview widget
def populate_treeview(node, parent):
    for child_node in node.children:
        if child_node.is_folder:
            child_id = parent.insert('', 'end', text=child_node.name)
            populate_treeview(child_node, child_id)
        else:
            parent.insert('', 'end', text=child_node.name)

# Define a function called organize_by_type that takes source_folder and destination_folder as arguments.
def organize_by_type(source_folder, destination_folder):
    # Check if the destination folder exists. If not, create it.
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

    # Iterate through the files in the source folder.
    for filename in os.listdir(source_folder):
        # Create the full path of the source file.
        source_path = os.path.join(source_folder, filename)

        # Check if the path represents a file (not a directory).
        if os.path.isfile(source_path):
            # Get the file extension (e.g., "txt" from "file.txt").
            file_extension = filename.split(".")[-1]

            # Create the full path for the destination folder based on the file extension.
            destination_path = os.path.join(destination_folder, file_extension)

            # If the destination folder for this file type doesn't exist, create it.
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)

            # Move the source file to the appropriate subfolder within the destination folder.
            shutil.move(source_path, os.path.join(destination_path, filename))


# Define a function to organize files by their creation date.
def organize_by_creation_date(source_folder, destination_folder):
    # Loop through the files in the source folder.
    for filename in os.listdir(source_folder):
        # Create the full path of the source file.
        source_path = os.path.join(source_folder, filename)

        # Check if the path represents a file (not a directory).
        if os.path.isfile(source_path):
            # Get the creation time of the file in seconds since the epoch.
            creation_time = os.path.getctime(source_path)

            # Convert the creation time to a datetime object.
            date = datetime.datetime.fromtimestamp(creation_time)

            # Extract the year and month from the datetime.
            year = date.year
            month = date.strftime("%B")  # Get the full month name

            # Create the full path for the destination folder based on the year and month.
            destination_path = os.path.join(destination_folder, str(year), month)

            # Create the destination folder if it doesn't exist.
            os.makedirs(destination_path, exist_ok=True)

            # Construct the new filename, which is just the original filename.
            new_filename = filename

            # Create the full path for the destination file.
            destination_file_path = os.path.join(destination_path, new_filename)

            # Move the source file to the appropriate subfolder within the destination folder.
            shutil.move(source_path, destination_file_path)


# Define a function to organize files by their modification date.
def organize_by_modification_date(source_folder, destination_folder):
    # Loop through the files in the source folder.
    for filename in os.listdir(source_folder):
        # Create the full path of the source file.
        source_path = os.path.join(source_folder, filename)

        # Check if the path represents a file (not a directory).
        if os.path.isfile(source_path):
            # Get the modification time of the file in seconds since the epoch.
            modification_time = os.path.getmtime(source_path)

            # Convert the modification time to a datetime object.
            date = datetime.datetime.fromtimestamp(modification_time)

            # Extract the year and month from the datetime.
            year = date.year
            month = date.strftime("%B")

            # Create the full path for the destination folder based on the year and month.
            destination_path = os.path.join(destination_folder, str(year), month)

            # Create the destination folder if it doesn't exist.
            os.makedirs(destination_path, exist_ok=True)

            # Move the source file to the appropriate subfolder within the destination folder.
            shutil.move(source_path, os.path.join(destination_path, filename))


def identify_duplicates(source_folder, destination_folder):
    # Create a dictionary to store file hashes and their corresponding paths
    file_hashes = {}

    for root, _, files in os.walk(source_folder):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Calculate the MD5 hash of the file
            hasher = hashlib.md5()
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(65536)  # Read in 64k chunks
                    if not data:
                        break
                    hasher.update(data)
            file_hash = hasher.hexdigest()

            # Check if the hash is already in the dictionary (indicating a duplicate)
            if file_hash in file_hashes:
                # Move the duplicate file to the destination folder with a new name
                new_filename = f'duplicate_{filename}'
                destination_path = os.path.join(destination_folder, new_filename)
                os.rename(file_path, destination_path)
            else:
                # Add the hash and file path to the dictionary
                file_hashes[file_hash] = file_path
