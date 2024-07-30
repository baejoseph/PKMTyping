import pygame
import json
from pokemon import Pokemon
from session import GameSession
from config import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, BLACK, FONTPATH, TRANSITION_TIME

# Initialize Pygame
pygame.init()

# Load JSON data
with open("data/pokemon_data_updated.json", "r", encoding="utf-8") as file:
    pokemon_data = json.load(file)

# Load all name sounds into memory
Pokemon.load_name_sounds()

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Poke Typing")

# Font
font = pygame.font.Font(FONTPATH, 30)
large_font = pygame.font.Font("font/MS PGothic.ttf", 92)
mini_font = pygame.font.Font("font/Microsoft Sans Serif.ttf", 20)

# Clock
clock = pygame.time.Clock()

# Timer event IDs
SPAWN_POKEMON_EVENT = pygame.USEREVENT + 1
MESSAGE_CLEAR_EVENT = pygame.USEREVENT + 2
WALK_EVENT = pygame.USEREVENT + 3
JIGGLE_EVENT = pygame.USEREVENT + 4
SPECIAL_MESSAGE_CLEAR_EVENT = pygame.USEREVENT + 5
TRANSITION_END_EVENT = pygame.USEREVENT + 6

# Main game loop
game_session = GameSession(pokemon_data, screen, font)
game_session.spawn_pokemon()

running = True

pygame.time.set_timer(JIGGLE_EVENT, 110)
pygame.time.set_timer(WALK_EVENT, 200)

current_time = 0

while running:

    screen.blit(game_session.bg_image, (0, 0))
    current_time = pygame.time.get_ticks()
    
    game_session.update_time(current_time)

    if game_session.current_pokemon and game_session.current_pokemon.legendary and game_session.current_pokemon.get_this_one:
        game_session.add_special_message("Get this one!")
        game_session.current_pokemon.get_this_one = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif game_session.game_ended:
            game_session.handle_end_menu_input(event)

        elif game_session.game_paused:
            game_session.handle_pause_menu_input(event)            
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_session.game_paused:
                game_session.unpause_game(current_time)
            else:
                game_session.pause_game(current_time)

        elif game_session.current_pokemon and event.type == pygame.KEYDOWN:
            game_session.typed_name += event.unicode.upper()
            game_session.animate_last_letter(event.unicode.upper())

            if game_session.current_pokemon.name.startswith(game_session.typed_name):
                if game_session.typed_name == game_session.current_pokemon.name:
                    game_session.pokemon_caught(game_session.current_pokemon.elapsed_time)
            else:
                game_session.pokemon_missed(500)

        elif event.type == SPAWN_POKEMON_EVENT:
            game_session.check_progress()
        elif event.type == MESSAGE_CLEAR_EVENT:
            game_session.messages.clear()
        elif event.type == SPECIAL_MESSAGE_CLEAR_EVENT:
            game_session.special_message["text"] = ""
        elif game_session.current_pokemon and event.type == JIGGLE_EVENT:
            game_session.jiggle_offset = game_session.jiggle()
        elif game_session.current_pokemon and event.type == WALK_EVENT:
            game_session.current_pokemon.walk()
        elif event.type == TRANSITION_END_EVENT:
            game_session.unpause_game(current_time, False)

    if game_session.transitioning:
        game_session.display_region_transition()
        continue

    if game_session.animation_state != "IDLE":
        game_session.update_capture_animation(screen)

    # Miss Pokemon due to running out of time
    if game_session.current_pokemon and game_session.current_pokemon.elapsed_time > game_session.current_pokemon.time_limit:
            game_session.pokemon_missed(10)

    # Display messages
    if game_session.game_ended:
        game_session.draw_end_screen(screen, font)
    elif game_session.game_paused:
        game_session.draw_pause_menu(screen, font)
    else:
        if game_session.current_pokemon:
            game_session.draw_game_elements(screen, large_font, game_session.current_pokemon.elapsed_time, game_session.bg_image)
        # Draw the caught Pokémon icons
        game_session.display_messages(screen, font, BLACK, SCREEN_WIDTH)
        game_session.display_special_message(screen, font, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    if not game_session.game_ended:
        game_session.draw_game_scores(screen, font)
        game_session.draw_caught_pokemon_icons(screen)
    

    # Draw the copyright line
    copyright_text = "Copyright 2024 Joseph Bae, made for my children with love"
    text_surface = mini_font.render(copyright_text, True, WHITE)
    screen.blit(text_surface, (SCREEN_WIDTH - text_surface.get_width() - 30, SCREEN_HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()