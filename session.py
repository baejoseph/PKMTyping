import pygame
import random
from pokemon import Pokemon
from config import SCREEN_WIDTH, SCREEN_HEIGHT, REWARD_MAP, WHITE, BLACK, GREEN, AMBER, RED, GRAY, LIGHT_GRAY, COMBOCOLOR1, COMBOCOLOR2

# Pause menu options
pause_options = ["Resume", "Restart"]
selected_option = 0

pkbimg = pygame.image.load("assets/items/poke-ball.png")
scoreimg = pygame.image.load("assets/items/sapphire.png")
comboimg = pygame.image.load("assets/items/shiny-stone.png")
masterball = pygame.transform.scale(pygame.image.load("assets/items/gen5/master-ball.png"), (25, 25))
ultraball = pygame.transform.scale(pygame.image.load("assets/items/gen5/ultra-ball.png"), (25, 25))
greatball = pygame.transform.scale(pygame.image.load("assets/items/gen5/great-ball.png"), (25, 25))
normalball = pygame.transform.scale(pygame.image.load("assets/items/gen5/poke-ball.png"), (25, 25))

pygame.mixer.init()
pygame.mixer.music.load("assets/music/Forest.mp3")

# Timer event IDs
SPAWN_POKEMON_EVENT = pygame.USEREVENT + 1
MESSAGE_CLEAR_EVENT = pygame.USEREVENT + 2
JIGGLE_EVENT = pygame.USEREVENT + 4
SPECIAL_MESSAGE_CLEAR_EVENT = pygame.USEREVENT + 5

def draw_gradient_rect(surface, rect, color1, color2, radius=15):
    """Draw a vertical gradient rounded rectangle."""
    gradient_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for y in range(rect.height):
        ratio = y / rect.height
        color = (
            int(color1[0] * (1 - ratio) + color2[0] * ratio),
            int(color1[1] * (1 - ratio) + color2[1] * ratio),
            int(color1[2] * (1 - ratio) + color2[2] * ratio)
        )
        pygame.draw.line(gradient_surface, color, (0, y), (rect.width, y))

    # Create a rounded mask
    mask_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask_surface, (255, 255, 255), mask_surface.get_rect(), border_radius=radius)
    mask = pygame.mask.from_surface(mask_surface)

    # Apply the mask to the gradient
    rounded_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for x in range(rect.width):
        for y in range(rect.height):
            if mask.get_at((x, y)):
                rounded_surface.set_at((x, y), gradient_surface.get_at((x, y)))

    surface.blit(rounded_surface, rect.topleft)

def draw_rounded_rect(surface, rect, color, radius=15, outline_color=None, outline_width=2):
    """Draw a rounded rectangle with optional outline."""
    rounded_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(rounded_surface, color, rounded_surface.get_rect(), border_radius=radius)
    if outline_color:
        pygame.draw.rect(rounded_surface, outline_color, rounded_surface.get_rect(), outline_width, border_radius=radius)
    surface.blit(rounded_surface, rect.topleft)

