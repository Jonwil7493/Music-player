import tkinter as tk
from tkinter import ttk
import os
import sounddevice as sd
import soundfile as sf
from tkinter import filedialog

# Define mood categories and recommendations || Backend
mood_categories = ["Happiness", "Sadness", "Anger", "Fear", "Love"]

recommendations = {
    "Happiness": ["upbeat", "pop", "dance", "cheerful", "party"],
    "Sadness": ["sad", "emotional", "slow", "melancholy", "heartbreak"],
    "Anger": ["rock", "metal", "aggressive", "intense"],
    "Fear": ["ambient", "dark", "ominous", "suspenseful", "anxiety"],
    "Love": ["romantic", "ballad", "passionate", "sentimental"]
}

# Define songs for each genre
songs = {
    "upbeat": ["Song 1", "Song 2", "Song 3"],
    "pop": ["Song 4", "Song 5", "Song 6"],
    "dance": ["Song 7", "Song 8", "Song 9"],
    "cheerful": ["Song 10", "Song 11", "Song 12"],
    "party": ["Song 13", "Song 14", "Song 15"],
    # Define songs for other genres similarly
}

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        # Initialize Tkinter variables
        self.selected_mood = tk.StringVar()
        self.selected_mood.set(mood_categories[0])

        # Initialize recommended genres
        self.recommended_genres = []

        # Initialize songs list
        self.songs_list = []

        # Initialize currently playing song
        self.current_stream = None  # Initialize current_stream

        # Create GUI elements
        self.create_gui()

    def create_gui(self):
        # Frame for mood selection
        mood_frame = ttk.Frame(self.root)
        mood_frame.pack(padx=10, pady=10)

        # Label for mood selection
        mood_label = ttk.Label(mood_frame, text="Select your mood:")
        mood_label.grid(row=0, column=0, padx=5)

        # Dropdown for mood selection
        mood_dropdown = ttk.Combobox(mood_frame, textvariable=self.selected_mood, values=mood_categories)
        mood_dropdown.grid(row=0, column=1, padx=5)

        # Button to detect mood
        detect_mood_button = ttk.Button(mood_frame, text="Detect Mood", command=self.detect_mood)
        detect_mood_button.grid(row=0, column=2, padx=5)

        # Frame for recommended genres
        genres_frame = ttk.Frame(self.root)
        genres_frame.pack(padx=10, pady=10)

        # Label for recommended genres
        genres_label = ttk.Label(genres_frame, text="Recommended Genres:")
        genres_label.grid(row=0, column=0, padx=5)

        # Listbox for recommended genres (only one selection allowed)
        self.genres_listbox = tk.Listbox(genres_frame, selectmode=tk.SINGLE, width=30, height=5)
        self.genres_listbox.grid(row=1, column=0, padx=5)

        # Button to apply recommendations
        apply_recommendations_button = ttk.Button(genres_frame, text="Apply Recommendations", command=self.apply_recommendations)
        apply_recommendations_button.grid(row=2, column=0, padx=5, pady=5)

        # Frame for song selection
        songs_frame = ttk.Frame(self.root)
        songs_frame.pack(padx=10, pady=10)

        # Label for song selection
        songs_label = ttk.Label(songs_frame, text="Select a song:")
        songs_label.grid(row=0, column=0, padx=5)

        # Listbox for displaying songs
        self.songs_listbox = tk.Listbox(songs_frame, selectmode=tk.SINGLE, width=30, height=5)
        self.songs_listbox.grid(row=1, column=0, padx=5)

        # Buttons for playback controls
        play_button = ttk.Button(songs_frame, text="Play", command=self.play_song)
        play_button.grid(row=2, column=0, padx=5)

        pause_button = ttk.Button(songs_frame, text="Pause", command=self.pause_song)
        pause_button.grid(row=2, column=1, padx=5)

        stop_button = ttk.Button(songs_frame, text="Stop", command=self.stop_song)
        stop_button.grid(row=2, column=2, padx=5)

        # Button to search for songs
        search_button = ttk.Button(songs_frame, text="Search Songs", command=self.search_songs)
        search_button.grid(row=3, column=0, columnspan=3, pady=5)

    def detect_mood(self):
        selected_mood = self.selected_mood.get()
        self.recommended_genres = recommendations.get(selected_mood, ["generic"])
        self.update_genres_listbox()

    def update_genres_listbox(self):
        self.genres_listbox.delete(0, tk.END)
        for genre in self.recommended_genres:
            self.genres_listbox.insert(tk.END, genre)

    def apply_recommendations(self):
        selected_genre_index = self.genres_listbox.curselection()
        if selected_genre_index:
            selected_genre = self.genres_listbox.get(selected_genre_index[0])
            self.songs_list = songs.get(selected_genre, [])
            self.update_songs_listbox()

    def update_songs_listbox(self):
        self.songs_listbox.delete(0, tk.END)
        for song in self.songs_list:
            self.songs_listbox.insert(tk.END, song)

    def search_songs(self):
        directory = filedialog.askdirectory()
        if directory:
            self.songs_list = self.find_audio_files(directory)
            self.update_songs_listbox()

    def find_audio_files(self, directory):
        audio_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith((".mp3", ".wav")):
                    audio_files.append(os.path.join(root, file))
        return audio_files

    def play_song(self):
        selected_song_index = self.songs_listbox.curselection()
        if selected_song_index:
            selected_song = self.songs_listbox.get(selected_song_index[0])
            self.play_audio(selected_song)

    def play_audio(self, filename):
        if self.current_stream:
            self.current_stream.stop()
            data, fs = sf.read(filename, dtype='float32')
        self.current_stream = sd.play(data, fs)

    def pause_song(self):
        if self.current_stream:
            sd.stop()

    def stop_song(self):
        if self.current_stream:
            sd.stop()

def main():
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

