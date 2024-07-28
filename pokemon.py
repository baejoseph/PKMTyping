import pygame
import random
import os
from config import LEGENDARY_CUTOFF, NORMAL_POKEMON_CATCH_TIME, LEGENDARY_POKEMON_CATCH_TIME, SCREEN_WIDTH, SCREEN_HEIGHT

class Pokemon:
    name_sounds = {}

    @classmethod
    def load_name_sounds(cls, sounds_folder="assets/names"):
        for filename in os.listdir(sounds_folder):
            if filename.endswith(".wav"):
                id = int(filename.split('-')[0])
                cls.name_sounds[id] = pygame.mixer.Sound(os.path.join(sounds_folder, filename))

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]["english"].upper()
        self.sprite = self.load_image()
        self.icon = self.load_icon()
        self.bg = self.load_bg_image()
        self.cry = self.load_sound()
        self.name_sound = Pokemon.name_sounds.get(self.id, None)
        self.legendary = self.is_legendary(data["base"])
        self.time_limit = self.get_time_limit(data["base"])
        self.get_this_one = True
        self.walk_offset = [0,0]

    def load_image(self):
        return pygame.image.load(os.path.join('assets/sprites', f"{self.id}.png"))

    def load_icon(self):
        return pygame.image.load(os.path.join('assets/icons', f"{self.id}.png"))

    def load_bg_image(self, target_size=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), gray_alpha=0.4):
        original_image = pygame.image.load(os.path.join('assets/sugimori', f"{self.id}.png")).convert_alpha()
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
        return final_image

    def load_sound(self):
        return pygame.mixer.Sound(os.path.join('assets/cries', f"{self.id}.ogg"))

    def is_legendary(self, base_stats):
        return base_stats["HP"] + base_stats["Attack"] + base_stats["Sp. Attack"] > LEGENDARY_CUTOFF

    def get_time_limit(self, base_stats):
        return LEGENDARY_POKEMON_CATCH_TIME if self.is_legendary(base_stats) else NORMAL_POKEMON_CATCH_TIME

    def walk(self):
        self.walk_offset[0] += random.randint(-5, 5)
        self.walk_offset[1] += random.randint(-5, 5)