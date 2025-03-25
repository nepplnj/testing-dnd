import pandas
import pygame

map = 'checkmap.xlsx'
dist = 50
white = (255, 255, 255)
black = (0, 0, 0)
xlen = 800
ylen = 800


def refresh():
    df = pandas.read_excel(map,header=None)
    matrix = df.values.tolist()
    for i in range(round(xlen/dist)):
        for j in range(round(ylen/dist)):
            if matrix[i][j] == 1:
                pygame.draw.rect(screen, black, (j*dist, i*dist, dist, dist))
            elif matrix[i][j] == 2:
                 pygame.draw.rect(screen, white, (j*dist, i*dist, dist, dist))
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

