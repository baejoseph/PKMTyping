import pygame
import json
import random
import os
from pokemon import Pokemon
from session import GameSession

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
AMBER = (255, 191, 0)
RED = (255, 0, 0)

# Load JSON data
with open("pokemon_data_updated.json", "r", encoding="utf-8") as file:
    pokemon_data = json.load(file)

# Load all name sounds into memory
Pokemon.load_name_sounds()

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon Typing Adventure")

# Font
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

# Timer event IDs
SPAWN_POKEMON_EVENT = pygame.USEREVENT + 1
MESSAGE_CLEAR_EVENT = pygame.USEREVENT + 2
JIGGLE_EVENT = pygame.USEREVENT + 4
SPECIAL_MESSAGE_CLEAR_EVENT = pygame.USEREVENT + 5

# Main game loop
game_session = GameSession(pokemon_data)
game_session.spawn_pokemon()

running = True
pygame.time.set_timer(JIGGLE_EVENT, 110)

while running:
    screen.fill(WHITE)
    elapsed_time = pygame.time.get_ticks() - game_session.start_time

    if game_session.current_pokemon.legendary and game_session.current_pokemon.get_this_one:
        game_session.add_special_message("Get this one!")
        game_session.current_pokemon.get_this_one = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            game_session.typed_name += event.unicode.upper()

            if game_session.current_pokemon.name.startswith(game_session.typed_name):
                if game_session.typed_name == game_session.current_pokemon.name:
                    game_session.pokemon_caught(elapsed_time)
            else:
                game_session.pokemon_missed(1500)

        elif event.type == SPAWN_POKEMON_EVENT:
            game_session.spawn_pokemon()
        elif event.type == MESSAGE_CLEAR_EVENT:
            game_session.messages.clear()
        elif event.type == SPECIAL_MESSAGE_CLEAR_EVENT:
            game_session.special_message["text"] = ""
        elif event.type == JIGGLE_EVENT:
            game_session.jiggle_offset = game_session.jiggle()

    # Update game state
    if elapsed_time > game_session.current_pokemon.time_limit:
        game_session.pokemon_missed(10)

    # Draw game elements
    game_session.draw_game_elements(screen, font, elapsed_time)

    # Display messages
    game_session.display_messages(screen, font, BLACK, SCREEN_WIDTH)
    game_session.display_special_message(screen, font, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()