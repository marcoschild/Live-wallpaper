import pygame
import time
import os
import platform
import psutil  # For CPU & RAM usage
import random
import requests
from datetime import datetime

# ---- CONFIGURATION ----
SHOW_WEATHER = False  # Set to True if you want weather (requires API)
WEATHER_API_KEY = "your_api_key_here"  # Get an API key from https://openweathermap.org/
CITY_NAME = "Zurich"

# Initialize Pygame
pygame.init()

# Get screen size
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.Surface((screen_width, screen_height))

# Fonts & Colors
font = pygame.font.Font(pygame.font.get_default_font(), 100)
small_font = pygame.font.Font(pygame.font.get_default_font(), 50)
color = (255, 255, 255)  # White
bg_color = (0, 0, 50)  # Dark blue

# Clock position & speed
x, y = screen_width // 2, screen_height // 2
dx, dy = 5, 5  # Speed of bouncing effect

# Temp file for wallpaper
wallpaper_path = os.path.join(os.getcwd(), "live_wallpaper.png")

# Get weather data
def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        temp = response["main"]["temp"]
        condition = response["weather"][0]["description"].capitalize()
        return f"{CITY_NAME}: {temp}°C, {condition}"
    except:
        return "Weather unavailable"

# Function to set wallpaper based on OS
def set_wallpaper(path):
    system = platform.system()
    if system == "Windows":
        import ctypes
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    elif system == "Darwin":  # macOS
        os.system(f"osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"{path}\"'")
    elif system == "Linux":
        os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{path}")

# Function to draw a gradient background
def draw_gradient():
    for i in range(screen_height):
        color_shade = int(50 + (i / screen_height) * 200)  # Dark to light blue
        pygame.draw.line(screen, (0, 0, color_shade), (0, i), (screen_width, i))

# Update wallpaper continuously
def update_wallpaper():
    global x, y, dx, dy

    while True:
        # Clear the screen & draw gradient
        draw_gradient()

        # Get current time & system stats
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%A, %d %B %Y")
        cpu_usage = f"CPU: {psutil.cpu_percent()}%"
        ram_usage = f"RAM: {psutil.virtual_memory().percent}%"
        
        # Get weather if enabled
        weather_info = get_weather() if SHOW_WEATHER else ""

        # Render text
        time_text = font.render(current_time, True, color)
        date_text = small_font.render(current_date, True, color)
        cpu_text = small_font.render(cpu_usage, True, color)
        ram_text = small_font.render(ram_usage, True, color)
        weather_text = small_font.render(weather_info, True, color)

        # Bouncing effect for time
        x += dx
        y += dy
        if x <= 100 or x >= screen_width - 100:
            dx = -dx
        if y <= 100 or y >= screen_height - 100:
            dy = -dy

        # Draw text on screen
        screen.blit(time_text, (x, y))
        screen.blit(date_text, (50, 50))
        screen.blit(cpu_text, (50, screen_height - 150))
        screen.blit(ram_text, (50, screen_height - 100))
        if SHOW_WEATHER:
            screen.blit(weather_text, (50, screen_height - 50))

        # Save image
        pygame.image.save(screen, wallpaper_path)

        # Set as wallpaper
        set_wallpaper(wallpaper_path)

        # Wait before updating again
        time.sleep(1)

# Run wallpaper update loop
update_wallpaper()
