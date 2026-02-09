import pygame
from pygame.locals import *
import sys
import json
import os
import random
import time
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants and global variables
SCREEN_WIDTH = 1275
SCREEN_HEIGHT = 700
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

# Game state variables
quest_notification_text = ""
quest_notification_time = 0
quest_notification_color = (0, 100, 0)  # Dark green
player_money = 30
character_name = ""
inventory = {"seeds": {}, "harvest": {}}
planted_seeds = []
equipped_item = None
dragging_seed = False
current_quests = []
completed_quests = []
show_achievements = False
achievement_notification = None
achievement_notification_time = 0
achievement_scroll_offset = 0
achievement_selected_category = "money"
carrotfest_active = False
carrotfest_end_time = 0
carrotfest_original_price = None
in_dialogue = False

# Initialize display
window_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Farming Game")

# Load images
def load_image(name, size=None):
    try:
        img = pygame.image.load(f"assets/{name}.png").convert_alpha()
        return pygame.transform.scale(img, size) if size else img
    except:
        # Create a placeholder if image fails to load
        surf = pygame.Surface(size or (64, 64))
        surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        return surf

# Load all game assets
welcome_img = pygame.transform.scale(load_image("WELCOME"), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_img = pygame.transform.scale(load_image("BACKGROUND"), (SCREEN_WIDTH, SCREEN_HEIGHT))
ending_img = pygame.transform.scale(load_image("ENDING"), (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = pygame.transform.scale(load_image("FarmerGirl"), (150, 200))

# Item images
item_images = {
    "Apple": load_image("SEEDAPPLE", (64, 64)),
    "Carrot": load_image("SEEDCARROT", (64, 64)),
    "Tomato": load_image("SEEDTOMATO", (64, 64)),
    "Banana": load_image("SEEDBANANA", (64, 64)),
    "Cacao": load_image("SEEDCACAO", (64, 64)),
    "Chili": load_image("SEEDCHILI", (64, 64)),
    "Cucumber": load_image("SEEDCUCUMBER", (64, 64)),
    "Eggplant": load_image("SEEDEGGPLANT", (64, 64)),
    "Grape": load_image("SEEDGRAPE", (64, 64)),
    "Lemon": load_image("SEEDLEMON", (64, 64)),
    "Lime": load_image("SEEDLIME", (64, 64)),
    "Mango": load_image("SEEDMANGO", (64, 64)),
    "Orange": load_image("SEEDORANGE", (64, 64)),
    "Pineapple": load_image("SEEDPINEAPPLE", (64, 64)),
    "Potato": load_image("SEEDPOTATO", (64, 64)),
    "Strawberry": load_image("SEEDSTRAWBERRY", (64, 64)),
    "Vanilla": load_image("SEEDVANILLA", (64, 64)),
    "Watermelon": load_image("SEEDWATERMELON", (64, 64))
}

grown_images = {
    "Apple": load_image("APPLE", (64, 64)),
    "Carrot": load_image("CARROT", (64, 64)),
    "Tomato": load_image("TOMATO", (64, 64)),
    "Banana": load_image("BANANA", (64, 64)),
    "Cacao": load_image("CACAO", (64, 64)),
    "Chili": load_image("CHILI", (64, 64)),
    "Cucumber": load_image("CUCUMBER", (64, 64)),
    "Eggplant": load_image("EGGPLANT", (64, 64)),
    "Grape": load_image("GRAPE", (64, 64)),
    "Lemon": load_image("LEMON", (64, 64)),
    "Lime": load_image("LIME", (64, 64)),
    "Mango": load_image("MANGO", (64, 64)),
    "Orange": load_image("ORANGE", (64, 64)),
    "Pineapple": load_image("PINEAPPLE", (64, 64)),
    "Potato": load_image("POTATO", (64, 64)),
    "Strawberry": load_image("STRAWBERRY", (64, 64)),
    "Vanilla": load_image("VANILLA", (64, 64)),
    "Watermelon": load_image("WATERMELON", (64, 64))
}

# Fonts
font = pygame.font.SysFont("arial", 24)
large_font = pygame.font.SysFont("arial", 32)
title_font = pygame.font.SysFont("arial", 48, bold=True)

# Player setup
player_rect = pygame.Rect(435, 350, 150, 200)
player_speed = 10

# Market items
market_items = [
    {"name": "Apple", "stock_chance": 100, "buy": 10, "sell": 25},
    {"name": "Carrot", "stock_chance": 99, "buy": 15, "sell": 30},
    {"name": "Tomato", "stock_chance": 95, "buy": 20, "sell": 50},
    {"name": "Eggplant", "stock_chance": 80, "buy": 50, "sell": 110},
    {"name": "Potato", "stock_chance": 75, "buy": 60, "sell": 130},
    {"name": "Banana", "stock_chance": 70, "buy": 75, "sell": 150},
    {"name": "Chili", "stock_chance": 70, "buy": 80, "sell": 175},
    {"name": "Cucumber", "stock_chance": 60, "buy": 150, "sell": 400},
    {"name": "Lemon", "stock_chance": 60, "buy": 160, "sell": 415},
    {"name": "Lime", "stock_chance": 55, "buy": 180, "sell": 440},
    {"name": "Orange", "stock_chance": 50, "buy": 200, "sell": 480},
    {"name": "Strawberry", "stock_chance": 40, "buy": 350, "sell": 690},
    {"name": "Mango", "stock_chance": 35, "buy": 400, "sell": 800},
    {"name": "Grape", "stock_chance": 35, "buy": 420, "sell": 888},
    {"name": "Pineapple", "stock_chance": 25, "buy": 600, "sell": 1100},
    {"name": "Watermelon", "stock_chance": 20, "buy": 650, "sell": 1250},
    {"name": "Vanilla", "stock_chance": 10, "buy": 900, "sell": 2000},
    {"name": "Cacao", "stock_chance": 5, "buy": 2000, "sell": 5000},
]

# Grow times
grow_times = {
    "Apple": 15,
    "Carrot": 20,
    "Tomato": 30,
    "Eggplant": 30,
    "Potato": 35,
    "Banana": 45,
    "Chili": 30,
    "Cucumber": 45,
    "Lemon": 20,
    "Lime": 20,
    "Orange": 60,
    "Strawberry": 45,
    "Mango": 90,
    "Grape": 120,
    "Pineapple": 210,
    "Watermelon": 210,
    "Vanilla": 55,
    "Cacao": 420
}

# Quests
quests = [
    {
        "id": 1,
        "title": "First Harvest",
        "description": "Grow and collect 3 Apples",
        "required_item": "Apple",
        "required_count": 3,
        "reward_money": 50,
        "reward_items": [],
        "completed": False,
        "active": False
    },
    {
        "id": 2,
        "title": "Profit Maker",
        "description": "Earn $5000 from selling crops",
        "required_money": 5000,
        "reward_money": 15000,
        "reward_items": [("Vanilla", 5)],
        "completed": False,
        "active": False
    },
    {
        "id": 3,
        "title": "Variety Grower",
        "description": "Grow 10 different crop types",
        "required_types": 10,
        "reward_money": 2500,
        "reward_items": [("Watermelon", 1)],
        "completed": False,
        "active": False
    }
]

# Achievements
achievements = {
    "money": [
        {"threshold": 1000, "title": "Thousands", "unlocked": False, "desc": "Reach $1,000"},
        {"threshold": 10000, "title": "Ten Thousands", "unlocked": False, "desc": "Reach $10,000"},
        {"threshold": 100000, "title": "Hundred Thousands", "unlocked": False, "desc": "Reach $100,000"},
        {"threshold": 1000000, "title": "Millionaire", "unlocked": False, "desc": "Reach $1,000,000"},
        {"threshold": 10000000, "title": "10x Millionaire", "unlocked": False, "desc": "Reach $10,000,000"},
        {"threshold": 100000000, "title": "100x Millionaire", "unlocked": False, "desc": "Reach $100,000,000"},
        {"threshold": 1000000000, "title": "Billionaire", "unlocked": False, "desc": "Reach $1,000,000,000"},
        {"threshold": 10000000000, "title": "10x Billionaire", "unlocked": False, "desc": "Reach $10,000,000,000"},
        {"threshold": 100000000000, "title": "100x Billionaire", "unlocked": False, "desc": "Reach $100,000,000,000"}
    ],
    "purchases": [
        {"item": "Tomato", "target": 100, "title": "Tomato Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Tomatoes"},
        {"item": "Carrot", "target": 100, "title": "Carrot Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Carrots"},
        {"item": "Banana", "target": 100, "title": "Banana Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Bananas"},
        {"item": "Apple", "target": 100, "title": "Apple Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Apples"},
        {"item": "Cacao", "target": 100, "title": "Chocolate Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Cacao"},
        {"item": "Chili", "target": 100, "title": "Spicy Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Chilies"},
        {"item": "Cucumber", "target": 100, "title": "Cucumber Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Cucumbers"},
        {"item": "Eggplant", "target": 100, "title": "Eggplant Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Eggplants"},
        {"item": "Grape", "target": 100, "title": "Grape Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Grapes"},
        {"item": "Lemon", "target": 100, "title": "Lemon Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Lemons"},
        {"item": "Lime", "target": 100, "title": "Lime Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Limes"},
        {"item": "Mango", "target": 100, "title": "Mango Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Mangos"},
        {"item": "Orange", "target": 100, "title": "Orange Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Oranges"},
        {"item": "Pineapple", "target": 100, "title": "Spongebob Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Pineapples"},
        {"item": "Potato", "target": 100, "title": "Potato Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Potatoes"},
        {"item": "Strawberry", "target": 100, "title": "Strawberry Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Strawberries"},
        {"item": "Vanilla", "target": 100, "title": "Vanilla Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Vanilla"},
        {"item": "Watermelon", "target": 100, "title": "Watermelon Lover", "unlocked": False, "current": 0, "desc": "Buy 100 Watermelons"}
    ]
}

# Save slots
save_slots = {
    1: "save_slot_1.json",
    2: "save_slot_2.json",
    3: "save_slot_3.json"
}

# NPC class
class NPC:
    def __init__(self, name, x, y):
        self.name = name
        self.rect = pygame.Rect(x, y, 60, 80)
        self.color = (100, 200, 100)
        self.text_color = (0, 0, 0)
        self.dialogue = {
            "greeting": f"Hello {character_name}! Need work?",
            "no_quests": "No quests available right now.",
            "quest_complete": "Thanks for your help!"
        }
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, black, self.rect, 2)
        
        head_center = (self.rect.x + self.rect.width//2, self.rect.y - 10)
        pygame.draw.circle(surface, (255, 200, 150), head_center, 20)
        pygame.draw.circle(surface, black, head_center, 20, 1)
        
        name_text = font.render(self.name, True, self.text_color)
        surface.blit(name_text, (self.rect.x + self.rect.width//2 - name_text.get_width()//2, 
                                self.rect.y - 40))

# Create NPCs
farmer_joe = NPC("Farmer Joe", 200, 300)
merchant_mary = NPC("Merchant Mary", 800, 400)
npc_list = [farmer_joe, merchant_mary]

# Helper functions
def draw_button(surface, rect, text, font, bg_color, text_color, border_color=None):
    pygame.draw.rect(surface, bg_color, rect, border_radius=5)
    if border_color:
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=5)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def show_notification(message, color=(0, 100, 0)):
    global quest_notification_text, quest_notification_time, quest_notification_color
    quest_notification_text = message
    quest_notification_time = time.time()
    quest_notification_color = color
    
def draw_notification():
    current_time = time.time()
    if quest_notification_text and current_time - quest_notification_time < 3:
        notification_font = pygame.font.SysFont("arial", 28, bold=True)
        text = notification_font.render(quest_notification_text, True, quest_notification_color)
        shadow = notification_font.render(quest_notification_text, True, black)
        
        pos_x = SCREEN_WIDTH // 2 - text.get_width() // 2
        window_screen.blit(shadow, (pos_x + 2, 102))
        window_screen.blit(text, (pos_x, 100))

def draw_achievement_notification():
    if achievement_notification and time.time() - achievement_notification_time < 3:
        notif_font = pygame.font.SysFont("arial", 32, bold=True)
        text = notif_font.render(achievement_notification, True, (255, 215, 0))
        shadow = notif_font.render(achievement_notification, True, black)
        
        pos_x = SCREEN_WIDTH // 2 - text.get_width() // 2
        window_screen.blit(shadow, (pos_x + 2, 52))
        window_screen.blit(text, (pos_x, 50))
        
        if random.random() < 0.1:
            pygame.draw.circle(window_screen, (255, 255, 0), 
                                (random.randint(0, SCREEN_WIDTH), random.randint(0, 100)), 
                                random.randint(2, 5))

def move_character(speed):
    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        if player_rect.top > 0:
            player_rect.y -= speed
    if keys[K_s] or keys[K_DOWN]:
        if player_rect.bottom < SCREEN_HEIGHT:
            player_rect.y += speed
    if keys[K_a] or keys[K_LEFT]:
        if player_rect.left > 0:
            player_rect.x -= speed
    if keys[K_d] or keys[K_RIGHT]:
        if player_rect.right < SCREEN_WIDTH:
            player_rect.x += speed

def draw_planted_seeds():
    current_time = time.time()
    for seed, pos, plant_time in planted_seeds:
        base_fruit = seed.replace(" (Snow Fruit)", "")
        grow_time = grow_times.get(base_fruit, 30)
        time_passed = current_time - plant_time
        
        if time_passed >= grow_time:
            img = grown_images.get(base_fruit, None)
        else:
            img = item_images.get(base_fruit, None)
        
        if img:
            window_screen.blit(img, (pos[0] - 32, pos[1] - 32))

def check_and_collect_grown_fruit():
    global planted_seeds
    current_time = time.time()
    new_plants = []
    harvested_items = []
    
    for seed, pos, plant_time in planted_seeds:
        base_fruit = seed.replace(" (Snow Fruit)", "")
        grow_time = grow_times.get(base_fruit, 30)
        
        if current_time - plant_time >= grow_time:
            harvested_items.append(base_fruit)
        else:
            new_plants.append((seed, pos, plant_time))
    
    planted_seeds = new_plants
    
    for item in harvested_items:
        inventory["harvest"][item] = inventory["harvest"].get(item, 0) + 1
    
    if harvested_items:
        unique_counts = {}
        for item in harvested_items:
            unique_counts[item] = unique_counts.get(item, 0) + 1
        
        if len(unique_counts) == 1:
            item, count = next(iter(unique_counts.items()))
            show_notification(f"Harvested {count} {item}!")
        else:
            total_count = len(harvested_items)
            show_notification(f"Harvested {total_count} crops!")

def sell_crops():
    global player_money
    total_value = 0
    sold_items = {}
    
    for item, count in inventory["harvest"].items():
        base_item = item.replace(" (Snow Fruit)", "")
        sell_price = 0
        
        for market_item in market_items:
            if market_item["name"] == base_item:
                if "(Snow Fruit)" in item:
                    sell_price = int(market_item["sell"] * random.uniform(1.15, 3.0))
                else:
                    sell_price = market_item["sell"]
                break
        
        total_value += sell_price * count
        sold_items[item] = count
    
    if total_value > 0:
        player_money += total_value
        for item in sold_items:
            del inventory["harvest"][item]
        show_notification(f"Sold crops for ${total_value}")
    else:
        show_notification("No crops to sell!")

def check_quest_progress():
    for quest in current_quests[:]:
        if "required_item" in quest:
            if inventory.get("harvest", {}).get(quest["required_item"], 0) >= quest["required_count"]:
                complete_quest(quest)
        elif "required_money" in quest:
            if player_money >= quest["required_money"]:
                complete_quest(quest)
        elif "required_types" in quest:
            unique_crops = set()
            for seed, _, _ in planted_seeds:
                base_fruit = seed.replace(" (Snow Fruit)", "")
                unique_crops.add(base_fruit)
            if len(unique_crops) >= quest["required_types"]:
                complete_quest(quest)

def complete_quest(quest):
    global player_money, current_quests, completed_quests
    
    player_money += quest.get("reward_money", 0)
    
    for item, count in quest.get("reward_items", []):
        inventory["seeds"][item] = inventory["seeds"].get(item, 0) + count
    
    quest["completed"] = True
    quest["active"] = False
    current_quests.remove(quest)
    completed_quests.append(quest)
    
    show_notification(f"Quest complete! +${quest.get('reward_money', 0)}")

def start_quest(quest_id):
    global current_quests
    quest = next((q for q in quests if q["id"] == quest_id), None)
    if quest and not quest["completed"] and not quest["active"]:
        quest["active"] = True
        current_quests.append(quest)
        show_notification(f"Quest started: {quest['title']}")

def get_quest_progress_text(quest):
    if "required_item" in quest:
        current = inventory.get("harvest", {}).get(quest["required_item"], 0)
        return f"{current}/{quest['required_count']} {quest['required_item']}"
    elif "required_money" in quest:
        current = min(player_money, quest["required_money"])
        return f"${current:,}/${quest['required_money']:,}"
    elif "required_types" in quest:
        unique_crops = set()
        for seed, _, _ in planted_seeds:
            base_fruit = seed.replace(" (Snow Fruit)", "")
            unique_crops.add(base_fruit)
        return f"{len(unique_crops)}/{quest['required_types']} types"
    return ""

def draw_npc_indicators():
    for npc in npc_list:
        if (abs(player_rect.x - npc.rect.x) < 150 and 
            abs(player_rect.y - npc.rect.y) < 150):
            pulse = int(10 * abs(math.sin(time.time() * 2)))
            talk_rect = pygame.Rect(npc.rect.x + npc.rect.width//2 - 15, 
                                   npc.rect.y - 50, 
                                   30 + pulse, 20 + pulse)
            pygame.draw.rect(window_screen, (255, 255, 0), talk_rect)
            pygame.draw.rect(window_screen, black, talk_rect, 2)
            
            talk_text = font.render("T", True, black)
            window_screen.blit(talk_text, (talk_rect.centerx - talk_text.get_width()//2, 
                                         talk_rect.centery - talk_text.get_height()//2))

def generate_market_items():
    global carrotfest_active, carrotfest_end_time, carrotfest_original_price
    
    available = []
    for item in market_items:
        if random.random() <= item.get("stock_chance", 100) / 100:
            available.append(item)
    
    if not carrotfest_active and random.random() < 0.2:
        carrotfest_active = True
        carrotfest_end_time = time.time() + 120
        for item in market_items:
            if item["name"] == "Carrot":
                carrotfest_original_price = item["sell"]
                item["sell"] = 200
                break
    
    if carrotfest_active and time.time() > carrotfest_end_time:
        carrotfest_active = False
        for item in market_items:
            if item["name"] == "Carrot":
                item["sell"] = carrotfest_original_price
                break
    
    if random.random() < 0.25:
        available.append({
            "name": "Legendary Ticket", 
            "buy": 50000, 
            "sell": 0,
            "stock_chance": 100
        })
    
    return random.sample(available, min(9, len(available)))

def open_market():
    global player_money, inventory, equipped_item
    
    items = generate_market_items()
    active = True
    selected_item = None
    buy_quantity = 1
    
    while active:
        window_screen.fill((50, 50, 70))
        
        # Draw title
        title_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 70)
        pygame.draw.rect(window_screen, (70, 70, 90), title_rect)
        title_text = title_font.render("MARKET", True, white)
        window_screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 20))
        
        # Draw money
        money_text = large_font.render(f"Money: ${player_money:,}", True, (200, 200, 100))
        window_screen.blit(money_text, (SCREEN_WIDTH - money_text.get_width() - 20, 25))
        
        # Draw items grid
        item_rects = []
        for i, item in enumerate(items[:9]):
            row = i // 3
            col = i % 3
            x = 50 + col * 400
            y = 100 + row * 200
            rect = pygame.Rect(x, y, 380, 180)
            item_rects.append((rect, item))
            
            is_selected = item == selected_item
            card_color = (150, 200, 255) if is_selected else (90, 90, 110)
            pygame.draw.rect(window_screen, card_color, rect, border_radius=10)
            pygame.draw.rect(window_screen, (150, 150, 170), rect, 2, border_radius=10)
            
            if item["name"] in item_images:
                window_screen.blit(item_images[item["name"]], (x + 20, y + 20))
            
            name_text = font.render(item["name"], True, white)
            window_screen.blit(name_text, (x + 120, y + 20))
            
            buy_text = font.render(f"Buy: ${item['buy']}", True, (150, 255, 150))
            window_screen.blit(buy_text, (x + 120, y + 50))
            
            sell_text = font.render(f"Sell: ${item['sell']}", True, (255, 150, 150))
            window_screen.blit(sell_text, (x + 120, y + 80))
            
            if "stock_chance" in item:
                stock_text = font.render(f"Stock: {item['stock_chance']}%", True, (200, 200, 255))
                window_screen.blit(stock_text, (x + 120, y + 110))
        
        # Draw purchase panel if item selected
        if selected_item:
            panel_rect = pygame.Rect(50, 550, SCREEN_WIDTH - 100, 120)
            pygame.draw.rect(window_screen, (70, 70, 90), panel_rect, border_radius=10)
            pygame.draw.rect(window_screen, (100, 100, 120), panel_rect, 2, border_radius=10)
            
            max_affordable = player_money // selected_item['buy'] if selected_item['buy'] > 0 else 1
            buy_quantity = min(buy_quantity, max_affordable)
            
            selected_text = large_font.render(f"Selected: {selected_item['name']}", True, white)
            window_screen.blit(selected_text, (panel_rect.x + 20, panel_rect.y + 20))
            
            qty_text = large_font.render(f"Quantity: {buy_quantity}", True, white)
            window_screen.blit(qty_text, (panel_rect.x + 20, panel_rect.y + 60))
            
            # Quantity buttons
            dec_rect = pygame.Rect(panel_rect.x + 200, panel_rect.y + 60, 40, 40)
            dec_color = (100, 200, 100) if buy_quantity > 1 else (100, 100, 100)
            draw_button(window_screen, dec_rect, "-", large_font, dec_color, white, (50, 150, 50))
            
            inc_rect = pygame.Rect(panel_rect.x + 260, panel_rect.y + 60, 40, 40)
            inc_color = (100, 200, 100) if buy_quantity < max_affordable else (100, 100, 100)
            draw_button(window_screen, inc_rect, "+", large_font, inc_color, white, (50, 150, 50))
            
            # Buy button
            buy_rect = pygame.Rect(panel_rect.x + 320, panel_rect.y + 60, 200, 40)
            can_buy = max_affordable >= 1 and buy_quantity > 0
            buy_color = (100, 200, 100) if can_buy else (100, 100, 100)
            draw_button(window_screen, buy_rect, f"Buy (${selected_item['buy'] * buy_quantity})", 
                        large_font, buy_color, white, (50, 150, 50))
        
        # Close button
        close_rect = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70, 100, 40)
        draw_button(window_screen, close_rect, "Close", large_font, (200, 80, 80), white, (150, 50, 50))
        
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    active = False
                elif event.key == K_LEFT and selected_item and buy_quantity > 1:
                    buy_quantity -= 1
                elif event.key == K_RIGHT and selected_item and buy_quantity < max_affordable:
                    buy_quantity += 1
                elif event.key == K_RETURN and selected_item and can_buy:
                    process_purchase(selected_item, buy_quantity)
                    selected_item = None
                    buy_quantity = 1
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if selected_item:
                    if 'dec_rect' in locals() and dec_rect.collidepoint(mouse_pos) and buy_quantity > 1:
                        buy_quantity -= 1
                        continue
                    
                    if 'inc_rect' in locals() and inc_rect.collidepoint(mouse_pos) and buy_quantity < max_affordable:
                        buy_quantity += 1
                        continue
                    
                    if 'buy_rect' in locals() and buy_rect.collidepoint(mouse_pos) and can_buy:
                        process_purchase(selected_item, buy_quantity)
                        selected_item = None
                        buy_quantity = 1
                        continue
                
                if close_rect.collidepoint(mouse_pos):
                    active = False
                    continue
                
                for rect, item in item_rects:
                    if rect.collidepoint(mouse_pos):
                        selected_item = item
                        buy_quantity = 1
                        break

