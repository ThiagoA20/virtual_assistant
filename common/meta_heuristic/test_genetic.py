# from genetic_algorithm import initPopulation, Population

# Gerar população
# population: Population = initPopulation()
from concurrent.futures import thread
import random
import os
import time
from threading import Thread

import pygame
from pygame.locals import *


WIDTH = 1920
HEIGHT = 1080

pygame.init()
pygame.display.set_caption('Trading bot')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.font.init()
my_font = pygame.font.SysFont('rockwell', 18)
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

""" 
No caso de um jogo, aquele que obteve o score máximo pode ser o que derrotou mais inimigos, ficou vivo mais tempo, coletou mais recursos, foi mais organizado, etc.

Já no caso de um daytrade, aquele que obteve o score máximo pode ser o que ganhou mais dinheiro.
Sendo que o lucro máximo vai ser o preço máximo que o gráfico chegou menos o preço da entrada para uma operação de compra e o lucro máximo para uma operação de venda vai ser o preço de entrada menos o preço mínimo que o gráfico chegou.
"""
score_maximo = [
    10,
    20,
    10,
    50,
    200,
    30,
    10,
    40,
    80,
    10
]

"""
O score obtido sempre será menor ou igual ao score máximo,
ele também pode ser negativo
"""
population_score = [
    [8, 17, 5, 20, 127, 12, 3, 28, 78, 8],
    [3, 19, 8, 29, 170, 8, 5, 38, 76, 4],
    [6, 13, 9, 42, 157, 11, 7, 12, 57, 7],
    [9, 15, 1, 32, 107, 15, 8, 32, 72, 5],
    [10, 12, 2, 21, 77, 30, 9, 31, 75, 6]
]

def calcular_taxa_de_acerto(score_maximo: list, score_obtido: list):
    score_individuo_perfeito = sum(score_maximo)
    score_individuo_atual = sum(score_obtido)
    taxa_de_acerto = round(score_individuo_atual / score_individuo_perfeito, 4)
    return taxa_de_acerto

melhor_individuo = 1
maximun_score = 0
maior_taxa_de_acerto = {}
running = True
draw_individuals = False
new_round = False

def drawScreen():
    global melhor_individuo
    global maximun_score
    global maior_taxa_de_acerto
    global melhor_score
    global draw_individuals

    LEFT_INFO = WIDTH/4
    RIGHT_INFO = WIDTH - WIDTH/4 + 50

    screen.fill((25, 25, 25))
    pygame.draw.line(screen, (175, 175, 175), (LEFT_INFO, 0), (LEFT_INFO, HEIGHT))
    pygame.draw.line(screen, (175, 175, 175), (RIGHT_INFO - 50, 0), (RIGHT_INFO - 50, HEIGHT))

    if draw_individuals:
        text_surface3 = my_font.render(f"Score máximo: {maximun_score}", False, (175, 175, 175))
        screen.blit(text_surface3, (100, 140))
        text_surface2 = my_font.render(f"Melhor indivíduo: {melhor_individuo}", False, (175, 175, 175))
        screen.blit(text_surface2, (RIGHT_INFO, 50))

        i = 20
        for individual in maior_taxa_de_acerto:
            individual_information = my_font.render(f"Individual {individual} - taxa de acerto: {maior_taxa_de_acerto[individual]}", False, (175, 175, 175))
            y = 20 + i
            screen.blit(individual_information, (100, y))
            i += 20

def detectEvents():
    global running
    global draw_individuals
    global new_round
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_1:
                draw_individuals = not draw_individuals
            if event.key == K_2:
                new_round = not new_round

def runGame():
    global melhor_individuo
    global maximun_score
    global maior_taxa_de_acerto
    global running
    global new_round

    while running:
        if new_round:
            new_score = random.randint(10, 200)
            maximun_score = new_score
            score_maximo.append(new_score)
            for individual in population_score:
                individual.append(random.randrange(0, new_score))

            individuals = 1
            for individual in population_score:
                taxa_de_acerto = calcular_taxa_de_acerto(score_maximo, individual)
                maior_taxa_de_acerto[individuals] = taxa_de_acerto
                # print(f"Individual {individuals} - taxa de acerto: {taxa_de_acerto}")
                individuals += 1

            melhor_score = 0
            for individual in maior_taxa_de_acerto:
                if maior_taxa_de_acerto[individual] > melhor_score:
                    melhor_score = maior_taxa_de_acerto[individual]
                    melhor_individuo = individual
            time.sleep(0.1)


def main():
    global running
    game = Thread(target=runGame, daemon=True)
    game.start()

    while running:
        clock.tick(60)
        drawScreen()
        detectEvents()
        pygame.display.update()
    
    pygame.display.quit()

# Salvar o DNA da população
# population.savePopulationDNA()

if __name__ == '__main__':
    main()