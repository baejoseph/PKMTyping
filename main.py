import pygame
import json
import random
import os
from pokemon import Pokemon

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

pkbimg = pygame.image.load("assets/items/poke-ball.png")
scoreimg = pygame.image.load("assets/items/sapphire.png")
comboimg = pygame.image.load("assets/items/shiny-stone.png")

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon Typing Adventure")

# Font
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

# Scoring system
reward_map = {
    1: 100,
    2: 150,
    3: 200,
    4: 300,
    5: 400,
    6: 500,
    7: 700,
    8: 900,
    9: 1000,
    10: 1200,
}

def get_combo_reward(combo_count):
    return reward_map.get(combo_count, 1200)  # Default to 1200 for combos beyond the map

def get_speed_multiplier(elapsed_time, time_limit):
    percentage = elapsed_time / time_limit
    if percentage <= 0.35:
        return 1.5
    elif percentage <= 0.55:
        return 1.2
    else:
        return 1.0

def is_legendary(pokemon):
    return pokemon["HP"] + pokemon["Attack"] + pokemon["Sp. Attack"] > 250

def get_time_limit(pokemon):
    if is_legendary(pokemon):
        return 7000
    else: 
        return 10000

# Game Sounds
caught_sound = pygame.mixer.Sound('assets/sounds/paafekuto.ogg')
miss_sound = pygame.mixer.Sound('assets/sounds/daijoubu.ogg')

# Game variables
caught_pokemon_count = 0
combo_count = 0
total_score = 0
current_pokemon = None
typed_name = ""
start_time = None
messages = []
special_message = {"text":"", "start_time":pygame.time.get_ticks()}
last_correct_letter_time = 0
jiggle_offset = [0, 0]

# Timer event IDs
SPAWN_POKEMON_EVENT = pygame.USEREVENT + 1
MESSAGE_CLEAR_EVENT = pygame.USEREVENT + 2
LAST_CORRECT_LETTER_EVENT = pygame.USEREVENT + 3
JIGGLE_EVENT = pygame.USEREVENT + 4
SPECIAL_MESSAGE_CLEAR_EVENT = pygame.USEREVENT + 5

# Helper functions
def spawn_pokemon():
    global current_pokemon, typed_name, start_time
    pokemon_data_choice = random.choice(pokemon_data[:151])
    current_pokemon = Pokemon(pokemon_data_choice)
    typed_name = ""
    start_time = pygame.time.get_ticks()
    current_pokemon.cry.play()

def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

def draw_timer_bar(surface, x, y, width, height, elapsed_time, time_limit):
    fill_width = (elapsed_time / time_limit) * width
    color = GREEN if fill_width < width * 0.5 else AMBER if fill_width < width * 0.75 else RED
    pygame.draw.rect(surface, color, (x, y, fill_width, height))
    
def add_message(text):
    messages.append({"text": text, "start_time": pygame.time.get_ticks()})
    pygame.time.set_timer(MESSAGE_CLEAR_EVENT, 1000, True)

def add_special_message(text):
    special_message["text"] = text
    special_message["start_time"] = pygame.time.get_ticks()
    pygame.time.set_timer(SPECIAL_MESSAGE_CLEAR_EVENT, 1000, True)