def process_purchase(item, quantity):
    global player_money, inventory, achievement_notification, achievement_notification_time
    
    total_cost = item['buy'] * quantity
    if player_money >= total_cost and quantity > 0:
        player_money -= total_cost
        inventory["seeds"][item["name"]] = inventory["seeds"].get(item["name"], 0) + quantity
        
        # Update purchase achievements
        update_purchase_achievements(item["name"], quantity)
        
        # 20% chance for bonus snow fruit seed
        if random.random() < 0.20:
            snow_data = generate_snow_fruit_data(item["name"])
            if snow_data:
                inventory["seeds"][snow_data["name"]] = inventory["seeds"].get(snow_data["name"], 0) + 1
                show_notification(f"Got bonus {snow_data['name']} seed!")

def generate_snow_fruit_data(base_item_name):
    for item in market_items:
        if item["name"] == base_item_name:
            original_price = item["sell"]
            price_multiplier = random.uniform(1.15, 3.0)
            boosted_price = int(original_price * price_multiplier)
            
            return {
                "name": f"{base_item_name} (Snow Fruit)",
                "stock_chance": 0,
                "buy": 0,
                "sell": boosted_price,
                "original_image": base_item_name
            }
    return None

def update_purchase_achievements(item_name, quantity):
    global achievement_notification, achievement_notification_time
    
    base_item = item_name.replace(" (Snow Fruit)", "")
    
    for achievement in achievements["purchases"]:
        if achievement["item"] == base_item and not achievement["unlocked"]:
            achievement["current"] += quantity
            if achievement["current"] >= achievement["target"]:
                achievement["unlocked"] = True
                achievement_notification = f"Achievement Unlocked: {achievement['title']}!"
                achievement_notification_time = time.time()

