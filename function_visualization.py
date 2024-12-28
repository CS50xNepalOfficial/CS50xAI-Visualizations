import pygame
import tkinter as tk
from tkinter import ttk
import math

class FunctionUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Function Controls")
        
        # Function dropdown
        self.functions = {
            "Square": lambda x: x**2,
            "Double": lambda x: x*2,
            "Cube": lambda x: x**3,
            "Half": lambda x: x/2
        }
        self.function_var = tk.StringVar(value="Square")
        function_dropdown = ttk.Combobox(
            self.root, 
            textvariable=self.function_var,
            values=list(self.functions.keys())
        )
        function_dropdown.pack(pady=5)
        
        # Input value entry
        self.value_var = tk.StringVar(value="0")
        ttk.Label(self.root, text="Input Value:").pack()
        ttk.Entry(self.root, textvariable=self.value_var).pack(pady=5)
        
        # Process button
        ttk.Button(self.root, text="Process", command=self.process).pack(pady=5)
        pygame.mixer.init()
        try:
            self.process_sound = pygame.mixer.Sound('duck.mp3')
            self.bg_music = pygame.mixer.Sound('duck.mp3')
            self.bg_music.set_volume(0.3)  # Lower background volume
        except:
            print("Audio files not found. Create processing.wav and background.wav for sound effects.")
            self.process_sound = None
            self.bg_music = None
        # Pygame setup
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Function Factory")
        
        # Load duck image
        try:
            self.duck_img = pygame.image.load('duck.png')  # Add a duck.png to your directory
            self.duck_img = pygame.transform.scale(self.duck_img, (50, 50))
        except:
            print("Duck image not found. Creating placeholder.")
            self.duck_img = pygame.Surface((50, 50))
            self.duck_img.fill((255, 255, 0))  # Yellow placeholder
        
        self.duck_pos = [350, 250]
        self.processing = False
        self.animation_progress = 0
        self.input_value = 0
        self.output_value = 0
    
    def process(self):
        """Process the input value through selected function"""
        try:
            # Get input value and convert to float
            self.input_value = float(self.value_var.get())
            
            # Get selected function and compute result
            selected_function = self.functions[self.function_var.get()]
            self.output_value = selected_function(self.input_value)
            if self.process_sound:
                self.process_sound.play()
            if self.bg_music:
                self.bg_music.play(-1)  # -1 for loop
            
            # Start animation
            self.processing = True
            self.animation_progress = 0
            
            # Reset duck position
            self.duck_pos = [350, 250]
            
        except ValueError:
            # Handle invalid input
            print("Please enter a valid number")
        except Exception as e:
            print(f"Error processing: {e}")
    def draw_fancy_box(self, surface, rect, border_radius=15):
        x, y, width, height = rect
        
        # Draw gradient background
        for i in range(height):
            color = (50, 100 + i//2, 200 - i//3)
            pygame.draw.rect(surface, color, (x, y + i, width, 1))
            
        # Draw rounded corners
        pygame.draw.rect(surface, (30, 70, 150), rect, border_radius=border_radius)
        
        # Draw highlights
        pygame.draw.line(surface, (255, 255, 255, 128), (x, y), (x + width, y), 2)
        pygame.draw.line(surface, (255, 255, 255, 128), (x, y), (x, y + height), 2)
            
    def draw_conveyor(self, surface, rect):
        x, y, width, height = rect
        
        # Draw base
        pygame.draw.rect(surface, (40, 40, 40), rect)
        
        # Draw conveyor belt segments
        segment_width = 20
        offset = (self.animation_progress * 30) % segment_width
        for i in range(0, width, segment_width):
            pygame.draw.rect(surface, (80, 80, 80), 
                           (x + i - offset, y, segment_width-2, height))
            
    def draw(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        
        self.screen.fill(WHITE)
        
        # Draw fancy factory box
        self.draw_fancy_box(self.screen, (300, 200, 200, 200))
        
        # Draw conveyor belts
        self.draw_conveyor(self.screen, (100, 300, 200, 20))
        self.draw_conveyor(self.screen, (500, 300, 200, 20))
        
        # Animate duck during processing
        if self.processing:
            self.duck_pos[1] = 250 + math.sin(self.animation_progress * 2) * 20
            self.duck_pos[0] = 350 + math.cos(self.animation_progress) * 30
            if self.animation_progress >= 2*math.pi:
                if self.bg_music:
                    self.bg_music.stop()
            
        # Draw duck
        self.screen.blit(self.duck_img, self.duck_pos)
        
        # Draw gears
        if self.processing:
            gears = [(320, 250), (480, 250), (320, 350), (480, 350)]
            for x, y in gears:
                pygame.draw.circle(self.screen, (200, 50, 50), (x, y), 15)
                end_x = x + 15 * math.cos(self.animation_progress)
                end_y = y + 15 * math.sin(self.animation_progress)
                pygame.draw.line(self.screen, WHITE, (x, y), (end_x, end_y), 3)
        
        # Text display with better styling
        font = pygame.font.Font(None, 36)
        input_text = font.render(f"Input: {self.input_value}", True, BLACK)
        output_text = font.render(f"Output: {self.output_value}", True, BLACK)
        function_text = font.render(f"Function: {self.function_var.get()}", True, BLACK)
        
        # Add text shadows
        shadow_offset = 2
        for text, pos in [(input_text, (100, 250)), 
                         (output_text, (550, 250)), 
                         (function_text, (300, 150))]:
            self.screen.blit(text, (pos[0] + shadow_offset, pos[1] + shadow_offset))
            self.screen.blit(text, pos)
        
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if self.processing:
                self.animation_progress += 0.1
                if self.animation_progress >= 2*math.pi:
                    self.processing = False
                    self.animation_progress = 0
            
            self.draw()
            pygame.display.flip()
            self.root.update()
            clock.tick(60)
            
        pygame.quit()
        self.root.destroy()

if __name__ == "__main__":
    app = FunctionUI()
    app.run()