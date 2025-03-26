import pandas
import pygame

map = 'checkmap.xlsx'
dist = 50
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
xlen = 800
ylen = 800
colors = [white, black, red, green, blue]


def refresh():
    df = pandas.read_excel(map,header=None)
    matrix = df.values.tolist()
    for i in range(round(xlen/dist)):
        for j in range(round(ylen/dist)):
                pygame.draw.rect(screen, colors[matrix[i][j]], (j*dist, i*dist, dist, dist))
    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((xlen, ylen))
pygame.display.set_caption("Grid Map")
refresh()

while True:
        for event in pygame.event.get():  
            if event.type == pygame.KEYDOWN:  # Detect when a key is pressed
                if event.key == pygame.K_r:
                    refresh()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break