class GameSession:
    def __init__(self, pokemon_data):
        self.reset_game(pokemon_data)

    def reset_game(self, pokemon_data):
        self.game_paused = False
        self.pokemon_data = pokemon_data
        self.caught_pokemon_count = 0
        self.combo_count = 0
        self.total_score = 0
        self.current_pokemon = None
        self.typed_name = ""
        self.start_time = None
        self.caught_sound = pygame.mixer.Sound('assets/sounds/paafekuto.ogg')
        self.miss_sound = pygame.mixer.Sound('assets/sounds/daijoubu.ogg')
        self.messages = []
        self.special_message = {"text": "", "start_time": pygame.time.get_ticks()}
        self.jiggle_offset = [0, 0]
        self.caught_pokemons = []
        self.combo_indices = []
        self.reward_map = REWARD_MAP
        pygame.mixer.music.play()

    def get_combo_reward(self, combo_count):
        return self.reward_map.get(combo_count, 500*(combo_count-14))

    def get_speed_multiplier(self, elapsed_time, time_limit):
        percentage = elapsed_time / time_limit
        if percentage <= 0.35:
            return 1.5
        elif percentage <= 0.55:
            return 1.2
        else:
            return 1.0

    def add_message(self, text):
        self.messages.append({"text": text, "start_time": pygame.time.get_ticks()})
        pygame.time.set_timer(MESSAGE_CLEAR_EVENT, 1000, True)

    def add_special_message(self, text):
        self.special_message["text"] = text
        self.special_message["start_time"] = pygame.time.get_ticks()
        pygame.time.set_timer(SPECIAL_MESSAGE_CLEAR_EVENT, 1000, True)

    def display_special_message(self, screen, font, color, width, height):
        current_time = pygame.time.get_ticks()
        self.draw_text(screen, self.special_message["text"], font, color, (width - font.size(self.special_message["text"])[0] - 50) // 2, 100)

    def display_messages(self, screen, font, color, width):
        current_time = pygame.time.get_ticks()
        for i, message in enumerate(self.messages[:]):
            self.draw_text(screen, message["text"], font, color, width - font.size(message["text"])[0] - 50, 50 + i * 50)

    def spawn_pokemon(self):
        pokemon_data_choice = random.choice(self.pokemon_data[:151])
        self.current_pokemon = Pokemon(pokemon_data_choice)
        self.typed_name = ""
        self.start_time = pygame.time.get_ticks()
        self.current_pokemon.cry.play()

    def pokemon_caught(self, elapsed_time):
        self.caught_pokemon_count += 1
        self.combo_count += 1

        # Calculate score
        base_score = self.get_combo_reward(self.combo_count)
        if self.current_pokemon.legendary:
            base_score = 10000
        speed_multiplier = self.get_speed_multiplier(elapsed_time, self.current_pokemon.time_limit)
        score = base_score * speed_multiplier
        self.total_score += score

        # Add to caught Pokémon list
        self.caught_pokemons.append((self.current_pokemon.icon, 
                                     self.current_pokemon.legendary,
                                     speed_multiplier == 1.2, 
                                     speed_multiplier == 1.5))

        # Add messages
        if self.current_pokemon.legendary:
            legendary = "LEGENDARY "
        else:
            legendary = ""
        self.add_message(f"{legendary}{self.current_pokemon.name} caught!")
        if speed_multiplier == 1.5:
            self.add_message(f"Super Fast! {round(base_score)} x 1.5")
        elif speed_multiplier == 1.2:
            self.add_message(f"Fast! {round(base_score)} x 1.2")
        if self.combo_count > 3:
            self.add_message(f"Combo {self.combo_count}!")

        self.current_pokemon.name_sound.play()
        pygame.time.set_timer(SPAWN_POKEMON_EVENT, 1000, True)

    def pokemon_missed(self, wait_time_ms):
        self.add_message("Missed!")
        if self.combo_count >= 3:
            self.combo_indices.append((len(self.caught_pokemons) - self.combo_count, len(self.caught_pokemons)))
        self.combo_count = 0
        self.miss_sound.play()
        self.current_pokemon = None
        pygame.time.set_timer(SPAWN_POKEMON_EVENT, wait_time_ms, True)

    def draw_pause_menu(self,screen, font):
        global selected_option
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(GRAY)
        overlay.set_alpha(150)  # Set transparency to 150
        screen.blit(overlay, (0, 0))

        # Draw pause menu options
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100)
        pygame.draw.rect(screen, WHITE, menu_rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, menu_rect, 2, border_radius=15)

        for i, option in enumerate(pause_options):
            color = GREEN if i == selected_option else BLACK
            self.draw_text(screen, option, font, color, menu_rect.x + 50, menu_rect.y + 20 + i * 30)

    def handle_pause_menu_input(self,event):
        global selected_option
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(pause_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(pause_options)
            elif event.key == pygame.K_RETURN:
                if pause_options[selected_option] == "Resume":
                    self.game_paused = False
                    pygame.mixer.music.unpause()
                elif pause_options[selected_option] == "Restart":
                    self.reset_game(self.pokemon_data)
                    self.spawn_pokemon()

    def draw_game_elements(self, screen, font, elapsed_time):
        if self.current_pokemon:
        
            # Apply jiggle offset
            jiggle_x, jiggle_y = self.jiggle_offset
            walk_x, walk_y = self.current_pokemon.walk_offset

            # Draw the Pokemon Background
            screen.blit(self.current_pokemon.bg, (450, 250))

            # Draw the Pokemon sprite
            screen.blit(self.current_pokemon.sprite, (SCREEN_WIDTH // 2 - self.current_pokemon.sprite.get_width() // 2 + walk_x +  jiggle_x, 100 + walk_y + jiggle_y))

            # Draw the rounded rectangle around the Pokémon name and timer bar
            name_x = SCREEN_WIDTH // 2 - font.size(self.current_pokemon.name)[0] // 2
            name_width = font.size(self.current_pokemon.name)[0]
            rect_width = name_width + 20  # Add some padding
            rect_height = 80  # Enough height to cover the name and timer bar
            rect_x = name_x - 10 + walk_x
            rect_y = 220
            draw_rounded_rect(screen, pygame.Rect(rect_x, rect_y, rect_width, rect_height), LIGHT_GRAY, radius=15, outline_color=BLACK)

            # Draw the Pokemon name in full capital letters
            name_x = SCREEN_WIDTH // 2 - font.size(self.current_pokemon.name)[0] // 2
            if elapsed_time > 3000 or len(self.typed_name) > 0:
                #self.draw_text(screen, self.current_pokemon.name, font, BLACK, name_x + jiggle_x, 200 + jiggle_y)
                self.draw_text(screen, self.current_pokemon.name, font, RED, name_x + walk_x, 240)
                # Draw the timer bar just below the typed name
                self.draw_timer_bar(screen, name_x + walk_x, 280, font.size(self.current_pokemon.name)[0], 10, elapsed_time, self.current_pokemon.time_limit)

            # Draw each typed letter exactly below each corresponding letter of the Pokemon name
            for i, char in enumerate(self.typed_name):
                char_x = name_x + font.size(self.current_pokemon.name[:i])[0]
                self.draw_text(screen, char, font, BLACK, char_x + walk_x, 240)
        else:
            screen.fill(WHITE)

        # Draw the score and combo count
        screen.blit(pkbimg, (20, 20))
        self.draw_text(screen, f"Caught: {self.caught_pokemon_count}", font, BLACK, 50, 20)
        screen.blit(comboimg, (20, 60))
        self.draw_text(screen, f"Combo: {self.combo_count}", font, BLACK, 50, 60)
        screen.blit(scoreimg, (20, 100))
        self.draw_text(screen, f"Score: {int(self.total_score)}", font, BLACK, 50, 100)

        # Draw the caught Pokémon icons
        self.draw_caught_pokemon_icons(screen)

    def draw_caught_pokemon_icons(self, screen):
        # Draw the box around it
        
        rect_width = 400  # Add some padding
        rect_height = 200  # Enough height to cover the name and timer bar
        rect_x = 10
        rect_y = 385
        
        draw_rounded_rect(screen, pygame.Rect(rect_x, rect_y, rect_width, rect_height), WHITE, radius=15, outline_color=BLACK)
               
        cols = 10
        rows = 5
        icon_size = 32
        padding = 5
        offset = 21
        x_start = 20
        y_start = SCREEN_HEIGHT - (rows * (icon_size + padding)) - 20

        # Include the current combo if it exists and is of length 3 or more
        combo_indices = self.combo_indices.copy()
        if self.combo_count >= 3:
            combo_indices.append((len(self.caught_pokemons) - self.combo_count, len(self.caught_pokemons)))

        # Draw combo outlines for all combos of length 3 or more
        for start_index, end_index in combo_indices:
            start_col = start_index % cols
            start_row = start_index // cols
            end_col = (end_index - 1) % cols
            end_row = (end_index - 1) // cols

            for row in range(start_row, end_row + 1):
                row_start_col = start_col if row == start_row else 0
                row_end_col = end_col if row == end_row else cols - 1
                x1 = x_start + row_start_col * (icon_size + padding) - 2
                x2 = x_start + row_end_col * (icon_size + padding) + icon_size + 2
                y = y_start + row * (icon_size + padding) - 2
                highlight_rect = pygame.Rect(x1, y, x2 - x1, icon_size + 4)
                
                # Draw gradient background
                draw_gradient_rect(screen, highlight_rect, COMBOCOLOR1, COMBOCOLOR2)

        for index, (icon, legendary, fast, superfast) in enumerate(self.caught_pokemons):
            col = index % cols
            row = index // cols
            x = x_start + col * (icon_size + padding)
            y = y_start + row * (icon_size + padding)
    
            screen.blit(icon, (x, y))
            
            # Draw Legendary outline
            if legendary:
                screen.blit(masterball, (x+offset,y+offset))
                        # Draw Super Fast outline
            elif superfast:
                screen.blit(ultraball, (x+offset,y+offset))
            elif fast:
                screen.blit(greatball, (x+offset,y+offset))
            else:
                screen.blit(normalball, (x+offset,y+offset))



    @staticmethod
    def draw_text(surface, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        surface.blit(text_obj, (x, y))

    @staticmethod
    def draw_timer_bar(surface, x, y, width, height, elapsed_time, time_limit):
        fill_width = (elapsed_time / time_limit) * width
        color = GREEN if fill_width < width * 0.55 else AMBER if fill_width < width * 0.80 else RED
        pygame.draw.rect(surface, color, (x, y, fill_width, height))

    @staticmethod
    def jiggle():
        return random.randint(-5, 5), random.randint(-5, 5)
