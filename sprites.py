import pygame

class Sprites:
    pkbimg = pygame.image.load("assets/items/poke-ball.png")
    scoreimg = pygame.image.load("assets/items/sapphire.png")
    comboimg = pygame.image.load("assets/items/shiny-stone.png")
    mistakeimg = pygame.image.load("assets/items/red-card.png")
    masterball = pygame.transform.scale(pygame.image.load("assets/items/gen5/master-ball.png"), (25, 25))
    ultraball = pygame.transform.scale(pygame.image.load("assets/items/gen5/ultra-ball.png"), (25, 25))
    greatball = pygame.transform.scale(pygame.image.load("assets/items/gen5/great-ball.png"), (25, 25))
    normalball = pygame.transform.scale(pygame.image.load("assets/items/gen5/poke-ball.png"), (25, 25))