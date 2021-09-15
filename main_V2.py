# Audio Visualizer Version 2 by Nolan Lowhorn
# Credit to Avi Rzayev
# 5/11/2021

import tkinter as tk
import pygame
import shutil
import numpy as np
import librosa
from pygame.locals import QUIT
from tkinter import filedialog

# Opens pygame window
def pygame_window():

    # Audio bars
    class Bars():

        def __init__(self, x, y, frequency, width, height):

            self.x = x
            self.y = y
            self.frequency = frequency
            self.width = width
            self.height = height

        # Updates height of bar
        def update(self, amplitude):

            self.height = amplitude*3

        # Draws bar
        def draw(self):

            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y - self.height, self.width, self.height))

    # Screen size
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 800

    # Processing audio
    time_series, sample_rate = librosa.load("file.wav")

    # Amplitude array
    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

    # Frequency array
    frequencies = librosa.core.fft_frequencies(n_fft=2048*4)

    # Array of time
    times = librosa.core.frames_to_time(np.arange(stft.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

    # Ratios of time and frequency
    time_index_ratio = len(times)/times[len(times) - 1]
    frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies) - 1]

    # Gets amplitude of frequency
    def get_amplitude(frequency, target_time):
        return stft[int(frequency * frequencies_index_ratio)][int(target_time * time_index_ratio)]

    # Creates the bars list
    bars = []
    bar_x = 0
    frequencies = np.arange(100, 3000, 100)

    # Creates the bars for each frequency
    for f in frequencies:
        bar_x += 25
        bars.append(Bars(bar_x, SCREEN_HEIGHT, f, 15, 100))

    # Setup for sounds
    pygame.mixer.init()

    # Intitialize pygame
    pygame.init()

    # Set window title
    pygame.display.set_caption('Audio Visualizer')

    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Frames
    FPS = 60
    FPSClock = pygame.time.Clock()

    # Plays sound
    pygame.mixer.music.load("file.wav")
    pygame.mixer.music.play(loops=0)

    # Main loop
    while True:

        # If closes the window
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                pygame.mixer.quit()

        # Sets screen to black
        screen.fill((0, 0, 0))

        # Draws each bar
        for b in bars:
            b.update(get_amplitude(b.frequency, pygame.mixer.music.get_pos()/1000))
            b.draw()

        # Updates screen
        pygame.display.flip()

        # Frames per second
        FPSClock.tick(FPS)

        # Stops program if music stops
        if pygame.mixer.music.get_busy() == False:
            pygame.display.quit()

# Opens audio files
def file_open():
    try:
        file_open.file = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
        shutil.copyfile(file_open.file, 'file.wav')
        pygame_window()
    except (FileNotFoundError,  PermissionError) as e:
        print(e)

# Creates tkinter window
root = tk.Tk()

# Sets size
root.geometry('300x300')

# Sets title
root.title('Audio Visualizer')

# Button that opens files
file_button = tk.Button(root, text="Select a file", command=file_open)
file_button.pack()

# Runs window
root.mainloop()