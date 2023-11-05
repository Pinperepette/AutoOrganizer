#!/usr/bin/env python
import os
import sys
import mimetypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self, folder_to_track, folder_destination, special_extensions):
        super(MyHandler, self).__init__()
        self.folder_to_track = folder_to_track
        self.folder_destination = folder_destination
        self.special_extensions = special_extensions

    def on_modified(self, event):
        for filename in os.listdir(self.folder_to_track):
            src = os.path.join(self.folder_to_track, filename)
            file_type, extension = mimetypes.guess_type(filename)
            tipo = mimetypes.guess_type(filename)
            file_type = file_type.split('/')[0] if file_type else 'Other'
            extension = extension.split('.')[-1].lower() if extension else 'Other'
            if tipo[0] != None:
                local_var = str(tipo[0])
                new_destination = os.path.join(self.folder_destination, local_var, filename)
                if not os.path.exists(os.path.join(self.folder_destination, local_var)):
                    os.makedirs(os.path.join(self.folder_destination, local_var))
                os.rename(src, new_destination)
            elif file_type in self.special_extensions or extension in self.special_extensions:
                if extension == 'txt':
                    file_type = 'text'
                    subfolder = 'txt'
                else:
                    subfolder = extension
                new_destination = os.path.join(self.folder_destination, file_type, subfolder)
                os.makedirs(new_destination, exist_ok=True)
                new_file_path = os.path.join(new_destination, filename)
                os.rename(src, new_file_path)
            else:
                new_destination = os.path.join(self.folder_destination, 'Other')
                os.makedirs(new_destination, exist_ok=True)
                new_file_path = os.path.join(new_destination, filename)
                os.rename(src, new_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <folder_to_track> <folder_destination> <special_extensions_file>")
        sys.exit(1)

    folder_to_track = sys.argv[1]
    folder_destination = sys.argv[2]
    special_extensions_file = sys.argv[3]

    with open(special_extensions_file, 'r') as file:
        special_extensions = [line.strip().lower() for line in file]

    event_handler = MyHandler(folder_to_track, folder_destination, special_extensions)
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()