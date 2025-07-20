import pygame
import random
import json
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
FONT_SIZE = 36
LARGE_FONT_SIZE = 48

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Word lists
EASY_WORDS = ["cat", "dog", "run", "jump", "play", "game", "fast", "slow", "big", "small"]
MEDIUM_WORDS = ["python", "computer", "keyboard", "mouse", "screen", "program", "coding", "debug", "function", "variable"]
HARD_WORDS = ["algorithm", "complexity", "optimization", "synchronization", "asynchronous", "microcontroller", "cryptography", "neural", "artificial", "intelligence"]
HACKER_WORDS = ["cryptocurrency", "decentralization", "blockchain", "penetration", "vulnerability", "exploitation", "obfuscation", "steganography", "polymorphism", "sandboxing"]

class Word:
    def __init__(self, text, x, y, speed, color):
        self.text = text
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.rendered = self.font.render(text, True, color)
        self.width = self.rendered.get_width()
        self.height = self.rendered.get_height()
        
    def update(self):
        self.x -= self.speed
        
    def draw(self, screen):
        screen.blit(self.rendered, (self.x, self.y))
        
    def is_off_screen(self):
        return self.x + self.width < 0

class RageTypingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rage Typing Game - Type to Survive!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
        
        self.reset_game()
        
    def reset_game(self):
        self.words = []
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.level = 1
        self.lives = 3
        self.game_over = False
        self.current_typed = ""
        self.spawn_timer = 0
        
    def get_words_for_level(self):
        if self.level <= 3:
            return ["cat", "dog", "run", "jump", "play", "game", "fast", "slow", "big", "small"]
        elif self.level <= 6:
            return ["python", "computer", "keyboard", "mouse", "screen", "program", "coding", "debug", "function", "variable"]
        elif self.level <= 9:
            return ["algorithm", "complexity", "optimization", "synchronization", "asynchronous", "microcontroller", "cryptography", "neural", "artificial", "intelligence"]
        else:
            return ["cryptocurrency", "decentralization", "blockchain", "penetration", "vulnerability", "exploitation", "obfuscation", "steganography", "polymorphism", "sandboxing"]
            
    def get_speed_for_level(self):
        return 1 + (self.level * 0.5)
        
    def get_spawn_rate_for_level(self):
        return max(30, 120 - (self.level * 10))
        
    def spawn_word(self):
        words_list = self.get_words_for_level()
        word_text = random.choice(words_list)
        x = SCREEN_WIDTH + 50
        y = random.randint(50, SCREEN_HEIGHT - 100)
        speed = self.get_speed_for_level()
        
        if self.level <= 3:
            color = GREEN
        elif self.level <= 6:
            color = BLUE
        elif self.level <= 9:
            color = ORANGE
        else:
            color = RED
            
        self.words.append(Word(word_text, x, y, speed, color))
        
    def handle_typing(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.current_typed = self.current_typed[:-1]
            elif event.key == pygame.K_RETURN:
                self.check_word()
            elif event.key == pygame.K_ESCAPE:
                self.game_over = True
            elif event.unicode and event.unicode.isprintable():
                self.current_typed += event.unicode
                
    def check_word(self):
        typed = self.current_typed.lower().strip()
        if typed:
            for i, word in enumerate(self.words[:]):
                if word.text.lower() == typed:
                    self.words.pop(i)
                    points = len(typed) * self.level * (1 + self.combo * 0.1)
                    self.score += int(points)
                    self.combo += 1
                    self.max_combo = max(self.max_combo, self.combo)
                    self.current_typed = ""
                    return
                    
        self.combo = 0
        self.current_typed = ""
        
    def update(self):
        if self.game_over:
            return
            
        # Update words
        for word in self.words[:]:
            word.update()
            if word.is_off_screen():
                self.words.remove(word)
                self.lives -= 1
                self.combo = 0
                if self.lives <= 0:
                    self.game_over = True
                    
        # Spawn new words
        self.spawn_timer += 1
        if self.spawn_timer >= self.get_spawn_rate_for_level():
            self.spawn_word()
            self.spawn_timer = 0
            
        # Level progression
        if self.score >= self.level * 100:
            self.level += 1
            
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw words
        for word in self.words:
            word.draw(self.screen)
            
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, RED)
        combo_text = self.font.render(f"Combo: {self.combo}x", True, YELLOW)
        typed_text = self.font.render(f"Type: {self.current_typed}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(lives_text, (10, 90))
        self.screen.blit(combo_text, (10, 130))
        self.screen.blit(typed_text, (SCREEN_WIDTH//2 - typed_text.get_width()//2, SCREEN_HEIGHT - 50))
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.large_font.render("GAME OVER!", True, RED)
            final_score_text = self.large_font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
            self.screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
            
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                self.handle_typing(event)
            
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = RageTypingGame()
    game.run()