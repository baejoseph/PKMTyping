import pygame
import random
import os
from utils import resource_path
from config import LEGENDARY_CUTOFF, NORMAL_POKEMON_CATCH_TIME, LEGENDARY_POKEMON_CATCH_TIME, SCREEN_WIDTH, SCREEN_HEIGHT

class Pokemon:
    name_sounds = {}

    @classmethod
    def load_name_sounds(cls, sounds_folder=resource_path("assets/names")):
        for filename in os.listdir(sounds_folder):
            if filename.endswith(".wav"):
                id = int(filename.split('-')[0])
                cls.name_sounds[id] = pygame.mixer.Sound(os.path.join(sounds_folder, filename))

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]["english"].upper()
        self.japanese_name = data["name"]["japanese"]
        self.korean_name = data["name"]["korean"]
        self.sprite = self.load_image()
        self.icon = self.load_icon()
        self.bg = self.load_bg_image()
        self.cry = self.load_sound()
        self.name_sound = Pokemon.name_sounds.get(self.id, None)
        self.is_caught = False
        self.caught_time = None
        self.ball_hit = False
        self.legendary = self.is_legendary(data["base"])
        self.is_fast = False
        self.is_super_fast = False
        self.time_limit = self.get_time_limit(data["base"])
        self.start_time = pygame.time.get_ticks()
        self.get_this_one = True
        self.walk_offset = [0,0]
        self.current_position = [0,0]
        self.elapsed_time = 0
        self.total_paused_time = 0

    def load_image(self):
        return pygame.image.load(resource_path(os.path.join('assets/sprites', f"{self.id}.png")))

    def load_icon(self):
        return pygame.image.load(resource_path(os.path.join('assets/icons', f"{self.id}.png")))

    def load_bg_image(self, target_size=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), gray_alpha=0.9):
        original_image = pygame.image.load(resource_path(os.path.join('assets/sugimori_mini', f"{self.id}.png"))).convert_alpha()
        orig_width, orig_height = original_image.get_size()
        aspect_ratio = orig_width / orig_height
        if aspect_ratio > (target_size[0] / target_size[1]):
            new_width = target_size[0]
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = target_size[1]
            new_width = int(new_height * aspect_ratio)
        scaled_image = pygame.transform.smoothscale(original_image, (new_width, new_height))
        gray_surface = pygame.Surface(scaled_image.get_size(), pygame.SRCALPHA)
        gray_surface.fill((128, 128, 128, int(255 * gray_alpha)))
        final_image = scaled_image.copy()
        final_image.blit(gray_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Render the Korean and Japanese name
        japanese_font = pygame.font.Font(resource_path("assets/font/MS PGothic.ttf"), 72)  # Adjust the font size as needed
        korean_font = pygame.font.Font(resource_path("assets/font/UnGungseo.ttf"), 72)  # Adjust the font size as needed
        id_font = pygame.font.Font(resource_path("assets/font/Courier New.ttf"), 62)
        
        japanese_surface = japanese_font.render(self.japanese_name, True, (244, 244, 244))  # Stylize the text as needed (e.g., color)
        korean_surface = korean_font.render(self.korean_name, True, (244, 244, 244))  # Stylize the text as needed (e.g., color)
        id_surface = id_font.render(f"#{self.id:04d}", True, (244,244,244))
        
        # Position the text at the bottom-right corner, justified to the right edge
        japanese_rect = japanese_surface.get_rect(bottomright=(new_width - 10, new_height - 10))  # 10-pixel padding from edges
        final_image.blit(japanese_surface, japanese_rect.topleft)
        korean_rect = korean_surface.get_rect(bottomright=(new_width - 10, japanese_rect.top - 10))  # 10-pixel padding from edges
        final_image.blit(korean_surface, korean_rect.topleft)
        id_rect = id_surface.get_rect(bottomright=(new_width - 10, korean_rect.top - 10))
        final_image.blit(id_surface, id_rect.topleft)
        
        return final_image

    def load_sound(self):
        return pygame.mixer.Sound(resource_path(os.path.join('assets/cries', f"{self.id}.ogg")))

    def is_legendary(self, base_stats):
        BST = base_stats["HP"] + base_stats["Attack"] + base_stats["Sp. Attack"]
        BST += base_stats["Defense"] + base_stats["Speed"] + base_stats["Sp. Defense"]
        return BST >= LEGENDARY_CUTOFF

    def get_time_limit(self, base_stats):
        return LEGENDARY_POKEMON_CATCH_TIME if self.is_legendary(base_stats) else NORMAL_POKEMON_CATCH_TIME

    def walk(self):
        self.walk_offset[0] += random.randint(-5, 5)
        self.walk_offset[1] += random.randint(-5, 10)
        
    def copy(self):
        # Create a new Pokemon instance without initializing it
        new_copy = Pokemon.__new__(Pokemon)

        # Copy the attributes from the current instance to the new one
        new_copy.__dict__ = self.__dict__.copy()

        return new_copy