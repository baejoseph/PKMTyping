# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TRANSITION_TIME = 2500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
AMBER = (255, 191, 0)
RED = (255, 0, 0)
GRAY = (120,120,120)
LIGHT_GRAY = (220,220,220)
COMBOCOLOR1 = (255, 165, 0)
COMBOCOLOR2 = (255, 69, 0)

# Font
FONTPATH = "assets/font/Microsoft Sans Serif.ttf"

# Pokemon Gens
GENS = [
    {"id": 1,
  "name": "Kanto",
  "indices": [0,151],
  "bg": "Pallet_Town_anime.png",
  "music":"Pikachu.mp3"},
    {"id": 2,
  "name": "Johto",
  "indices": [151,251],
  "bg": "Azalea_Town_anime.png",
  "music":"Deerling.mp3"},
    {"id": 3,
  "name": "Hoenn",
  "indices": [251,386],
  "bg": "Slateport_City_anime.png",
  "music":"Zorua.mp3"},
    {"id": 4,
  "name": "Sinnoh",
  "indices": [386,493],
  "bg": "Eterna_City_anime.png",
  "music":"Paradise.mp3"},
    {"id": 5,
  "name": "Unova",
  "indices": [493,649],
  "bg": "Accumula_Town_anime.png",
  "music":"Forest.mp3"},
    ]

# Thresholds
NOT_SHOW_NAME_TIME = 3000
LEGENDARY_CUTOFF = 580
NORMAL_POKEMON_CATCH_TIME = 9000
LEGENDARY_POKEMON_CATCH_TIME = 4000
PASS_MARK = 7
MAX_MISTAKE = 5
REWARD_MAP = {
            1: 100,
            2: 150,
            3: 200,
            4: 250,
            5: 300,
            6: 400,
            7: 500,
            8: 600,
            9: 800,
            10: 1000,
            11: 1200,
            12: 1400,
            13: 1600,
            14: 1800,
            15: 2000,
            16: 2200,
            17: 2400,
            18: 2600,
            19: 2800,
            20: 3000,
        }