import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame # type: ignore
import os
from tkinter import messagebox

class MusicPlayer:

    def __init__(self, root):
        self.root = root

        self.root.title("DataFlair - Music Player")

        self.root.geometry("800x450")
        self.root.resizable(False, False)

        self.bg_image =  tk.PhotoImage(file = os.path.join(os.getcwd(), "MusicPlayer/music", "bg_con.png"))
        self.bg_label = ttk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relx=0, rely=-0, relwidth=1, relheight=1)
       
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('.', background='black', foreground='black')
        s.configure('TFrame', background='white', foreground='white')
        s.configure('TButton', font=('Times New Roman', 12), background='White', foreground='black', 
                                            activebackground='brown', activeforeground='white')
        s.configure('TLabel', font=('Times New Roman', 12), background='white', foreground='black')
        s.configure('TScale', background='white')

        pygame.init()

        pygame.mixer.init()

        self.playlist_frame = tk.Frame(self.root)
        self.playlist_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.playlist = tk.Listbox(self.playlist_frame, width=40, height=20)
        self.playlist.pack(fill=tk.BOTH, expand=True)
        self.playlist.bind("<<ListboxSelect>>", self.play_selected)

        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10)
        self.control_frame.configure(border=1, relief="groove", borderwidth=2)
      
        self.bg_image3 =  tk.PhotoImage(file = os.path.join(os.getcwd(), "MusicPlayer/music", "control_bg.png"))
        self.bg_label3 = ttk.Label(self.control_frame, image=self.bg_image3)
        self.bg_label3.place(relx=0, rely=-0, relwidth=1, relheight=1)

        self.play_var = tk.StringVar()
        self.play_var.set("Play")
        self.play_pause_button = ttk.Button(self.control_frame, textvariable=self.play_var, command=self.play_pause)
        self.play_pause_button.grid(row=1, column=0, padx=10, pady=10)

        self.skip_backward_button = ttk.Button(self.control_frame, text="⏪", command=self.skip_backward)
        self.skip_backward_button.grid(row=2, column=0, padx=10, pady=10)
        
        self.skip_forward_button = ttk.Button(self.control_frame, text="⏩", command=self.skip_forward)
        self.skip_forward_button.grid(row=3, column=0, padx=10, pady=10)

        self.status_var = tk.StringVar()
        self.status_var.set("Volume Control")
        self.status_label = ttk.Label(self.control_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, padx=10, pady=10)

        self.volume_var = tk.DoubleVar()
        self.volume_scale = ttk.Scale(self.control_frame, orient="horizontal", from_=0, to=1, 
                                                variable=self.volume_var, command=self.set_volume)
        self.volume_scale.grid(row=5, column=0, padx=10, pady=10)

        self.import_button = ttk.Button(self.control_frame, text="Import Music", command=self.import_music)
        self.import_button.grid(row=6, column=0, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(self.control_frame, orient="horizontal", length=325, mode="determinate")
        self.progress_bar.grid(row=7, column=0, padx=10, pady=10)

        self.elapsed_time = ttk.Label(self.control_frame, text="00:00")
        self.elapsed_time.grid(row=8, column=0, padx=10, pady=10)

        self.current_song = ""

        self.paused = False

    def play_selected(self, event):
        selected_song = self.playlist.get(self.playlist.curselection())
        self.current_song = selected_song
        pygame.mixer.music.load(self.current_song)
        self.status_var.set("Now Playing: " + os.path.basename(self.current_song)[0:40]+"...")
        self.progress_bar["maximum"] = pygame.mixer.Sound(self.current_song).get_length()
        self.update_progressbar()
        pygame.mixer.music.play()
        self.play_var.set("Pause")

    def play_pause(self):
     
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.play_var.set("Pause")
        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.play_var.set("Play")

    def skip_backward(self):
        
        selection = self.playlist.curselection()
        if selection:
            prev_song_index = int(selection[0]) - 1
            if prev_song_index >= 0:
                prev_song = self.playlist.get(prev_song_index)
                self.current_song = prev_song
                pygame.mixer.music.load(self.current_song)
                self.status_var.set("Now Playing: " + os.path.basename(self.current_song)[0:40]+"...")
                pygame.mixer.music.play()
                self.play_var.set("Pause")
            else:
                messagebox.showwarning("Warning", "This is the first song.")
        else:
            messagebox.showerror("Error", "No song is selected.")

    def skip_forward(self):
     
        selection = self.playlist.curselection()
        if selection:
            next_song_index = int(selection[0]) + 1
            if next_song_index < self.playlist.size():
                next_song = self.playlist.get(next_song_index)
                self.current_song = next_song
                pygame.mixer.music.load(self.current_song)
                self.status_var.set("Now Playing: " + os.path.basename(self.current_song)[0:40]+"...")
                pygame.mixer.music.play()
                self.play_var.set("Pause")
            else:
                messagebox.showwarning("Warning", "This is the last song.")

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

    def import_music(self):
        
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:  
            if file_path not in self.playlist.get(0, tk.END):
                self.playlist.insert(tk.END, file_path)

    def update_progressbar(self):
        current_time = pygame.mixer.music.get_pos() / 1000
        self.progress_bar["value"] = current_time
        minutes, seconds = divmod(int(current_time), 60)
        self.elapsed_time.config(text="{:02d}:{:02d}".format(minutes, seconds))
        self.root.after(1000, self.update_progressbar)

root = tk.Tk()
MusicPlayer(root)
root.mainloop()
