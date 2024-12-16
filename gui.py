import sys
import pygame
# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize pygame mixer for audio handling
        pygame.mixer.init()

        # Set up the GUI
        self.setWindowTitle("Simple Music Player")
        self.setGeometry(300, 300, 300, 150)

        self.layout = QVBoxLayout()

        # Label to display current track
        self.track_label = QLabel("No track selected", self)
        self.layout.addWidget(self.track_label)

        # Play button
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_music)
        self.layout.addWidget(self.play_button)

        # Pause button
        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause_music)
        self.layout.addWidget(self.pause_button)

        # Stop button
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_music)
        self.layout.addWidget(self.stop_button)

        # Select file button
        self.select_file_button = QPushButton("Select Music File", self)
        self.select_file_button.clicked.connect(self.select_music_file)
        self.layout.addWidget(self.select_file_button)

        self.setLayout(self.layout)

        self.music_file = None

    def play_music(self):
        """ Play the selected music file """
        if self.music_file:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(loops=0, start=0.0)
            self.track_label.setText(f"Playing: {self.music_file}")
        else:
            self.track_label.setText("No track selected")

    def pause_music(self):
        """ Pause the music playback """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.track_label.setText("Music paused")

    def stop_music(self):
        """ Stop the music playback """
        pygame.mixer.music.stop()
        self.track_label.setText("Music stopped")

    def select_music_file(self):
        """ Open a file dialog to select a music file """
        options = QFileDialog.Option()
        file, _ = QFileDialog.getOpenFileName(self, "Open Music File", "", "MP3 Files (*.mp3);;All Files (*)", options=options)
        if file:
            self.music_file = file
            self.track_label.setText(f"Selected: {self.music_file}")

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
