#!/usr/bin/env python

import os
import getpass
import rumps
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import mimetypes

class MyHandler(FileSystemEventHandler):
    def __init__(self, special_extensions):
        super(MyHandler, self).__init__()
        self.special_extensions = special_extensions

    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            src = os.path.join(folder_to_track, filename)
            file_type = mimetypes.guess_type(filename)[0]
            if file_type:
                file_type = file_type.split('/')[0]
            else:
                file_type = 'Other'
            if file_type in self.special_extensions or filename.split('.')[-1].lower() in self.special_extensions:
                if filename.lower().endswith('.txt'):
                    file_type = 'text'
                    subfolder = 'txt'
                new_destination = os.path.join(folder_destination, file_type, subfolder)
                os.makedirs(new_destination, exist_ok=True)
                new_file_path = os.path.join(new_destination, filename)
                os.rename(src, new_file_path)
            else:
                new_destination = os.path.join(folder_destination, 'Other')
                os.makedirs(new_destination, exist_ok=True)
                new_file_path = os.path.join(new_destination, filename)
                os.rename(src, new_file_path)

class OrganizerApp(rumps.App):
    def __init__(self, folder_to_track, folder_destination, special_extensions_file):
        super(OrganizerApp, self).__init__("Organizer", icon=os.path.join(os.path.dirname(os.path.abspath(__file__)), "layers.png"))
        self.folder_to_track = folder_to_track
        self.folder_destination = folder_destination
        self.special_extensions_file = special_extensions_file
        self.monitoring_active = False
        self.observer = None
        self.special_extensions = self.read_special_extensions()

    def read_special_extensions(self):
        with open(self.special_extensions_file, 'r') as file:
            special_extensions = [line.strip().lower() for line in file]
        return special_extensions

    @rumps.clicked("Start")
    def start_monitoring(self, _):
        if not self.observer:
            self.special_extensions = self.read_special_extensions()
            self.observer = Observer()
            event_handler = MyHandler(self.special_extensions)
            self.observer.schedule(event_handler, self.folder_to_track, recursive=True)
            self.observer.start()
            rumps.notification("Organizer", "Monitoring Started", "Monitoring of the download folder has been started.")
            self.monitoring_active = True
        else:
            rumps.notification("Organizer", "Error", "Monitoring is already active.")

    @rumps.clicked("Stop")
    def stop_monitoring(self, _):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            rumps.notification("Organizer", "Monitoring Stopped", "Monitoring of the download folder has been stopped.")
            self.monitoring_active = False
        else:
            rumps.notification("Organizer", "Error", "Monitoring is not active.")

    @rumps.clicked("Edit List")
    def edit_special_extensions(self, _):
        subprocess.run(['open', self.special_extensions_file])

if __name__ == "__main__":
    user = getpass.getuser()
    folder_to_track = '/Users/' + user + '/Downloads'
    folder_destination = '/Users/' + user + '/organized_files'
    special_extensions_file = 'special_extensions.txt'
    app = OrganizerApp(folder_to_track, folder_destination, special_extensions_file)
    app.run()