def check_achievements():
    global achievement_notification, achievement_notification_time
    
    for achievement in achievements["money"]:
        if not achievement["unlocked"] and player_money >= achievement["threshold"]:
            achievement["unlocked"] = True
            achievement_notification = f"Achievement Unlocked: {achievement['title']}!"
            achievement_notification_time = time.time()

def open_inventory():
    global equipped_item, inventory
    
    active = True
    selected_tab = "seeds"  # "seeds" or "harvest"
    
    while active:
        window_screen.fill((50, 50, 70))
        
        # Draw title
        title_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 70)
        pygame.draw.rect(window_screen, (70, 70, 90), title_rect)
        title_text = title_font.render("INVENTORY", True, white)
        window_screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 20))
        
        # Draw tabs
        seeds_tab = pygame.Rect(SCREEN_WIDTH//2 - 200, 90, 150, 40)
        harvest_tab = pygame.Rect(SCREEN_WIDTH//2 + 50, 90, 150, 40)
        
        draw_button(window_screen, seeds_tab, "SEEDS", large_font, 
                   (100, 150, 200) if selected_tab == "seeds" else (70, 70, 90), 
                   white, (100, 100, 120))
        
        draw_button(window_screen, harvest_tab, "HARVEST", large_font, 
                   (100, 150, 200) if selected_tab == "harvest" else (70, 70, 90), 
                   white, (100, 100, 120))
        
        # Draw items
        items = inventory.get(selected_tab, {})
        start_x = 50
        start_y = 150
        item_width = 120
        item_height = 140
        padding = 15
        cols = (SCREEN_WIDTH - 100) // (item_width + padding)
        
        for i, (item_name, count) in enumerate(items.items()):
            row = i // cols
            col = i % cols
            x = start_x + col * (item_width + padding)
            y = start_y + row * (item_height + padding)
            rect = pygame.Rect(x, y, item_width, item_height)
            
            is_equipped = (selected_tab == "seeds" and equipped_item == item_name)
            card_color = (150, 200, 255) if is_equipped else (90, 90, 110)
            
            pygame.draw.rect(window_screen, card_color, rect, border_radius=10)
            pygame.draw.rect(window_screen, (150, 150, 170), rect, 2, border_radius=10)
            
            # Draw item image
            base_item = item_name.replace(" (Snow Fruit)", "")
            img = item_images.get(base_item, None) if selected_tab == "seeds" else grown_images.get(base_item, None)
            if img:
                window_screen.blit(img, (x + item_width//2 - 32, y + 10))
            
            # Draw item name and count
            name_text = font.render(base_item, True, white)
            window_screen.blit(name_text, (x + item_width//2 - name_text.get_width()//2, y + 80))
            
            count_text = font.render(f"x{count}", True, white)
            window_screen.blit(count_text, (x + item_width//2 - count_text.get_width()//2, y + 110))
        
        # Close button
        close_rect = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70, 100, 40)
        draw_button(window_screen, close_rect, "Close", large_font, (200, 80, 80), white, (150, 50, 50))
        
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    active = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if seeds_tab.collidepoint(mouse_pos):
                    selected_tab = "seeds"
                elif harvest_tab.collidepoint(mouse_pos):
                    selected_tab = "harvest"
                elif close_rect.collidepoint(mouse_pos):
                    active = False
                else:
                    # Check for item clicks
                    for i, (item_name, count) in enumerate(items.items()):
                        row = i // cols
                        col = i % cols
                        x = start_x + col * (item_width + padding)
                        y = start_y + row * (item_height + padding)
                        rect = pygame.Rect(x, y, item_width, item_height)
                        
                        if rect.collidepoint(mouse_pos):
                            if selected_tab == "seeds":
                                equipped_item = item_name if equipped_item != item_name else None
                            break

def draw_achievement_menu():
    global show_achievements, achievement_scroll_offset, achievement_selected_category
    
    # Store events to process later
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        events.append(event)
    
    # Dark overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    window_screen.blit(overlay, (0, 0))
    
    # Main panel
    panel_rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
    pygame.draw.rect(window_screen, (70, 70, 90), panel_rect, border_radius=15)
    pygame.draw.rect(window_screen, (100, 100, 120), panel_rect, 3, border_radius=15)
    
    # Title
    title_text = title_font.render("ACHIEVEMENTS", True, white)
    window_screen.blit(title_text, (panel_rect.centerx - title_text.get_width() // 2, panel_rect.y + 30))
    
    # Category tabs
    tabs = {
        "money": "WEALTH",
        "purchases": "PURCHASES"
    }
    
    tab_x = panel_rect.x + 50
    mouse_clicked = False
    
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True
    
    for category, name in tabs.items():
        tab_rect = pygame.Rect(tab_x, panel_rect.y + 90, 150, 40)
        tab_color = (100, 150, 200) if category == achievement_selected_category else (70, 70, 90)
        draw_button(window_screen, tab_rect, name, large_font, tab_color, white, (120, 120, 140))
        
        if mouse_clicked and tab_rect.collidepoint(pygame.mouse.get_pos()):
            achievement_selected_category = category
            achievement_scroll_offset = 0
        
        tab_x += 160
    
    # Draw achievements
    clip_rect = pygame.Rect(panel_rect.x + 20, panel_rect.y + 140, panel_rect.width - 40, panel_rect.height - 160)
    window_screen.set_clip(clip_rect)
    
    current_achievements = achievements[achievement_selected_category]
    y_pos = panel_rect.y + 140 - achievement_scroll_offset
    
    for achievement in current_achievements:
        if y_pos + 70 > panel_rect.y + 140 and y_pos < panel_rect.bottom - 20:
            ach_rect = pygame.Rect(panel_rect.x + 20, y_pos, panel_rect.width - 40, 60)
            color = (100, 150, 100) if achievement["unlocked"] else (60, 60, 80)
            pygame.draw.rect(window_screen, color, ach_rect, border_radius=8)
            pygame.draw.rect(window_screen, (120, 120, 140), ach_rect, 2, border_radius=8)
            
            # Icon
            icon = "✓" if achievement["unlocked"] else "?"
            icon_text = font.render(icon, True, (255, 255, 0) if achievement["unlocked"] else (150, 150, 150))
            window_screen.blit(icon_text, (ach_rect.x + 15, ach_rect.centery - icon_text.get_height()//2))
            
            # Achievement info
            title_text = font.render(achievement["title"], True, white)
            window_screen.blit(title_text, (ach_rect.x + 50, ach_rect.y + 10))
            
            desc_text = font.render(achievement["desc"], True, (200, 200, 200))
            window_screen.blit(desc_text, (ach_rect.x + 50, ach_rect.y + 30))
            
            # Progress
            if achievement_selected_category == "money":
                progress = min(1, player_money / achievement["threshold"])
                progress_text = f"${player_money:,}/${achievement['threshold']:,}"
            else:
                progress = min(1, achievement["current"] / achievement["target"])
                progress_text = f"{achievement['current']}/{achievement['target']} {achievement['item']}"
            
            # Progress bar
            pygame.draw.rect(window_screen, (50, 50, 70), (ach_rect.x + 50, ach_rect.bottom - 15, ach_rect.width - 70, 8))
            pygame.draw.rect(window_screen, (100, 200, 100), (ach_rect.x + 50, ach_rect.bottom - 15, (ach_rect.width - 70) * progress, 8))
            
            # Progress text
            progress_text_surface = font.render(progress_text, True, white)
            window_screen.blit(progress_text_surface, (ach_rect.right - progress_text_surface.get_width() - 10, ach_rect.centery - progress_text_surface.get_height()//2))
        
        y_pos += 70
    
    window_screen.set_clip(None)
    
    # Draw scroll bar if needed
    content_height = len(current_achievements) * 70
    visible_height = panel_rect.height - 160
    if content_height > visible_height:
        scrollbar_width = 10
        scrollbar_x = panel_rect.right - scrollbar_width - 10
        scrollbar_height = visible_height * (visible_height / content_height)
        scrollbar_pos = (achievement_scroll_offset / (content_height - visible_height)) * (visible_height - scrollbar_height)
        
        pygame.draw.rect(window_screen, (100, 100, 120), (scrollbar_x, panel_rect.y + 140, scrollbar_width, visible_height), border_radius=5)
        pygame.draw.rect(window_screen, (150, 150, 170), (scrollbar_x, panel_rect.y + 140 + scrollbar_pos, scrollbar_width, scrollbar_height), border_radius=5)
    
    # Close hint
    hint_text = font.render("Press P or ESC to close", True, (150, 150, 150))
    window_screen.blit(hint_text, (panel_rect.centerx - hint_text.get_width() // 2, panel_rect.bottom - 40))
    
    # Check for exit input
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                show_achievements = False
                return
        elif event.type == pygame.MOUSEWHEEL:
            achievement_scroll_offset -= event.y * 30
            max_scroll = max(0, len(achievements[achievement_selected_category]) * 70 - (panel_rect.height - 160))
            achievement_scroll_offset = max(0, min(achievement_scroll_offset, max_scroll))

def interact_with_npc(npc):
    global in_dialogue
    
    available_quests = [q for q in quests if not q["completed"] and not q["active"]]
    active = True
    
    while active:
        window_screen.blit(background_img, (0, 0))
        draw_game_world()
        
        # Draw dialogue box
        dialogue_rect = pygame.Rect(150, 400, SCREEN_WIDTH - 300, 200)
        pygame.draw.rect(window_screen, (250, 250, 200), dialogue_rect, border_radius=10)
        pygame.draw.rect(window_screen, black, dialogue_rect, 3, border_radius=10)
        
        text_y = dialogue_rect.y + 20
        
        if not available_quests:
            text = large_font.render(npc.dialogue["no_quests"], True, black)
            window_screen.blit(text, (dialogue_rect.x + 20, text_y))
        else:
            greeting_lines = npc.dialogue["greeting"].split('\n')
            for line in greeting_lines:
                text = large_font.render(line, True, black)
                window_screen.blit(text, (dialogue_rect.x + 20, text_y))
                text_y += 30
            
            text_y += 10
            for i, quest in enumerate(available_quests[:3]):
                quest_rect = pygame.Rect(dialogue_rect.x + 30, text_y, dialogue_rect.width - 60, 40)
                difficulty_color = (200, 230, 200) if "Apple" in quest["title"] else (230, 200, 200)
                draw_button(window_screen, quest_rect, quest["title"], large_font, difficulty_color, black)
                text_y += 50
        
        # Exit button
        exit_rect = pygame.Rect(dialogue_rect.right - 100, dialogue_rect.bottom - 50, 80, 40)
        draw_button(window_screen, exit_rect, "Exit", large_font, (230, 150, 150), black)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    active = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if available_quests:
                    for i, quest in enumerate(available_quests[:3]):
                        quest_rect = pygame.Rect(dialogue_rect.x + 30, dialogue_rect.y + 80 + i*50, 
                                                dialogue_rect.width - 60, 40)
                        if quest_rect.collidepoint(mouse_pos):
                            start_quest(quest["id"])
                            active = False
                
                if exit_rect.collidepoint(mouse_pos):
                    active = False
    
    in_dialogue = False

def name_character_screen():
    global character_name
    
    input_text = ""
    active = False
    error_message = ""
    
    while True:
        window_screen.fill((50, 50, 70))
        
        # Title
        title_text = title_font.render("FARMER'S NAME", True, white)
        window_screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 150))
        
        # Prompt
        prompt_text = large_font.render("Enter your character's name:", True, white)
        window_screen.blit(prompt_text, (SCREEN_WIDTH//2 - prompt_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
        
        # Input box
        input_box = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2, 400, 50)
        color = (100, 200, 255) if active else (150, 150, 170)
        pygame.draw.rect(window_screen, color, input_box, 2, border_radius=5)
        pygame.draw.rect(window_screen, (60, 60, 80), input_box, border_radius=5)
        
        # Input text
        text_surface = large_font.render(input_text, True, white)
        window_screen.blit(text_surface, (input_box.x + 15, input_box.y + 10))
        
        # Cursor
        if active and time.time() % 1 > 0.5:
            cursor_pos = large_font.size(input_text)[0] + input_box.x + 15
            pygame.draw.line(window_screen, white, (cursor_pos, input_box.y + 10), (cursor_pos, input_box.y + 40), 2)
        
        # Error message
        if error_message:
            error_text = font.render(error_message, True, (255, 100, 100))
            window_screen.blit(error_text, (SCREEN_WIDTH//2 - error_text.get_width()//2, input_box.y + 60))
        
        # Hint
        hint_text = font.render("(2-16 characters, letters and numbers only)", True, (150, 150, 150))
        window_screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, input_box.y - 30))
        
        # Continue button (only enabled if valid name)
        if len(input_text.strip()) >= 2 and len(input_text.strip()) <= 16:
            button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 80, 200, 50)
            draw_button(window_screen, button_rect, "Continue", large_font, (100, 200, 100), white, (50, 150, 50))
        else:
            button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 80, 200, 50)
            draw_button(window_screen, button_rect, "Continue", large_font, (100, 100, 100), (150, 150, 150), (50, 50, 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                
                if button_rect.collidepoint(event.pos) and len(input_text.strip()) >= 2 and len(input_text.strip()) <= 16:
                    character_name = input_text.strip()
                    return
            elif event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN and len(input_text.strip()) >= 2 and len(input_text.strip()) <= 16:
                        character_name = input_text.strip()
                        return
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif len(input_text) < 16 and event.unicode.isprintable():
                        input_text += event.unicode

def draw_game_world():
    window_screen.blit(background_img, (0, 0))
    draw_planted_seeds()
    window_screen.blit(player_img, (player_rect.x, player_rect.y))
    for npc in npc_list:
        npc.draw(window_screen)
    draw_ui()

def draw_ui():
    # Player name
    name_text = font.render(character_name, True, black)
    window_screen.blit(name_text, (player_rect.x + player_rect.width//2 - name_text.get_width()//2, 
                                  player_rect.y - 25))
    
    # Money
    money_text = font.render(f"Money: ${player_money:,}", True, black)
    window_screen.blit(money_text, (20, 20))
    
    # Equipped item
    if equipped_item:
        equip_text = font.render(f"Equipped: {equipped_item}", True, black)
        window_screen.blit(equip_text, (20, 50))
    
    # Dragging seed
    if dragging_seed and equipped_item and equipped_item in item_images:
        window_screen.blit(item_images[equipped_item.replace(" (Snow Fruit)", "")], 
                         (pygame.mouse.get_pos()[0] - 32, pygame.mouse.get_pos()[1] - 32))
    
    # Events
    current_time = time.time()
    if carrotfest_active:
        remaining_time = max(0, carrotfest_end_time - current_time)
        fest_text = font.render(f"CARROTFEST! {int(remaining_time//60)}:{int(remaining_time%60):02d}", 
                              True, (255, 215, 0))
        window_screen.blit(fest_text, (SCREEN_WIDTH//2 - fest_text.get_width()//2, 10))
    
    # Quests
    if current_quests:
        tracker_y = SCREEN_HEIGHT - 70
        for i, quest in enumerate(current_quests[:3]):
            tracker_rect = pygame.Rect(20, tracker_y - (i * 60), 300, 50)
            pygame.draw.rect(window_screen, (200, 240, 200), tracker_rect)
            pygame.draw.rect(window_screen, black, tracker_rect, 2)
            
            quest_text = font.render(f"{quest['title']}: {get_quest_progress_text(quest)}", True, black)
            window_screen.blit(quest_text, (tracker_rect.x + 10, tracker_rect.y + 15))
    
    # Controls hint
    controls_text = font.render("Controls: M=Market, E=Inventory, F=Sell, SPACE=Harvest, P=Achievements, T=Talk", 
                              True, (100, 100, 100))
    window_screen.blit(controls_text, (SCREEN_WIDTH//2 - controls_text.get_width()//2, SCREEN_HEIGHT - 30))
    
    # Notifications
    draw_notification()
    draw_achievement_notification()
    draw_npc_indicators()

def dialogue_scene():
    global in_dialogue
    
    in_dialogue = True
    dialogues = [
        {"speaker": character_name, "text": "I must farm to get money so I can visit my father."},
        {"speaker": "Farmer Joe", "text": "Welcome to the valley! I can help you get started."},
        {"speaker": character_name, "text": "Thank you! I'll work hard to make my farm successful."},
        {"speaker": "Farmer Joe", "text": "Controls: M=Market, E=Inventory, F=Sell, SPACE=Harvest"}
    ]
    
    current_dialogue = 0
    
    while in_dialogue and current_dialogue < len(dialogues):
        draw_game_world()
        
        # Draw dialogue box
        text_box = pygame.Rect(100, SCREEN_HEIGHT - 250, SCREEN_WIDTH - 200, 200)
        pygame.draw.rect(window_screen, (250, 250, 200), text_box, border_radius=10)
        pygame.draw.rect(window_screen, black, text_box, 3, border_radius=10)
        
        # Speaker name
        speaker_text = large_font.render(f"{dialogues[current_dialogue]['speaker']}:", True, black)
        window_screen.blit(speaker_text, (text_box.x + 20, text_box.y + 20))
        
        # Wrapped text
        words = dialogues[current_dialogue]['text'].split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < text_box.width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        # Draw text (max 4 lines)
        for i, line in enumerate(lines[:4]):
            text_surface = font.render(line, True, black)
            window_screen.blit(text_surface, (text_box.x + 20, text_box.y + 60 + i*30))
        
        # Continue prompt
        continue_text = font.render("Press any key to continue...", True, (100, 100, 100))
        window_screen.blit(continue_text, (text_box.right - continue_text.get_width() - 20, text_box.bottom - 30))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    in_dialogue = False
                else:
                    current_dialogue += 1
            elif event.type == MOUSEBUTTONDOWN:
                current_dialogue += 1
    
    in_dialogue = False

def save_game(slot):
    """Save game data to a file"""
    try:
        data = {
            "character_name": character_name,
            "player_money": player_money,
            "inventory": inventory,
            "planted_seeds": planted_seeds,
            "achievements": achievements,
            "current_quests": current_quests,
            "completed_quests": completed_quests,
            "carrotfest_active": carrotfest_active,
            "carrotfest_end_time": carrotfest_end_time,
            "carrotfest_original_price": carrotfest_original_price
        }
        
        with open(save_slots[slot], "w") as f:
            json.dump(data, f, indent=4)
        show_notification(f"Game saved to slot {slot}")
    except Exception as e:
        show_notification(f"Failed to save: {str(e)}", (255, 0, 0))

def load_game(slot):
    """Load game data from a file"""
    global character_name, player_money, inventory, planted_seeds
    global achievements, current_quests, completed_quests
    global carrotfest_active, carrotfest_end_time, carrotfest_original_price
    
    try:
        if os.path.exists(save_slots[slot]):
            with open(save_slots[slot], "r") as f:
                data = json.load(f)
                
                # Load all game state variables
                character_name = data.get("character_name", "")
                player_money = data.get("player_money", 30)
                inventory = data.get("inventory", {"seeds": {}, "harvest": {}})
                planted_seeds = data.get("planted_seeds", [])
                achievements = data.get("achievements", achievements)
                current_quests = data.get("current_quests", [])
                completed_quests = data.get("completed_quests", [])
                carrotfest_active = data.get("carrotfest_active", False)
                carrotfest_end_time = data.get("carrotfest_end_time", 0)
                carrotfest_original_price = data.get("carrotfest_original_price", None)
                
                # Reconstruct planted seeds with current time if needed
                current_time = time.time()
                planted_seeds = [
                    (seed, pos, plant_time if plant_time > 0 else current_time)
                    for seed, pos, plant_time in planted_seeds
                ]
                
            show_notification(f"Game loaded from slot {slot}")
        else:
            show_notification(f"No save file in slot {slot}", (255, 0, 0))
    except Exception as e:
        show_notification(f"Failed to load: {str(e)}", (255, 0, 0))

def save_load_menu(is_saving=True):
    """Show save or load menu"""
    active = True
    
    while active:
        window_screen.fill((50, 50, 70))
        
        # Title
        title = "SAVE GAME" if is_saving else "LOAD GAME"
        title_text = title_font.render(title, True, white)
        window_screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Slot buttons
        slot_rects = []
        for i in range(1, 4):
            slot_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, 150 + (i-1)*120, 300, 80)
            slot_rects.append(slot_rect)
            
            # Check if save exists
            save_exists = os.path.exists(save_slots[i])
            
            # Different colors for existing/empty slots
            if is_saving:
                color = (100, 200, 100)  # Green for save slots
            else:
                color = (100, 200, 100) if save_exists else (100, 100, 100)  # Green if exists, gray if not
            
            pygame.draw.rect(window_screen, color, slot_rect, border_radius=10)
            pygame.draw.rect(window_screen, (150, 150, 170), slot_rect, 2, border_radius=10)
            
            # Slot text
            slot_text = large_font.render(f"Slot {i}", True, white)
            window_screen.blit(slot_text, (slot_rect.centerx - slot_text.get_width()//2, 
                                        slot_rect.centery - 20))
            
            # Additional info for load menu
            if not is_saving and save_exists:
                try:
                    with open(save_slots[i], "r") as f:
                        data = json.load(f)
                        name = data.get("character_name", "Unknown")
                        money = data.get("player_money", 0)
                        info_text = font.render(f"{name} - ${money:,}", True, white)
                        window_screen.blit(info_text, (slot_rect.centerx - info_text.get_width()//2, 
                                                     slot_rect.centery + 10))
                except:
                    pass
        
        # Back button
        back_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50)
        draw_button(window_screen, back_rect, "Back", large_font, (200, 80, 80), white, (150, 50, 50))
        
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    active = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check slot buttons
                for i, rect in enumerate(slot_rects, start=1):
                    if rect.collidepoint(mouse_pos):
                        if is_saving or os.path.exists(save_slots[i]):
                            if is_saving:
                                save_game(i)
                            else:
                                load_game(i)
                            active = False
                        break
                
                # Check back button
                if back_rect.collidepoint(mouse_pos):
                    active = False

def unlock_ending():
    end_active = True
    while end_active:
        window_screen.blit(ending_img, (0, 0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                end_active = False
                pygame.quit()
                sys.exit()

def welcome_screen():
    try:
        pygame.mixer.music.load("assets/music2.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        pass
    
    while True:
        window_screen.blit(welcome_img, (0, 0))
        welcome_text = font.render("Press Any Key To Begin...", True, black)
        window_screen.blit(welcome_text, (SCREEN_WIDTH//2 - welcome_text.get_width()//2, SCREEN_HEIGHT//2 - welcome_text.get_height()//2))
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.fadeout(1000)
                name_character_screen()
                dialogue_scene()
                main()
        
        pygame.display.update()

def main():
    global show_achievements, player_money, inventory, planted_seeds, equipped_item, dragging_seed
    global current_quests, completed_quests, player_rect, in_dialogue
    global achievement_scroll_offset, achievement_selected_category
    global carrotfest_active, carrotfest_end_time
    
    # Initialize game state
    clock = pygame.time.Clock()
    last_wheel_event_time = time.time()
    last_harvest_time = 0
    harvest_cooldown = 0.5
    
    # Start first quest if none active
    if not current_quests and not completed_quests:
        start_quest(1)
    
    # Main game loop
    running = True
    while running:
        current_time = time.time()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if show_achievements:
                        show_achievements = False
                    else:
                        running = False
                elif event.key == K_p and not in_dialogue:
                    show_achievements = not show_achievements
                    achievement_scroll_offset = 0
                elif event.key == K_k:  # Press F5 to save
                    save_load_menu(is_saving=True)
                elif event.key == K_l:  # Press F9 to load
                    save_load_menu(is_saving=False)
                elif not in_dialogue:
                    if event.key == K_m:
                        open_market()
                    elif event.key == K_e:
                        open_inventory()
                    elif event.key == K_SPACE:
                        check_and_collect_grown_fruit()
                        check_quest_progress()
                    elif event.key == K_f:
                        sell_crops()
                    elif event.key == K_t:
                        for npc in npc_list:
                            if (abs(player_rect.x - npc.rect.x) < 150 and 
                                abs(player_rect.y - npc.rect.y) < 150):
                                in_dialogue = True
                                interact_with_npc(npc)
                                break
            
            elif event.type == MOUSEBUTTONDOWN and not in_dialogue and not show_achievements:
                if (event.button == 1 and equipped_item and 
                    equipped_item in inventory.get("seeds", {}) and 
                    inventory["seeds"][equipped_item] > 0):
                    dragging_seed = True
            
            elif event.type == MOUSEBUTTONUP and not in_dialogue and not show_achievements:
                if event.button == 1 and dragging_seed and equipped_item:
                    planted_seeds.append((equipped_item, pygame.mouse.get_pos(), current_time))
                    inventory["seeds"][equipped_item] -= 1
                    if inventory["seeds"][equipped_item] <= 0:
                        del inventory["seeds"][equipped_item]
                        equipped_item = None
                    dragging_seed = False
            
            elif event.type == MOUSEWHEEL and show_achievements:
                achievement_scroll_offset -= event.y * 20
                max_scroll = max(0, len(achievements[achievement_selected_category]) * 70 - (SCREEN_HEIGHT - 340))
                achievement_scroll_offset = max(0, min(achievement_scroll_offset, max_scroll))
        
        # Game logic
        if not in_dialogue:
            move_character(player_speed)
            
            # Wheel event
            if current_time - last_wheel_event_time >= 120:
                last_wheel_event_time = current_time
                random_fruit = random.choice([item["name"] for item in market_items])
                random_pos = (random.randint(100, SCREEN_WIDTH - 100), 
                             random.randint(100, SCREEN_HEIGHT - 100))
                planted_seeds.append((random_fruit, random_pos, current_time))
                show_notification(f"Lucky Wheel: Free {random_fruit} planted!")
            
            # CarrotFest check
            if carrotfest_active and current_time > carrotfest_end_time:
                carrotfest_active = False
                for item in market_items:
                    if item["name"] == "Carrot":
                        item["sell"] = carrotfest_original_price
                        show_notification("CarrotFest has ended!")
                        break
            
            # Harvest cooldown
            if current_time - last_harvest_time >= harvest_cooldown:
                last_harvest_time = current_time
        
        # Check achievements
        check_achievements()
        
        # Drawing
        draw_game_world()
        
        # Draw achievement menu if open
        if show_achievements:
            draw_achievement_menu()
        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    welcome_screen()