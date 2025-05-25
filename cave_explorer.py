import pygame
import sys
import random
import time
import os
import math

# Initialize pygame
pygame.init()
pygame.font.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PIXEL_SIZE = 4  # Size of each "pixel" in our pixel art

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
CAVE_WALL = (70, 45, 30)
CAVE_FLOOR = (120, 100, 80)
CAVE_DARK = (40, 25, 15)
CAVE_HIGHLIGHT = (150, 120, 100)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cave Explorer")
clock = pygame.time.Clock()

# Load or create images
def load_images():
    images = {}
    
    # Create the images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # Create or load treasure chest image
    treasure_path = 'images/treasure_chest_shining.png'
    if not os.path.exists(treasure_path):
        treasure_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Background color - cave interior
        treasure_img.fill(CAVE_DARK)
        
        # Draw cave floor
        pygame.draw.rect(treasure_img, CAVE_FLOOR, (0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2))
        
        # Draw treasure chest
        chest_width = 300
        chest_height = 200
        chest_x = (SCREEN_WIDTH - chest_width) // 2
        chest_y = (SCREEN_HEIGHT - chest_height) // 2
        
        # Chest base
        pygame.draw.rect(treasure_img, BROWN, (chest_x, chest_y + chest_height//3, 
                                             chest_width, chest_height - chest_height//3))
        pygame.draw.rect(treasure_img, DARK_BROWN, (chest_x, chest_y + chest_height//3, 
                                                  chest_width, chest_height - chest_height//3), 3)
        
        # Chest top (open)
        pygame.draw.rect(treasure_img, BROWN, (chest_x, chest_y - chest_height//3, chest_width, chest_height//3))
        pygame.draw.rect(treasure_img, DARK_BROWN, (chest_x, chest_y - chest_height//3, chest_width, chest_height//3), 3)
        
        # Chest hinge
        pygame.draw.rect(treasure_img, DARK_BROWN, (chest_x, chest_y, chest_width, 10))
        
        # Gold, silver and gems inside and spilling out
        treasure_colors = [
            GOLD,                  # Gold
            (192, 192, 192),       # Silver
            (255, 0, 0),           # Ruby
            (0, 0, 255),           # Sapphire
            (0, 255, 0),           # Emerald
            (255, 0, 255),         # Amethyst
            (0, 255, 255)          # Diamond
        ]
        
        # Draw piles of treasure
        for _ in range(200):
            x = random.randint(chest_x + 20, chest_x + chest_width - 20)
            y = random.randint(chest_y, chest_y + chest_height - 20)
            size = random.randint(5, 15)
            color = random.choice(treasure_colors)
            pygame.draw.circle(treasure_img, color, (x, y), size)
        
        # Add light rays emanating from the treasure
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            length = random.randint(100, 300)
            end_x = chest_x + chest_width//2 + math.cos(rad) * length
            end_y = chest_y + chest_height//2 + math.sin(rad) * length
            
            # Draw light ray
            pygame.draw.line(treasure_img, (255, 255, 100, 100), 
                           (chest_x + chest_width//2, chest_y + chest_height//2),
                           (end_x, end_y), 2)
        
        # Add shining effect (bright spots)
        for _ in range(50):
            x = random.randint(chest_x - 50, chest_x + chest_width + 50)
            y = random.randint(chest_y - 50, chest_y + chest_height + 50)
            size = random.randint(2, 8)
            pygame.draw.circle(treasure_img, WHITE, (x, y), size)
        
        # Add glow effect around the chest
        for radius in range(200, 0, -10):
            alpha = max(0, 100 - radius // 2)
            temp_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (255, 255, 100, alpha), 
                             (chest_x + chest_width//2, chest_y + chest_height//2), radius)
            treasure_img.blit(temp_surf, (0, 0))
        
        pygame.image.save(treasure_img, treasure_path)
    
    images['treasure'] = pygame.image.load(treasure_path)
    
    # Create or load trap image (approaching spikes)
    trap_path = 'images/trap_approaching_spikes.png'
    if not os.path.exists(trap_path):
        trap_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        trap_img.fill(CAVE_DARK)
        
        # Draw cave floor and walls
        pygame.draw.rect(trap_img, CAVE_FLOOR, (0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2))
        
        # Draw spikes coming from all directions (approaching the player)
        # Spikes from floor
        for x in range(0, SCREEN_WIDTH, 40):
            height = random.randint(50, 150)
            width = 20
            points = [
                (x, SCREEN_HEIGHT // 2),
                (x + width, SCREEN_HEIGHT // 2),
                (x + width // 2, SCREEN_HEIGHT // 2 - height)
            ]
            pygame.draw.polygon(trap_img, GRAY, points)
            
            # Add metallic highlights
            highlight_points = [
                (x + width // 4, SCREEN_HEIGHT // 2),
                (x + width // 4, SCREEN_HEIGHT // 2 - height * 0.8)
            ]
            pygame.draw.line(trap_img, WHITE, highlight_points[0], highlight_points[1], 2)
        
        # Spikes from ceiling
        for x in range(20, SCREEN_WIDTH, 40):
            height = random.randint(50, 150)
            width = 20
            points = [
                (x, 0),
                (x + width, 0),
                (x + width // 2, height)
            ]
            pygame.draw.polygon(trap_img, GRAY, points)
            
            # Add metallic highlights
            highlight_points = [
                (x + width * 3 // 4, 0),
                (x + width * 3 // 4, height * 0.8)
            ]
            pygame.draw.line(trap_img, WHITE, highlight_points[0], highlight_points[1], 2)
        
        # Spikes from left wall
        for y in range(SCREEN_HEIGHT // 4, SCREEN_HEIGHT * 3 // 4, 40):
            length = random.randint(50, 150)
            width = 20
            points = [
                (0, y),
                (0, y + width),
                (length, y + width // 2)
            ]
            pygame.draw.polygon(trap_img, GRAY, points)
            
            # Add metallic highlights
            highlight_points = [
                (0, y + width * 3 // 4),
                (length * 0.8, y + width // 2)
            ]
            pygame.draw.line(trap_img, WHITE, highlight_points[0], highlight_points[1], 2)
        
        # Spikes from right wall
        for y in range(SCREEN_HEIGHT // 4, SCREEN_HEIGHT * 3 // 4, 40):
            length = random.randint(50, 150)
            width = 20
            points = [
                (SCREEN_WIDTH, y),
                (SCREEN_WIDTH, y + width),
                (SCREEN_WIDTH - length, y + width // 2)
            ]
            pygame.draw.polygon(trap_img, GRAY, points)
            
            # Add metallic highlights
            highlight_points = [
                (SCREEN_WIDTH, y + width * 1 // 4),
                (SCREEN_WIDTH - length * 0.8, y + width // 2)
            ]
            pygame.draw.line(trap_img, WHITE, highlight_points[0], highlight_points[1], 2)
        
        # Add motion blur effect to suggest spikes are moving
        for _ in range(50):
            # Random position near center
            center_x = SCREEN_WIDTH // 2
            center_y = SCREEN_HEIGHT // 2
            
            x = center_x + random.randint(-SCREEN_WIDTH//4, SCREEN_WIDTH//4)
            y = center_y + random.randint(-SCREEN_HEIGHT//4, SCREEN_HEIGHT//4)
            
            # Calculate direction from edge to center
            dx = center_x - x
            dy = center_y - y
            length = math.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                dx /= length
                dy /= length
                
                # Draw motion blur line
                blur_length = random.randint(10, 30)
                pygame.draw.line(trap_img, (150, 150, 150), 
                               (x, y), 
                               (x - dx * blur_length, y - dy * blur_length), 
                               2)
        
        pygame.image.save(trap_img, trap_path)
    
    images['trap'] = pygame.image.load(trap_path)
    
    # Create or load dead end image (falling rocks)
    dead_end_path = 'images/dead_end_falling_rocks.png'
    if not os.path.exists(dead_end_path):
        dead_end_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dead_end_img.fill(CAVE_DARK)
        
        # Draw cave floor
        pygame.draw.rect(dead_end_img, CAVE_FLOOR, (0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2))
        
        # Draw rocks falling from ceiling
        for _ in range(20):
            # Random position and size
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT * 3 // 4)  # Mostly in upper part of screen
            size = random.randint(30, 100)
            
            # Draw rock
            pygame.draw.circle(dead_end_img, GRAY, (x, y), size)
            
            # Add some texture to rocks
            for i in range(5):
                inner_x = random.randint(x - size + 10, x + size - 10)
                inner_y = random.randint(y - size + 10, y + size - 10)
                inner_size = random.randint(5, 15)
                pygame.draw.circle(dead_end_img, DARK_BROWN, (inner_x, inner_y), inner_size)
            
            # Add motion blur effect (lines trailing behind rocks)
            blur_length = random.randint(20, 50)
            pygame.draw.line(dead_end_img, GRAY, 
                           (x, y), 
                           (x, y - blur_length), 
                           size // 2)
        
        # Add dust and small debris
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 5)
            pygame.draw.circle(dead_end_img, WHITE, (x, y), size)
            
            # Add motion blur to small debris too
            if size > 2:
                blur_length = random.randint(5, 15)
                pygame.draw.line(dead_end_img, WHITE, 
                               (x, y), 
                               (x, y - blur_length), 
                               1)
        
        # Add cracks in the ceiling
        for _ in range(5):
            start_x = random.randint(0, SCREEN_WIDTH)
            start_y = random.randint(0, SCREEN_HEIGHT // 4)
            
            # Create a jagged line for the crack
            points = [(start_x, start_y)]
            for i in range(5):
                points.append((
                    points[-1][0] + random.randint(-30, 30),
                    points[-1][1] + random.randint(10, 30)
                ))
            
            # Draw the crack
            pygame.draw.lines(dead_end_img, BLACK, False, points, 3)
            
            # Add some smaller cracks branching off
            for point in points[1:-1]:
                branch_length = random.randint(10, 30)
                branch_end = (
                    point[0] + random.randint(-branch_length, branch_length),
                    point[1] + random.randint(-branch_length, branch_length)
                )
                pygame.draw.line(dead_end_img, BLACK, point, branch_end, 2)
        
        pygame.image.save(dead_end_img, dead_end_path)
    
    images['dead_end'] = pygame.image.load(dead_end_path)
    
    # Create or load torch image
    torch_path = 'images/torch_pixel.png'
    if not os.path.exists(torch_path):
        torch_img = pygame.Surface((32, 48), pygame.SRCALPHA)
        torch_img.fill((0, 0, 0, 0))
        
        # Draw torch handle
        pygame.draw.rect(torch_img, BROWN, (14, 24, 4, 24))
        
        # Draw flame
        pygame.draw.polygon(torch_img, (255, 100, 0), 
                          [(10, 30), (16, 5), (22, 30)])
        pygame.draw.polygon(torch_img, (255, 200, 0), 
                          [(12, 30), (16, 10), (20, 30)])
        
        pygame.image.save(torch_img, torch_path)
    
    images['torch'] = pygame.image.load(torch_path)
    
    # Create arrow indicators for all three directions
    arrow_paths = {}
    arrow_directions = ['left', 'up', 'right']
    
    for direction in arrow_directions:
        arrow_path = f'images/arrow_{direction}.png'
        if not os.path.exists(arrow_path):
            arrow_img = pygame.Surface((60, 40), pygame.SRCALPHA)
            arrow_img.fill((0, 0, 0, 0))
            
            if direction == 'left':
                # Draw left arrow
                pygame.draw.polygon(arrow_img, (255, 255, 0), 
                                  [(0, 20), (30, 0), (30, 10), (60, 10), (60, 30), (30, 30), (30, 40)])
            elif direction == 'up':
                # Draw up arrow
                pygame.draw.polygon(arrow_img, (255, 255, 0), 
                                  [(30, 0), (60, 30), (45, 30), (45, 40), (15, 40), (15, 30), (0, 30)])
            elif direction == 'right':
                # Draw right arrow
                pygame.draw.polygon(arrow_img, (255, 255, 0), 
                                  [(60, 20), (30, 0), (30, 10), (0, 10), (0, 30), (30, 30), (30, 40)])
            
            pygame.image.save(arrow_img, arrow_path)
        
        arrow_paths[direction] = arrow_path
    
    images['arrow_left'] = pygame.image.load(arrow_paths['left'])
    images['arrow_up'] = pygame.image.load(arrow_paths['up'])
    images['arrow_right'] = pygame.image.load(arrow_paths['right'])
    
    return images

# Game class
class Game:
    def __init__(self):
        self.images = load_images()
        self.state = "playing"  # playing, success, trap, dead_end, victory
        self.correct_path = random.randint(0, 2)  # 0: left, 1: middle, 2: right
        self.selected_path = 1  # Default to middle
        self.success_count = 0
        self.transition_time = 0
        self.transition_duration = 1.0  # seconds
        self.message = ""
        
        # For torch animation
        self.torch_flicker = 0
        
        # For first-person perspective
        self.perspective_offset = 0
        self.perspective_target = 0
        
        # For transition effects
        self.transition_effect = None
        
        # For animation timing
        self.animation_start_time = 0
        
        # Load cave textures
        self.wall_texture = self.create_texture(CAVE_WALL, 100, 100)
        self.floor_texture = self.create_texture(CAVE_FLOOR, 100, 100)
    
    def create_texture(self, base_color, width, height):
        texture = pygame.Surface((width, height))
        texture.fill(base_color)
        
        # Add some random noise for texture
        for _ in range(width * height // 10):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            brightness = random.randint(-20, 20)
            color = (
                max(0, min(255, base_color[0] + brightness)),
                max(0, min(255, base_color[1] + brightness)),
                max(0, min(255, base_color[2] + brightness))
            )
            pygame.draw.circle(texture, color, (x, y), random.randint(1, 3))
        
        return texture
    
    def update(self):
        # Update torch flicker
        self.torch_flicker = (self.torch_flicker + 0.1) % (2 * math.pi)
        
        # Update perspective animation
        if self.perspective_offset < self.perspective_target:
            self.perspective_offset = min(self.perspective_target, self.perspective_offset + 0.1)
        elif self.perspective_offset > self.perspective_target:
            self.perspective_offset = max(self.perspective_target, self.perspective_offset - 0.1)
        
        # Handle transition effects
        if self.transition_effect:
            current_time = time.time()
            progress = (current_time - self.transition_effect["start_time"]) / self.transition_effect["duration"]
            
            if progress >= 1.0:
                self.transition_effect = None
            elif self.transition_effect["type"] == "forward_movement":
                # Create a forward movement effect
                # Adjust the perspective to create a zooming effect
                zoom_factor = progress * 0.5  # Zoom in by 50%
                self.perspective_offset = self.perspective_target * (1 - zoom_factor)
        
        # Handle transitions
        if self.state == "success":
            if time.time() - self.transition_time > self.transition_duration:
                self.success_count += 1
                if self.success_count >= 5:  # Changed from 2 to 5
                    self.state = "victory"
                else:
                    self.state = "playing"
                    self.correct_path = random.randint(0, 2)
                    # Reset perspective to center for next choice
                    self.perspective_offset = 0
                    self.perspective_target = 0
                    self.selected_path = 1  # Reset to middle path
    
    def handle_key(self, key):
        if self.state == "playing":
            if key == pygame.K_LEFT:
                self.selected_path = 0
                self.perspective_target = -0.3  # Move view to left
                self.check_path()
            elif key == pygame.K_UP:
                self.selected_path = 1
                self.perspective_target = 0  # Center view
                self.check_path()
            elif key == pygame.K_RIGHT:
                self.selected_path = 2
                self.perspective_target = 0.3  # Move view to right
                self.check_path()
        elif self.state in ["trap", "dead_end", "victory"]:
            if key == pygame.K_SPACE:  # Changed from R key to Space key
                self.reset_game()
    
    def reset_game(self):
        # Reset the game state
        self.state = "playing"
        self.correct_path = random.randint(0, 2)
        self.selected_path = 1  # Default to middle
        self.success_count = 0
        self.perspective_offset = 0
        self.perspective_target = 0
    
    def check_path(self):
        self.transition_time = time.time()
        self.animation_start_time = time.time()  # Set animation start time
        
        if self.selected_path == self.correct_path:
            self.state = "success"
            self.message = "Correct! Moving to the next passage..."
            
            # Create a transition effect to show movement to next passage
            self.transition_effect = {
                "start_time": time.time(),
                "duration": 1.0,
                "type": "forward_movement"
            }
        else:
            # Randomly choose between trap and dead end
            if random.random() < 0.5:
                self.state = "trap"
                self.message = "It's a trap! Game over."
            else:
                self.state = "dead_end"
                self.message = "Dead end... Game over."
    
    def draw_first_person_cave(self):
        # Fill with dark background
        screen.fill(CAVE_DARK)
        
        # Draw cave in Minecraft-like pixel art style
        # Draw floor in pixel art style
        for y in range(int(SCREEN_HEIGHT * 0.6), SCREEN_HEIGHT, PIXEL_SIZE):
            for x in range(0, SCREEN_WIDTH, PIXEL_SIZE):
                # Create a checkerboard pattern for floor
                if (x // (PIXEL_SIZE * 4) + y // (PIXEL_SIZE * 4)) % 2 == 0:
                    pygame.draw.rect(screen, CAVE_FLOOR, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(screen, (CAVE_FLOOR[0] - 20, CAVE_FLOOR[1] - 20, CAVE_FLOOR[2] - 20), 
                                   (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Draw left wall in pixel art style
        left_wall_points = [
            (0, 0),
            (SCREEN_WIDTH * 0.25 + self.perspective_offset * SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6),
            (0, SCREEN_HEIGHT)
        ]
        
        # Fill the left wall area with pixel blocks
        min_x = 0
        max_x = int(SCREEN_WIDTH * 0.25 + self.perspective_offset * SCREEN_WIDTH * 0.5)
        for y in range(0, SCREEN_HEIGHT, PIXEL_SIZE):
            # Calculate the right edge of the wall at this y-coordinate
            if y < SCREEN_HEIGHT * 0.6:
                # Top part of wall (sloped)
                right_edge = int(y * max_x / (SCREEN_HEIGHT * 0.6))
            else:
                # Bottom part of wall (vertical)
                right_edge = max_x
            
            for x in range(0, right_edge, PIXEL_SIZE):
                # Create a pattern for wall
                if ((x // (PIXEL_SIZE * 3) + y // (PIXEL_SIZE * 3)) % 2 == 0):
                    pygame.draw.rect(screen, CAVE_WALL, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(screen, (CAVE_WALL[0] - 15, CAVE_WALL[1] - 15, CAVE_WALL[2] - 15), 
                                   (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Draw right wall in pixel art style
        right_wall_points = [
            (SCREEN_WIDTH, 0),
            (SCREEN_WIDTH * 0.75 + self.perspective_offset * SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        ]
        
        # Fill the right wall area with pixel blocks
        min_x = int(SCREEN_WIDTH * 0.75 + self.perspective_offset * SCREEN_WIDTH * 0.5)
        max_x = SCREEN_WIDTH
        for y in range(0, SCREEN_HEIGHT, PIXEL_SIZE):
            # Calculate the left edge of the wall at this y-coordinate
            if y < SCREEN_HEIGHT * 0.6:
                # Top part of wall (sloped)
                left_edge = int(SCREEN_WIDTH - (y * (SCREEN_WIDTH - min_x) / (SCREEN_HEIGHT * 0.6)))
            else:
                # Bottom part of wall (vertical)
                left_edge = min_x
            
            for x in range(left_edge, SCREEN_WIDTH, PIXEL_SIZE):
                # Create a pattern for wall
                if ((x // (PIXEL_SIZE * 3) + y // (PIXEL_SIZE * 3)) % 2 == 0):
                    pygame.draw.rect(screen, CAVE_WALL, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(screen, (CAVE_WALL[0] - 15, CAVE_WALL[1] - 15, CAVE_WALL[2] - 15), 
                                   (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Draw ceiling in pixel art style
        for y in range(0, int(SCREEN_HEIGHT * 0.3), PIXEL_SIZE):
            for x in range(0, SCREEN_WIDTH, PIXEL_SIZE):
                # Calculate the edges of the ceiling at this y-coordinate
                progress = y / (SCREEN_HEIGHT * 0.3)
                left_edge = int(SCREEN_WIDTH * 0.25 * progress + self.perspective_offset * SCREEN_WIDTH * 0.5 * progress)
                right_edge = int(SCREEN_WIDTH - SCREEN_WIDTH * 0.25 * progress + self.perspective_offset * SCREEN_WIDTH * 0.5 * progress)
                
                if left_edge <= x < right_edge:
                    # Create a pattern for ceiling
                    if ((x // (PIXEL_SIZE * 3) + y // (PIXEL_SIZE * 3)) % 2 == 0):
                        pygame.draw.rect(screen, CAVE_WALL, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                    else:
                        pygame.draw.rect(screen, (CAVE_WALL[0] - 15, CAVE_WALL[1] - 15, CAVE_WALL[2] - 15), 
                                       (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Draw the three realistic cave passages - static, no flickering
        path_centers = [0.25, 0.5, 0.75]  # Left, middle, right positions
        
        for i, center in enumerate(path_centers):
            # Adjust center based on perspective
            adjusted_center = center + self.perspective_offset * 0.5
            
            # Calculate path dimensions
            path_width = 0.15
            path_height = 0.4
            
            # Calculate tunnel coordinates
            tunnel_left = int(SCREEN_WIDTH * (adjusted_center - path_width/2))
            tunnel_right = int(SCREEN_WIDTH * (adjusted_center + path_width/2))
            tunnel_top = int(SCREEN_HEIGHT * 0.3)
            tunnel_bottom = int(SCREEN_HEIGHT * 0.6)
            
            # Draw tunnel in pixel art style (black interior)
            for y in range(tunnel_top, tunnel_bottom, PIXEL_SIZE):
                # Calculate tunnel width at this y-coordinate (narrower at bottom)
                progress = (y - tunnel_top) / (tunnel_bottom - tunnel_top)
                left_edge = int(tunnel_left + (SCREEN_WIDTH * (adjusted_center - path_width/3) - tunnel_left) * progress)
                right_edge = int(tunnel_right + (SCREEN_WIDTH * (adjusted_center + path_width/3) - tunnel_right) * progress)
                
                for x in range(left_edge, right_edge, PIXEL_SIZE):
                    pygame.draw.rect(screen, BLACK, (x, y, PIXEL_SIZE, PIXEL_SIZE))
            
            # Draw tunnel outline in pixel art style
            for y in range(tunnel_top, tunnel_bottom, PIXEL_SIZE):
                # Calculate tunnel width at this y-coordinate
                progress = (y - tunnel_top) / (tunnel_bottom - tunnel_top)
                left_edge = int(tunnel_left + (SCREEN_WIDTH * (adjusted_center - path_width/3) - tunnel_left) * progress)
                right_edge = int(tunnel_right + (SCREEN_WIDTH * (adjusted_center + path_width/3) - tunnel_right) * progress)
                
                # Draw left and right edges
                pygame.draw.rect(screen, CAVE_HIGHLIGHT, (left_edge - PIXEL_SIZE, y, PIXEL_SIZE, PIXEL_SIZE))
                pygame.draw.rect(screen, CAVE_HIGHLIGHT, (right_edge, y, PIXEL_SIZE, PIXEL_SIZE))
            
            # Draw top edge
            for x in range(tunnel_left, tunnel_right, PIXEL_SIZE):
                pygame.draw.rect(screen, CAVE_HIGHLIGHT, (x, tunnel_top - PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            
            # Draw arrow indicators for all three paths (static position, no floating)
            # Position the arrows above each tunnel
            arrow_x = SCREEN_WIDTH * adjusted_center - 30  # Center the 60px wide arrow
            arrow_y = SCREEN_HEIGHT * 0.2
            
            # Draw the appropriate arrow - all with the same color (no dimming for unselected)
            if i == 0:  # Left path
                screen.blit(self.images['arrow_left'], (arrow_x, arrow_y))
            elif i == 1:  # Middle path
                screen.blit(self.images['arrow_up'], (arrow_x, arrow_y))
            elif i == 2:  # Right path
                screen.blit(self.images['arrow_right'], (arrow_x, arrow_y))
            
            # Highlight the selected path with a subtle glow
            if i == self.selected_path:
                glow_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                glow_radius = 50
                for radius in range(glow_radius, 0, -5):
                    alpha = max(0, 50 - radius)
                    pygame.draw.circle(glow_surf, (255, 255, 100, alpha),
                                     (int(SCREEN_WIDTH * adjusted_center), int(SCREEN_HEIGHT * 0.2) + 20),
                                     radius)
                screen.blit(glow_surf, (0, 0))
        
        # Add some static stalactites (no movement) in pixel art style
        for i in range(5):
            x = 100 + i * 150  # Evenly spaced instead of random
            height = 30 + i % 3 * 10  # Varied but not random heights
            width = 10 + i % 2 * 5    # Varied but not random widths
            
            # Draw stalactite in pixel art style
            for py in range(0, height, PIXEL_SIZE):
                # Calculate width at this height
                w = int(width * py / height)
                for px in range(x - w, x + w, PIXEL_SIZE):
                    pygame.draw.rect(screen, CAVE_WALL, (px, py, PIXEL_SIZE, PIXEL_SIZE))
        
        # Add some static stalagmites (no movement) in pixel art style
        for i in range(3):
            x = 200 + i * 200  # Evenly spaced instead of random
            base_y = SCREEN_HEIGHT
            height = 25 + i * 5  # Varied but not random heights
            width = 10 + i * 3   # Varied but not random widths
            
            # Draw stalagmite in pixel art style
            for py in range(base_y - height, base_y, PIXEL_SIZE):
                # Calculate width at this height
                w = int(width * (base_y - py) / height)
                for px in range(x - w, x + w, PIXEL_SIZE):
                    pygame.draw.rect(screen, CAVE_WALL, (px, py, PIXEL_SIZE, PIXEL_SIZE))
    
    def draw(self, screen):
        # Draw first-person cave view
        self.draw_first_person_cave()
        
        # Draw torches
        torch_positions = [(100, 150), (SCREEN_WIDTH - 100, 150)]
        
        for pos in torch_positions:
            screen.blit(self.images['torch'], pos)
            # Add flickering light effect
            flicker_size = 50 + int(10 * abs(math.sin(self.torch_flicker)))
            light_surf = pygame.Surface((flicker_size*2, flicker_size*2), pygame.SRCALPHA)
            for radius in range(flicker_size, 0, -10):
                alpha = max(0, 100 - radius)
                pygame.draw.circle(light_surf, (255, 200, 100, alpha), 
                                 (flicker_size, flicker_size), radius)
            screen.blit(light_surf, (pos[0] - flicker_size + 15, pos[1] - flicker_size + 15))
        
        if self.state == "playing":
            # Draw progress
            font = pygame.font.SysFont(None, 36)
            progress_text = font.render(f"Progress: {self.success_count}/5", True, WHITE)
            screen.blit(progress_text, (SCREEN_WIDTH//2 - progress_text.get_width()//2, 50))
            
            # Draw instruction
            instruction_font = pygame.font.SysFont(None, 24)
            instruction_text = instruction_font.render("Use arrow keys to choose a path", True, WHITE)
            screen.blit(instruction_text, (SCREEN_WIDTH//2 - instruction_text.get_width()//2, 90))
        
        elif self.state == "success":
            # Draw tunnel movement animation
            self.draw_tunnel_movement()
            
            # Draw success message
            self.draw_message("Correct! Moving to the next passage...", GREEN)
        
        elif self.state == "trap":
            # Draw animated trap (spikes moving inward)
            self.draw_animated_trap()
            
            # Draw message
            self.draw_message("It's a trap! Game over.", RED)
            
            # Draw restart instruction as text (positioned to avoid overlap)
            self.draw_restart_message()
        
        elif self.state == "dead_end":
            # Draw animated falling rocks
            self.draw_animated_falling_rocks()
            
            # Draw message
            self.draw_message("Dead end... Game over.", RED)
            
            # Draw restart instruction as text (positioned to avoid overlap)
            self.draw_restart_message()
        
        elif self.state == "victory":
            # Draw treasure with pixel art sparkle animation
            self.draw_pixel_art_treasure()
            
            # Draw victory message
            font = pygame.font.SysFont(None, 48)
            victory_text = font.render("You found the treasure!", True, GOLD)
            screen.blit(victory_text, (SCREEN_WIDTH//2 - victory_text.get_width()//2, 150))
            
            # Draw restart instruction as text (positioned to avoid overlap)
            self.draw_restart_message()
    
    def draw_pixel_art_treasure(self):
        # Fill background with dark cave color
        screen.fill(CAVE_DARK)
        
        # Draw cave floor in pixel art style
        for y in range(SCREEN_HEIGHT//2, SCREEN_HEIGHT, PIXEL_SIZE):
            for x in range(0, SCREEN_WIDTH, PIXEL_SIZE):
                # Create a checkerboard pattern for floor
                if (x // (PIXEL_SIZE * 4) + y // (PIXEL_SIZE * 4)) % 2 == 0:
                    pygame.draw.rect(screen, CAVE_FLOOR, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(screen, (CAVE_FLOOR[0] - 20, CAVE_FLOOR[1] - 20, CAVE_FLOOR[2] - 20), 
                                   (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Calculate animation time
        animation_time = time.time() - self.animation_start_time
        
        # Draw treasure chest (pixel art style)
        chest_width = 200
        chest_height = 120
        chest_x = (SCREEN_WIDTH - chest_width) // 2
        chest_y = (SCREEN_HEIGHT - chest_height) // 2
        
        # Draw chest base (pixel by pixel)
        for y in range(chest_y + chest_height//3, chest_y + chest_height, PIXEL_SIZE):
            for x in range(chest_x, chest_x + chest_width, PIXEL_SIZE):
                if (x == chest_x or x >= chest_x + chest_width - PIXEL_SIZE or 
                    y >= chest_y + chest_height - PIXEL_SIZE):
                    # Draw border pixels darker
                    pygame.draw.rect(screen, DARK_BROWN, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    # Draw inner pixels
                    pygame.draw.rect(screen, BROWN, (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Draw chest top (pixel by pixel) - fully open position
        lid_angle = -60  # Degrees (negative means open upward)
        lid_height = chest_height//3
        
        # Calculate the position of the lid based on the angle
        lid_offset_y = int(math.sin(math.radians(lid_angle)) * lid_height * 2)
        
        # Draw the lid in open position
        for y in range(chest_y + lid_offset_y - lid_height, chest_y + lid_offset_y, PIXEL_SIZE):
            # Calculate how far we are through the lid height
            progress = (y - (chest_y + lid_offset_y - lid_height)) / lid_height
            
            # Calculate the x-offset based on the angle
            x_offset = int(math.cos(math.radians(lid_angle)) * progress * lid_height)
            
            for x in range(chest_x + x_offset, chest_x + chest_width + x_offset, PIXEL_SIZE):
                if (x == chest_x + x_offset or x >= chest_x + chest_width + x_offset - PIXEL_SIZE or 
                    y <= chest_y + lid_offset_y - lid_height + PIXEL_SIZE):
                    # Draw border pixels darker
                    pygame.draw.rect(screen, DARK_BROWN, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    # Draw inner pixels
                    pygame.draw.rect(screen, BROWN, (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Draw chest hinge (pixel by pixel)
        for y in range(chest_y, chest_y + 10, PIXEL_SIZE):
            for x in range(chest_x, chest_x + chest_width, PIXEL_SIZE):
                pygame.draw.rect(screen, DARK_BROWN, (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Draw treasure inside chest (pixel art style)
        treasure_colors = [
            GOLD,                  # Gold
            (192, 192, 192),       # Silver
            (255, 0, 0),           # Ruby
            (0, 0, 255),           # Sapphire
            (0, 255, 0),           # Emerald
            (255, 0, 255),         # Amethyst
            (0, 255, 255)          # Diamond
        ]
        
        # Draw piles of treasure (pixel by pixel) - more visible now that chest is fully open
        for i in range(80):  # Increased number of treasure items
            # Calculate position with slight animation
            offset_x = math.sin(animation_time * 2 + i) * 3
            offset_y = math.cos(animation_time * 3 + i) * 2
            
            # Spread treasure more widely around the open chest
            spread_factor = 1.5
            x = chest_x + 20 + (i * 3) % (chest_width - 40) + int(offset_x)
            y = chest_y + chest_height//3 + (i * 5) % (chest_height - chest_height//3 - 20) + int(offset_y)
            
            # Some treasure spilling out
            if i % 5 == 0:
                x += random.randint(-30, 30)
                y += random.randint(-10, 20)
            
            # Randomize size and color for variety
            size = (i % 3 + 1) * PIXEL_SIZE
            color = treasure_colors[i % len(treasure_colors)]
            
            # Draw treasure item (pixel by pixel)
            for px in range(x, x + size, PIXEL_SIZE):
                for py in range(y, y + size, PIXEL_SIZE):
                    if 0 <= px < SCREEN_WIDTH and 0 <= py < SCREEN_HEIGHT:
                        pygame.draw.rect(screen, color, (px, py, PIXEL_SIZE, PIXEL_SIZE))
        
        # Draw sparkles all over the screen (pixel art style)
        for i in range(100):
            # Calculate sparkle position and timing
            sparkle_x = (i * 37 + int(animation_time * 50)) % SCREEN_WIDTH
            sparkle_y = (i * 23 + int(animation_time * 30)) % SCREEN_HEIGHT
            
            # Make sparkles appear and disappear
            sparkle_time = (animation_time + i * 0.1) % 2
            if sparkle_time < 1.0:  # Only show some sparkles at a time
                # Determine sparkle size based on its life cycle
                if sparkle_time < 0.3:
                    size = PIXEL_SIZE
                elif sparkle_time < 0.6:
                    size = PIXEL_SIZE * 2
                elif sparkle_time < 0.8:
                    size = PIXEL_SIZE * 3
                else:
                    size = PIXEL_SIZE
                
                # Draw sparkle (pixel art style)
                # Center pixel
                pygame.draw.rect(screen, WHITE, 
                               (sparkle_x, sparkle_y, PIXEL_SIZE, PIXEL_SIZE))
                
                # Cross pattern for larger sparkles
                if size >= PIXEL_SIZE * 2:
                    pygame.draw.rect(screen, WHITE, 
                                   (sparkle_x + PIXEL_SIZE, sparkle_y, PIXEL_SIZE, PIXEL_SIZE))
                    pygame.draw.rect(screen, WHITE, 
                                   (sparkle_x - PIXEL_SIZE, sparkle_y, PIXEL_SIZE, PIXEL_SIZE))
                    pygame.draw.rect(screen, WHITE, 
                                   (sparkle_x, sparkle_y + PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                    pygame.draw.rect(screen, WHITE, 
                                   (sparkle_x, sparkle_y - PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                
                # Diagonal pixels for the largest sparkles
                if size >= PIXEL_SIZE * 3:
                    pygame.draw.rect(screen, WHITE, 
                                   (sparkle_x + PIXEL_SIZE, sparkle_y + PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                    pygame.draw.rect(screen, WHITE, 
                                   (sparkle_x - PIXEL_SIZE, sparkle_y - PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                    pygame.draw.rect(screen, WHITE, 
                                   (sparkle_x + PIXEL_SIZE, sparkle_y - PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                    pygame.draw.rect(screen, WHITE, 
                                   (sparkle_x - PIXEL_SIZE, sparkle_y + PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
    
    def draw_animated_trap(self):
        # Fill background
        screen.fill(CAVE_DARK)
        
        # Draw cave floor in pixel art style
        for y in range(SCREEN_HEIGHT//2, SCREEN_HEIGHT, PIXEL_SIZE):
            for x in range(0, SCREEN_WIDTH, PIXEL_SIZE):
                # Create a checkerboard pattern for floor
                if (x // (PIXEL_SIZE * 4) + y // (PIXEL_SIZE * 4)) % 2 == 0:
                    pygame.draw.rect(screen, CAVE_FLOOR, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(screen, (CAVE_FLOOR[0] - 20, CAVE_FLOOR[1] - 20, CAVE_FLOOR[2] - 20), 
                                   (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Calculate animation progress (0.0 to 1.0)
        progress = min(1.0, (time.time() - self.animation_start_time) / (self.transition_duration * 0.8))
        
        # Draw spikes coming from all directions in pixel art style
        # The spikes move inward as progress increases
        
        # Spikes from floor
        for x in range(0, SCREEN_WIDTH, PIXEL_SIZE * 8):
            height = int(150 * progress)  # Height increases with progress
            
            # Draw spike in pixel art style
            for y in range(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2 - height, -PIXEL_SIZE):
                # Calculate width at this height
                width = int(PIXEL_SIZE * 4 * (SCREEN_HEIGHT // 2 - y) / height)
                for px in range(x - width, x + width, PIXEL_SIZE):
                    if 0 <= px < SCREEN_WIDTH:
                        pygame.draw.rect(screen, GRAY, (px, y, PIXEL_SIZE, PIXEL_SIZE))
            
            # Add metallic highlights
            highlight_x = x + PIXEL_SIZE
            for y in range(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2 - height * 4 // 5, -PIXEL_SIZE * 2):
                pygame.draw.rect(screen, WHITE, (highlight_x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Spikes from ceiling
        for x in range(PIXEL_SIZE * 4, SCREEN_WIDTH, PIXEL_SIZE * 8):
            height = int(150 * progress)  # Height increases with progress
            
            # Draw spike in pixel art style
            for y in range(0, height, PIXEL_SIZE):
                # Calculate width at this height
                width = int(PIXEL_SIZE * 4 * y / height)
                for px in range(x - width, x + width, PIXEL_SIZE):
                    if 0 <= px < SCREEN_WIDTH:
                        pygame.draw.rect(screen, GRAY, (px, y, PIXEL_SIZE, PIXEL_SIZE))
            
            # Add metallic highlights
            highlight_x = x - PIXEL_SIZE
            for y in range(0, height * 4 // 5, PIXEL_SIZE * 2):
                pygame.draw.rect(screen, WHITE, (highlight_x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Spikes from left wall
        for y in range(SCREEN_HEIGHT // 4, SCREEN_HEIGHT * 3 // 4, PIXEL_SIZE * 8):
            length = int(150 * progress)  # Length increases with progress
            
            # Draw spike in pixel art style
            for x in range(0, length, PIXEL_SIZE):
                # Calculate height at this position
                height = int(PIXEL_SIZE * 4 * x / length)
                for py in range(y - height, y + height, PIXEL_SIZE):
                    if 0 <= py < SCREEN_HEIGHT:
                        pygame.draw.rect(screen, GRAY, (x, py, PIXEL_SIZE, PIXEL_SIZE))
            
            # Add metallic highlights
            highlight_y = y + PIXEL_SIZE
            for x in range(0, length * 4 // 5, PIXEL_SIZE * 2):
                pygame.draw.rect(screen, WHITE, (x, highlight_y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Spikes from right wall
        for y in range(SCREEN_HEIGHT // 4, SCREEN_HEIGHT * 3 // 4, PIXEL_SIZE * 8):
            length = int(150 * progress)  # Length increases with progress
            
            # Draw spike in pixel art style
            for x in range(SCREEN_WIDTH, SCREEN_WIDTH - length, -PIXEL_SIZE):
                # Calculate height at this position
                height = int(PIXEL_SIZE * 4 * (SCREEN_WIDTH - x) / length)
                for py in range(y - height, y + height, PIXEL_SIZE):
                    if 0 <= py < SCREEN_HEIGHT:
                        pygame.draw.rect(screen, GRAY, (x, py, PIXEL_SIZE, PIXEL_SIZE))
            
            # Add metallic highlights
            highlight_y = y - PIXEL_SIZE
            for x in range(SCREEN_WIDTH, SCREEN_WIDTH - length * 4 // 5, -PIXEL_SIZE * 2):
                pygame.draw.rect(screen, WHITE, (x, highlight_y, PIXEL_SIZE, PIXEL_SIZE))
    
    def draw_animated_falling_rocks(self):
        # Fill background
        screen.fill(CAVE_DARK)
        
        # Draw cave floor in pixel art style
        for y in range(SCREEN_HEIGHT//2, SCREEN_HEIGHT, PIXEL_SIZE):
            for x in range(0, SCREEN_WIDTH, PIXEL_SIZE):
                # Create a checkerboard pattern for floor
                if (x // (PIXEL_SIZE * 4) + y // (PIXEL_SIZE * 4)) % 2 == 0:
                    pygame.draw.rect(screen, CAVE_FLOOR, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(screen, (CAVE_FLOOR[0] - 20, CAVE_FLOOR[1] - 20, CAVE_FLOOR[2] - 20), 
                                   (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Calculate animation progress (0.0 to 1.0)
        progress = min(1.0, (time.time() - self.animation_start_time) / (self.transition_duration * 0.8))
        
        # Create a list of rocks with their positions
        rocks = [
            {"x": 100, "size": 80, "start_y": -100},
            {"x": 300, "size": 120, "start_y": -200},
            {"x": 500, "size": 90, "start_y": -150},
            {"x": 200, "size": 70, "start_y": -250},
            {"x": 600, "size": 100, "start_y": -180},
            {"x": 400, "size": 110, "start_y": -300},
            {"x": 700, "size": 60, "start_y": -220}
        ]
        
        # Draw rocks falling from top in pixel art style
        for rock in rocks:
            # Calculate current y position based on progress
            # Rocks fall at different speeds based on their size
            fall_speed = 600 + rock["size"] * 3  # Larger rocks fall faster
            current_y = rock["start_y"] + fall_speed * progress
            
            # Draw rock in pixel art style
            rock_x = rock["x"]
            rock_y = int(current_y)
            rock_size = rock["size"]
            
            # Draw rock as a collection of pixels
            for y in range(rock_y - rock_size, rock_y + rock_size, PIXEL_SIZE):
                for x in range(rock_x - rock_size, rock_x + rock_size, PIXEL_SIZE):
                    # Only draw pixels within the rock's circular boundary
                    if ((x - rock_x)**2 + (y - rock_y)**2 < rock_size**2 and
                        0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT):
                        
                        # Create a pattern for the rock
                        if ((x // (PIXEL_SIZE * 2) + y // (PIXEL_SIZE * 2)) % 2 == 0):
                            pygame.draw.rect(screen, GRAY, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                        else:
                            pygame.draw.rect(screen, (GRAY[0] - 30, GRAY[1] - 30, GRAY[2] - 30), 
                                           (x, y, PIXEL_SIZE, PIXEL_SIZE))
            
            # Add motion blur effect (lines trailing behind rocks) in pixel art style
            blur_length = 30
            for y in range(rock_y - blur_length, rock_y, PIXEL_SIZE * 2):
                # Calculate x position along the blur line
                x_offset = int((rock_y - y) * rock_size / blur_length / 2)
                
                # Draw a few pixels for the blur
                for x in range(rock_x - x_offset, rock_x + x_offset, PIXEL_SIZE * 2):
                    if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                        pygame.draw.rect(screen, (GRAY[0] - 20, GRAY[1] - 20, GRAY[2] - 20), 
                                       (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Add dust and small debris in pixel art style
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH // PIXEL_SIZE) * PIXEL_SIZE
            y = random.randint(0, int(SCREEN_HEIGHT * progress) // PIXEL_SIZE) * PIXEL_SIZE
            size = random.randint(1, 2) * PIXEL_SIZE
            pygame.draw.rect(screen, WHITE, (x, y, size, size))
        
        # Add cracks in the ceiling that grow with progress in pixel art style
        for i in range(5):
            start_x = 100 + i * 150
            start_y = 0
            
            # Create a jagged line for the crack
            crack_length = int(100 * progress)  # Cracks grow longer with progress
            
            # Draw main crack
            current_x = start_x
            current_y = start_y
            
            for j in range(crack_length // (PIXEL_SIZE * 2)):
                next_x = current_x + random.randint(-PIXEL_SIZE, PIXEL_SIZE)
                next_y = current_y + PIXEL_SIZE * 2
                
                # Draw a few pixels for the crack
                for y in range(current_y, next_y, PIXEL_SIZE):
                    # Interpolate x position
                    x = current_x + (next_x - current_x) * (y - current_y) // (next_y - current_y)
                    if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                        pygame.draw.rect(screen, BLACK, (x, y, PIXEL_SIZE, PIXEL_SIZE))
                
                current_x = next_x
                current_y = next_y
                
                # Add some branch cracks
                if j % 3 == 0 and j > 0:
                    branch_x = current_x
                    branch_y = current_y
                    branch_dir = random.choice([-1, 1])
                    
                    for k in range(random.randint(2, 5)):
                        branch_x += branch_dir * PIXEL_SIZE
                        branch_y += PIXEL_SIZE
                        if 0 <= branch_x < SCREEN_WIDTH and 0 <= branch_y < SCREEN_HEIGHT:
                            pygame.draw.rect(screen, BLACK, (branch_x, branch_y, PIXEL_SIZE, PIXEL_SIZE))
    
    def draw_tunnel_movement(self):
        # Calculate how far into the transition we are
        progress = min(1.0, (time.time() - self.transition_time) / (self.transition_duration * 0.8))
        
        # Draw cave background in pixel art style
        for y in range(0, SCREEN_HEIGHT, PIXEL_SIZE):
            for x in range(0, SCREEN_WIDTH, PIXEL_SIZE):
                # Create a pattern for background
                darkness = int(255 * (1 - progress))
                color = (darkness // 4, darkness // 6, 0)
                pygame.draw.rect(screen, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Draw a tunnel that gets progressively longer as we move through it
        tunnel_length = int(progress * 10)  # Number of tunnel segments
        
        # Draw the tunnel segments in pixel art style
        for i in range(tunnel_length):
            # Calculate tunnel segment size (gets smaller as we go deeper)
            segment_size = 1.0 - (i / tunnel_length) * progress
            
            # Calculate tunnel segment position
            x = SCREEN_WIDTH // 2
            y = SCREEN_HEIGHT // 2
            width = int(SCREEN_WIDTH * segment_size)
            height = int(SCREEN_HEIGHT * segment_size)
            
            # Draw tunnel segment in pixel art style
            for py in range(y - height//2, y + height//2, PIXEL_SIZE):
                for px in range(x - width//2, x + width//2, PIXEL_SIZE):
                    # Only draw the border pixels
                    if (abs(px - (x - width//2)) < PIXEL_SIZE * 2 or 
                        abs(px - (x + width//2 - PIXEL_SIZE)) < PIXEL_SIZE * 2 or
                        abs(py - (y - height//2)) < PIXEL_SIZE * 2 or
                        abs(py - (y + height//2 - PIXEL_SIZE)) < PIXEL_SIZE * 2):
                        pygame.draw.rect(screen, CAVE_HIGHLIGHT, (px, py, PIXEL_SIZE, PIXEL_SIZE))
                    else:
                        pygame.draw.rect(screen, BLACK, (px, py, PIXEL_SIZE, PIXEL_SIZE))
            
            # Add some texture to tunnel walls in pixel art style
            if i % 2 == 0:  # Add texture to every other segment for performance
                for _ in range(5):
                    wall_x = random.randint(x - width//2, x + width//2) // PIXEL_SIZE * PIXEL_SIZE
                    wall_y = random.randint(y - height//2, y + height//2) // PIXEL_SIZE * PIXEL_SIZE
                    # Only add texture near the edges
                    if (abs(wall_x - (x - width//2)) < PIXEL_SIZE * 4 or 
                        abs(wall_x - (x + width//2 - PIXEL_SIZE)) < PIXEL_SIZE * 4 or
                        abs(wall_y - (y - height//2)) < PIXEL_SIZE * 4 or
                        abs(wall_y - (y + height//2 - PIXEL_SIZE)) < PIXEL_SIZE * 4):
                        pygame.draw.rect(screen, CAVE_HIGHLIGHT, (wall_x, wall_y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Add some motion blur lines for speed effect in pixel art style
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(50, 200) * progress
            start_x = SCREEN_WIDTH // 2
            start_y = SCREEN_HEIGHT // 2
            
            # Draw dotted line for motion blur
            for i in range(0, int(length), PIXEL_SIZE * 3):
                pos_x = int(start_x + math.cos(angle) * i)
                pos_y = int(start_y + math.sin(angle) * i)
                
                if (0 <= pos_x < SCREEN_WIDTH and 0 <= pos_y < SCREEN_HEIGHT):
                    pygame.draw.rect(screen, (100, 100, 100), 
                                   (pos_x, pos_y, PIXEL_SIZE, PIXEL_SIZE))
        
        # Add a bright flash at the end of the tunnel to transition to next scene
        if progress > 0.7:
            flash_alpha = int(255 * ((progress - 0.7) / 0.3))
            
            # Draw flash in pixel art style
            for y in range(0, SCREEN_HEIGHT, PIXEL_SIZE * 2):
                for x in range(0, SCREEN_WIDTH, PIXEL_SIZE * 2):
                    # Create a checkerboard pattern for the flash
                    if (x // (PIXEL_SIZE * 4) + y // (PIXEL_SIZE * 4)) % 2 == 0:
                        brightness = min(255, flash_alpha + 50)
                    else:
                        brightness = flash_alpha
                    
                    pygame.draw.rect(screen, (brightness, brightness, brightness), 
                                   (x, y, PIXEL_SIZE * 2, PIXEL_SIZE * 2))
    
    def draw_restart_message(self):
        # Draw a simple text message instead of a button
        # Position it higher to avoid overlap with other messages
        font = pygame.font.SysFont(None, 30)
        text = font.render("Press SPACE to Restart", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT - 50))
    
    def draw_message(self, message, color):
        font = pygame.font.SysFont(None, 36)
        text = font.render(message, True, color)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT - 100))

# Main function
def main():
    game = Game()
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.handle_key(event.key)
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
