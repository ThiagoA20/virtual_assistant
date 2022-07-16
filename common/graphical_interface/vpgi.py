import pygame
from pygame.locals import *

running = False
clock = False
screen = False
my_font = False

# screen = pygame.display.set_mode((WIDTH, HEIGHT))
def initialSetup():
    global clock
    global screen
    global my_font

    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    my_font = pygame.font.SysFont('rockwell', 18)

# Detect Keyboard
def detectEvents():
    global running
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

# Draw Screen
def drawScreen():
    screen.fill((25, 25, 25))

###############################################
def is_process_alive(filename):
    global running
    with open(filename, 'r') as file:
        if file.readlines()[0] == '0':
            running = False
###############################################

# Main loop
def Interface(**kwargs):
    global running

    ###############################################
    check_process = kwargs.pop('is_alive_temp', False)
    ###############################################

    if check_process != False:
        with open(check_process, 'r') as file:
            if file.readlines()[0] == '1':
                running = True
                initialSetup()
            else:
                running = False

    while running:
        clock.tick(60)

        ###############################################
        if check_process != False:
            is_process_alive(check_process)
        ###############################################

        drawScreen()
        detectEvents()
        pygame.display.update()

    pygame.display.quit()