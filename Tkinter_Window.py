import pygame
import tkinter
import wave
import shutil
import librosa
import numpy as np
from tkinter import filedialog
from pygame.locals import QUIT

# Opens pygame window
def pygame_window():

    # The audio bars
    class Bar:

        def __init__(self, x, y, frequency, min_height, max_height, min_amp, max_amp):

            self.x = x
            self.y = y
            self.frequency = frequency
            self.min_height = min_height
            self.max_height = max_height
            self.min_amp = min_amp
            self.max_amp = max_amp

        # Updates bars
        def update(self):


    # Screen size
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Setup for sounds
    pygame.mixer.init()

    # Intitialize pygame
    pygame.init()

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Set window title
    pygame.display.set_caption('Audio Visualizer')

    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Plays sound
    pygame.mixer.music.load('file.wav')
    pygame.mixer.music.play(loops=0)

    # Processing data
    '''samplerate, wavdata = wavfile.read('file.wav')
        chunks = np.array_split(wavdata, len(wavdata)/(samplerate/2))
        db = [(20*np.log10(chunk)) for chunk in chunks]'''

    '''audio = wave.open("file.wav", "rb")
    audio_params = audio.getparams()
    sampwidth, framerate, nframes = audio_params[1:4]
    wavdata = audio.readframes(nframes)
    intdata = int.from_bytes(wavdata, byteorder='little')
    print(intdata)'''

    time_series, sample_width = librosa.load('file.wav')
    amplitude = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048))
    frequencies = np.arange(100, 3000, 100)

    bars = []
    for i in frequencies:
        bars.append(Bar())

    # Draws the bars of the visualizer
    def show_bars():
        bars = ["x", "y"]
        for bar in bars:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((bars.index(bar)*30+10), 590, 25, 5))

    # Main loop
    while True:

        # If closes the window
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                pygame.mixer.quit()

        # Sets background as black
        screen.fill((0, 0, 0))
        show_bars()
        # Updates screen
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        clock.tick(30)

        # Quits window when stops playing
        if pygame.mixer.music.get_busy() == False:
            pygame.display.quit()

# Opens audio files
def file_open():
    file_open.file = filedialog.askopenfilename(filetypes=[("Audio", "*.wav")])
    shutil.copyfile(file_open.file, 'file.wav')
    pygame_window()

# Creates window
root = tkinter.Tk()

# Sets size
root.geometry('300x300')

# Sets title
root.title("Audio Visualizer")

# Open file button
file_button = tkinter.Button(root, text='Select a file', command=file_open)
file_button.pack()

# Runs window
root.mainloop()