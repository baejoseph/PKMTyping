import pygame
from utils import resource_path

class Sprites:
    pkbimg = pygame.transform.scale(pygame.image.load(resource_path("assets/balls/poke-ball.png")), (30, 30))
    scoreimg = pygame.transform.scale(pygame.image.load(resource_path("assets/balls/sapphire.png")), (25, 25))
    comboimg = pygame.transform.scale(pygame.image.load(resource_path("assets/balls/shiny-stone.png")), (30, 30))
    mistakeimg = pygame.transform.scale(pygame.image.load(resource_path("assets/balls/red-card.png")), (30, 30))
    masterball = pygame.transform.scale(pygame.image.load(resource_path("assets/balls/master-ball.png")), (25, 25))
    ultraball = pygame.transform.scale(pygame.image.load(resource_path("assets/balls/ultra-ball.png")), (25, 25))
    greatball = pygame.transform.scale(pygame.image.load(resource_path("assets/balls/great-ball.png")), (25, 25))
    normalball = pygame.transform.scale(pygame.image.load(resource_path("assets/balls/poke-ball.png")), (25, 25))
    bikeimg = pygame.transform.scale(pygame.image.load(resource_path("assets/balls/bicycle.png")), (20, 20))