def display_special_message():
    current_time = pygame.time.get_ticks()
    draw_text(screen, special_message["text"], font, BLACK, (SCREEN_WIDTH - font.size(special_message["text"])[0]-50)//2, 100)

def display_messages():
    current_time = pygame.time.get_ticks()
    for i, message in enumerate(messages[:]):
        draw_text(screen, message["text"], font, BLACK, SCREEN_WIDTH - font.size(message["text"])[0]-50, 50+i*50)
    
def jiggle():
    return random.randint(-5, 5), random.randint(-5, 5)

# Main game loop
running = True
spawn_pokemon()

pygame.time.set_timer(JIGGLE_EVENT, 110)

while running:
    screen.fill(WHITE)
    # Start the jiggle event
    elapsed_time = pygame.time.get_ticks() - start_time
    if current_pokemon.legendary and current_pokemon.get_this_one:
        add_special_message("Get this one!")
        current_pokemon.get_this_one = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            typed_name += event.unicode.upper()

            if current_pokemon.name.startswith(typed_name):
                if typed_name == current_pokemon.name:
                    
                    caught_pokemon_count += 1
                    combo_count += 1
                    
                    # Calculate score
                    combo_reward = get_combo_reward(combo_count)
                    speed_multiplier = get_speed_multiplier(elapsed_time, current_pokemon.time_limit)
                    score = combo_reward * speed_multiplier
                    if current_pokemon.legendary: score *= 10
                    total_score += score
                    
                    # Add messages
                    if current_pokemon.legendary:    
                        legendary = "LEGENDARY "
                    else:
                        legendary = ""
                    add_message(f"{legendary}{current_pokemon.name} caught!")
                    if speed_multiplier == 1.5:
                        add_message("Super Fast! x1.5")
                        #caught_sound.play()
                    elif speed_multiplier == 1.2:
                        add_message("Fast! x1.2")
                    if combo_count > 3:
                        add_message(f"Combo {combo_count}!")
                    #add_special_message(score)
                    
                    current_pokemon.name_sound.play()
                    pygame.time.set_timer(SPAWN_POKEMON_EVENT, 1000, True)
                    
            else:
                add_message("Missed!")
                combo_count = 0
                miss_sound.play()
                
                pygame.time.set_timer(SPAWN_POKEMON_EVENT, 1500, True)

            last_correct_letter_time = pygame.time.get_ticks()
            pygame.time.set_timer(LAST_CORRECT_LETTER_EVENT, 500, True)

        elif event.type == SPAWN_POKEMON_EVENT:
            spawn_pokemon()
        elif event.type == MESSAGE_CLEAR_EVENT:
            messages.clear()
        elif event.type == SPECIAL_MESSAGE_CLEAR_EVENT:
            special_message["text"]=""
        elif event.type == LAST_CORRECT_LETTER_EVENT:
            last_correct_letter_time = 0
        elif event.type == JIGGLE_EVENT:
            jiggle_offset = jiggle()


    # Update game state
    if elapsed_time > current_pokemon.time_limit:
        combo_count = 0
        miss_sound.play()
        
        pygame.time.set_timer(SPAWN_POKEMON_EVENT, 10, True)

    # Apply jiggle offset
    jiggle_x, jiggle_y = jiggle_offset

    # Draw the Pokemon Background
    screen.blit(current_pokemon.bg, (450, 250))

    # Draw the Pokemon sprite
    screen.blit(current_pokemon.sprite, (SCREEN_WIDTH//2 - current_pokemon.sprite.get_width()//2 + jiggle_x, 100 + jiggle_y))

    # Draw the Pokemon name in full capital letters
    name_x = SCREEN_WIDTH//2 - font.size(current_pokemon.name)[0]//2
    if elapsed_time > 3000 or len(typed_name) > 0:
        draw_text(screen, current_pokemon.name, font, BLACK, name_x + jiggle_x, 200 + jiggle_y)
        draw_text(screen, current_pokemon.name, font, RED, name_x + jiggle_x, 240 + jiggle_y)
        # Draw the timer bar just below the typed name
        draw_timer_bar(screen, name_x + jiggle_x, 220 + jiggle_y, font.size(current_pokemon.name)[0], 10, elapsed_time, current_pokemon.time_limit)

    # Draw each typed letter exactly below each corresponding letter of the Pokemon name
    for i, char in enumerate(typed_name):
        char_x = name_x + font.size(current_pokemon.name[:i])[0]
        draw_text(screen, char, font, BLACK, char_x + jiggle_x, 240 + jiggle_y)
    
    
    # Draw the score and combo count
    screen.blit(pkbimg, (20, 20))
    draw_text(screen, f"Caught: {caught_pokemon_count}", font, BLACK, 50, 20)
    screen.blit(comboimg, (20, 60))
    draw_text(screen, f"Combo: {combo_count}", font, BLACK, 50, 60)
    screen.blit(scoreimg, (20, 100))
    draw_text(screen, f"Score: {int(total_score)}", font, BLACK, 50, 100)

    # Display messages
    display_messages()
    display_special_message()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()