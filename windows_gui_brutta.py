import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import mimetypes
from tkinter import ttk

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
            file_type = file_type.split('/')[0] if file_type else 'Other'
            extension = extension.split('.')[-1].lower() if extension else 'Other'

            if file_type in self.special_extensions or extension in self.special_extensions:
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

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizer")
        self.geometry("700x180") 
        self.configure(bg="#f2f2f2")
        self.iconbitmap('layers.ico')

        style = ttk.Style()
        style.configure("TButton", padding=10, width=20, background="#4CAF50", foreground="white")
        style.configure("TLabel", background="#f2f2f2", foreground="#333333", font=('Helvetica', 12, 'bold'))
        style.configure("TEntry", fieldbackground="#ffffff", font=('Helvetica', 11))

        self.track_label = ttk.Label(self, text="Cartella da monitorare:")
        self.track_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.track_entry = ttk.Entry(self)
        self.track_entry.grid(row=0, column=1, pady=10, sticky="ew")
        self.track_button = ttk.Button(self, text="Sfoglia", command=self.browse_track_folder)
        self.track_button.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        self.dest_label = ttk.Label(self, text="Cartella organizzata:")
        self.dest_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.dest_entry = ttk.Entry(self)
        self.dest_entry.grid(row=1, column=1, pady=10, sticky="ew")
        self.dest_button = ttk.Button(self, text="Sfoglia", command=self.browse_destination_folder)
        self.dest_button.grid(row=1, column=2, pady=10, padx=10, sticky="w")

        self.empty_label = ttk.Label(self, text="")
        self.empty_label.grid(row=0, column=3, rowspan=2, padx=10, sticky="ew")

        self.start_button = ttk.Button(self, text="Avvia", command=self.start_organizer)
        self.start_button.grid(row=0, column=4, rowspan=2, pady=20, padx=10, sticky="e")

        self.info_label = tk.Label(self, text="Premi 'Avvia' per iniziare l'organizzazione dei file.", font=('Helvetica', 10))
        self.info_label.grid(row=2, column=0, columnspan=5, pady=10, padx=10, sticky="w")

    def browse_track_folder(self):
        self.folder_to_track = filedialog.askdirectory()
        self.track_entry.delete(0, tk.END)
        self.track_entry.insert(0, self.folder_to_track)

    def browse_destination_folder(self):
        self.folder_destination = filedialog.askdirectory()
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.insert(0, self.folder_destination)

    def start_organizer(self):
        if os.path.isdir(self.folder_to_track) and os.path.isdir(self.folder_destination):
            event_handler = MyHandler(self.folder_to_track, self.folder_destination, ['.txt'])
            observer = Observer()
            observer.schedule(event_handler, self.folder_to_track, recursive=True)
            observer.start()
            messagebox.showinfo("Organizer", "Organizer è attivo e sta monitorando la cartella.")
            self.protocol("WM_DELETE_WINDOW", lambda: self.stop_observer(observer))
        else:
            messagebox.showerror("Errore", "Cartelle non valide. Seleziona cartelle valide.")

    def stop_observer(self, observer):
        observer.stop()
        observer.join()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()


