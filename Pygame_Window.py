import Tkinter_Window
import pygame

# Opens pygame window
def pygame_window():

    # Gets quit function
    from pygame.locals import QUIT

    # Setup for sounds
    pygame.mixer.init()

    # Intitialize pygame
    pygame.init()

    # Set window title
    pygame.display.set_caption('Audio Visualizer')

    # Create screen
    screen = pygame.display.set_mode((800, 600))

    # Plays sound
    pygame.mixer.music.load(Tkinter_Window.file_open.file)
    pygame.mixer.music.play(loops=0)

    # Main loop
    running = True
    while running is True:

        # If closes the window
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Updates screen
        pygame.display.flip()

        if pygame.mixer.music.get_busy() == False:
            break