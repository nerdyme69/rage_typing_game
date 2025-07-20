import pygame
import random
import json
import math
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
FONT_SIZE = 36
LARGE_FONT_SIZE = 48

# Colors - Modern palette
BLACK = (15, 15, 23)
WHITE = (248, 248, 255)
DARK_PURPLE = (25, 25, 45)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (20, 233, 255)
NEON_PINK = (255, 20, 147)
NEON_ORANGE = (255, 165, 0)
NEON_YELLOW = (255, 255, 20)
RED = (255, 69, 58)
GREEN = (48, 209, 88)
BLUE = (0, 122, 255)
PURPLE = (175, 82, 222)
GOLD = (255, 214, 10)

# Gradient colors for background
BG_GRADIENT_TOP = (20, 20, 40)
BG_GRADIENT_BOTTOM = (40, 20, 60)

# Gen Z & Humorous Word Lists 🔥
EASY_WORDS = ["sus", "vibe", "slay", "flex", "mood", "stan", "tea", "salty", "bet", "cap", "fam", "lit", "fire", "ghost", "simp", "queen", "king", "woke", "cringe", "based"]
MEDIUM_WORDS = ["periodt", "lowkey", "highkey", "bestie", "slaps", "snack", "bussin", "sheesh", "chefs kiss", "no cap", "sending me", "rent free", "main character", "that girl", "gaslight", "gatekeep", "girlboss", "toxic", "wholesome"]
HARD_WORDS = ["doomscrolling", "chronically online", "touch grass", "parasocial", "gaslighting", "mansplaining", "womansplaining", "virtue signaling", "cancel culture", "snowflake generation", "ok boomer", "living rent free", "emotional damage", "social battery", "overthinking era"]
HACKER_WORDS = ["cyberbullying survivor", "digital detox needed", "algorithm manipulation", "dopamine deficiency", "social media addiction", "influencer wannabe", "content creator burnout", "tiktok brain rot", "reddit moment", "twitter discourse", "instagram vs reality", "youtube rabbit hole", "discord moderator", "twitch streamer grind"]

class Word:
    def __init__(self, text, x, y, speed, color):
        self.text = text
        self.original_x = x
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.original_color = color
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.rendered = self.font.render(text, True, color)
        self.width = self.rendered.get_width()
        self.height = self.rendered.get_height()
        self.glow_radius = 0
        self.pulse_time = 0
        self.shadow_offset = 3
        self.rotation = 0
        self.scale = 1.0
        self.target_scale = 1.0
        self.wobble = 0
        self.float_offset = 0
        self.physics_vx = 0
        self.physics_vy = 0
        self.gravity = 0.1
        self.bounce = 0.8
        
    def update(self):
        # Basic movement
        self.x -= self.speed
        self.pulse_time += 0.1
        
        # Advanced physics and animations
        self.rotation += 0.5
        self.wobble += 0.15
        
        # Floating animation
        self.float_offset = math.sin(self.pulse_time * 2) * 3
        self.glow_radius = 2 + math.sin(self.pulse_time) * 0.5
        
        # Scale animation for emphasis
        self.scale += (self.target_scale - self.scale) * 0.1
        
        # Physics for special word types
        if hasattr(self, 'physics_enabled') and self.physics_enabled:
            self.physics_vy += self.gravity
            self.y += self.physics_vy
            
            # Bounce off ground
            if self.y > SCREEN_HEIGHT - 100:
                self.y = SCREEN_HEIGHT - 100
                self.physics_vy *= -self.bounce
                if abs(self.physics_vy) < 0.5:
                    self.physics_vy = 0
        
    def draw(self, screen):
        # Calculate final position with animations
        final_x = self.x + math.sin(self.wobble) * 2
        final_y = self.y + self.float_offset
        
        # Create scaled and rotated surface for advanced effects
        if self.scale != 1.0 or self.rotation != 0:
            # Create temporary surface for transformations
            temp_surf = pygame.Surface((self.width * 2, self.height * 2), pygame.SRCALPHA)
            temp_text = self.font.render(self.text, True, self.color)
            temp_surf.blit(temp_text, (self.width//2, self.height//2))
            
            # Apply transformations
            if self.rotation != 0:
                temp_surf = pygame.transform.rotate(temp_surf, self.rotation)
            if self.scale != 1.0:
                new_size = (int(temp_surf.get_width() * self.scale), int(temp_surf.get_height() * self.scale))
                if new_size[0] > 0 and new_size[1] > 0:
                    temp_surf = pygame.transform.scale(temp_surf, new_size)
            
            # Center the transformed surface
            rect = temp_surf.get_rect()
            rect.center = (final_x + self.width//2, final_y + self.height//2)
            screen.blit(temp_surf, rect.topleft)
        else:
            # Standard drawing with enhanced effects
            # Draw glow effect
            for i in range(int(self.glow_radius * 2)):
                alpha = max(0, 80 - i * 15)
                glow_size = i * 3
                glow_color = (*self.color[:3], alpha)
                
                # Create glow surface
                glow_surf = pygame.Surface((self.width + glow_size, self.height + glow_size), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=8)
                screen.blit(glow_surf, (final_x - glow_size//2, final_y - glow_size//2))
            
            # Draw dynamic shadow based on movement
            shadow_offset_x = self.shadow_offset + math.sin(self.pulse_time) * 2
            shadow_offset_y = self.shadow_offset + math.cos(self.pulse_time) * 1
            shadow_color = (0, 0, 0, 120)
            shadow_text = self.font.render(self.text, True, (0, 0, 0))
            screen.blit(shadow_text, (final_x + shadow_offset_x, final_y + shadow_offset_y))
            
            # Draw main text with enhanced border
            border_color = (255, 255, 255)
            for dx, dy in [(-2,-2), (-2,2), (2,-2), (2,2), (-3,0), (3,0), (0,-3), (0,3)]:
                border_text = self.font.render(self.text, True, border_color)
                screen.blit(border_text, (final_x + dx, final_y + dy))
            
            # Draw main text
            screen.blit(self.rendered, (final_x, final_y))
        
    def is_off_screen(self):
        return self.x + self.width < 0

class RageTypingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🔥 GEN Z TYPING CHAOS 🔥 - No Cap, Just Facts!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
        self.title_font = pygame.font.Font(None, 72)
        
        # Visual effects
        self.screen_shake = 0
        self.bg_stars = []
        self.particles = []
        self.time_elapsed = 0
        self.rainbow_offset = 0
        self.achievement_popup = None
        self.achievement_timer = 0
        self.camera_zoom = 1.0
        self.camera_target_zoom = 1.0
        self.blur_effect = 0
        self.chromatic_offset = 0
        
        # Dynamic backgrounds
        self.bg_elements = []
        self.current_theme = 'default'
        self.init_background_themes()
        
        # Initialize background stars
        for _ in range(50):
            self.bg_stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.1, 0.5),
                'brightness': random.randint(100, 255)
            })
        
        self.reset_game()
        
        # Initialize background elements for themes after level is set
        self.init_theme_elements()
        
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
        self.screen_shake = 0
        self.particles = []
        self.combo_display_timer = 0
        
    def get_words_for_level(self):
        if self.level <= 3:
            return EASY_WORDS
        elif self.level <= 6:
            return MEDIUM_WORDS
        elif self.level <= 9:
            return HARD_WORDS
        else:
            return HACKER_WORDS
            
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
            color = NEON_GREEN
        elif self.level <= 6:
            color = NEON_BLUE
        elif self.level <= 9:
            color = NEON_ORANGE
        else:
            color = NEON_PINK
        
        word = Word(word_text, x, y, speed, color)
        
        # Add special physics for certain words
        if random.random() < 0.2:  # 20% chance for physics words
            word.physics_enabled = True
            word.physics_vy = random.uniform(-3, -1)
            word.gravity = 0.15
        
        # Add special scaling for emphasis
        if len(word_text) > 10:  # Long words get emphasis
            word.target_scale = 1.2
            
        self.words.append(word)
        
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
                    self.combo_display_timer = 60  # Show combo for 1 second
                    
                    # Camera effects for big combos
                    if self.combo > 10:
                        self.camera_target_zoom = 1.1
                        self.blur_effect = 10
                        self.chromatic_offset = 3
                    elif self.combo > 5:
                        self.camera_target_zoom = 1.05
                        self.blur_effect = 5
                    
                    # Add explosion particles with extra pizzazz
                    particle_count = 20 + self.combo * 2  # More particles for higher combos
                    for _ in range(particle_count):
                        self.particles.append({
                            'x': word.x + word.width // 2,
                            'y': word.y + word.height // 2,
                            'vx': random.uniform(-8, 8),
                            'vy': random.uniform(-8, 8),
                            'life': 40 + random.randint(0, 20),
                            'color': word.color,
                            'size': random.randint(2, 6),
                            'trail': []
                        })
                    
                    # Achievement system
                    if self.combo == 5:
                        self.show_achievement("Getting Heated! 🔥")
                    elif self.combo == 10:
                        self.show_achievement("Absolutely Slaying! 💫")
                    elif self.combo == 20:
                        self.show_achievement("No Cap Detective! 🕵️")
                    elif self.combo == 50:
                        self.show_achievement("Periodt Queen! 👑")
                    
                    # Screen shake and effects on combo
                    if self.combo > 5:
                        self.screen_shake = min(15, self.combo)
                    
                    
                    # Word destruction animation
                    word.target_scale = 0.1  # Shrink word before destruction
                    
                    self.current_typed = ""
                    return
                    
        self.combo = 0
        self.current_typed = ""
        
    def update(self):
        if self.game_over:
            return
            
        self.time_elapsed += 1
        
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
            
        # Update combo display timer
        if self.combo_display_timer > 0:
            self.combo_display_timer -= 1
            
        # Update background stars
        for star in self.bg_stars:
            star['x'] -= star['speed']
            if star['x'] < 0:
                star['x'] = SCREEN_WIDTH
                star['y'] = random.randint(0, SCREEN_HEIGHT)
                
        # Update particles with trails
        for particle in self.particles[:]:
            # Store trail positions
            if 'trail' in particle:
                particle['trail'].append((particle['x'], particle['y']))
                if len(particle['trail']) > 5:
                    particle['trail'].pop(0)
            
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['vy'] += 0.3  # Gravity
            particle['vx'] *= 0.98  # Air resistance
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Update camera effects
        self.camera_zoom += (self.camera_target_zoom - self.camera_zoom) * 0.1
        self.camera_target_zoom += (1.0 - self.camera_target_zoom) * 0.05
        
        if self.blur_effect > 0:
            self.blur_effect -= 0.5
        if self.chromatic_offset > 0:
            self.chromatic_offset -= 0.2
        
        # Update rainbow effect
        self.rainbow_offset += 2
        
        # Update achievement popup
        if self.achievement_timer > 0:
            self.achievement_timer -= 1
        
        # Update background theme
        self.update_background_theme()
        
        # Update words
        for word in self.words[:]:
            word.update()
            if word.is_off_screen():
                self.words.remove(word)
                self.lives -= 1
                self.combo = 0
                self.screen_shake = 8  # Shake on life lost
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
            self.screen_shake = 12
            self.camera_target_zoom = 1.2
            
    def draw_gradient_background(self):
        # Get current theme colors
        current_theme = self.get_current_theme()
        theme_colors = self.themes[current_theme]['colors']
        
        # Create animated gradient background with theme
        for y in range(0, SCREEN_HEIGHT, 2):  # Skip lines for performance
            ratio = y / SCREEN_HEIGHT
            # Add time-based color shifting
            shift = math.sin(self.time_elapsed * 0.01) * 15
            
            r = int(theme_colors[0][0] * (1 - ratio) + theme_colors[1][0] * ratio + shift)
            g = int(theme_colors[0][1] * (1 - ratio) + theme_colors[1][1] * ratio)
            b = int(theme_colors[0][2] * (1 - ratio) + theme_colors[1][2] * ratio + shift)
            r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
            
            # Draw double lines for smoother gradient
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
            if y + 1 < SCREEN_HEIGHT:
                pygame.draw.line(self.screen, (r, g, b), (0, y + 1), (SCREEN_WIDTH, y + 1))
    
    def draw(self):
        # Apply screen shake
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        # Draw gradient background
        self.draw_gradient_background()
        
        # Draw themed background elements
        self.draw_background_elements(shake_x, shake_y)
        
        # Draw background stars with theme-appropriate colors
        current_theme = self.get_current_theme()
        for star in self.bg_stars:
            brightness = int(star['brightness'] + math.sin(self.time_elapsed * 0.05 + star['x'] * 0.01) * 50)
            brightness = max(50, min(255, brightness))
            
            if current_theme == 'matrix':
                color = (0, brightness, 0)  # Green for matrix
            elif current_theme == 'tiktok':
                color = (brightness, 0, brightness//2)  # Pink for TikTok
            else:
                color = (brightness//3, brightness//3, brightness)
            
            size = 1 if brightness < 150 else 2
            pygame.draw.circle(self.screen, color, 
                             (int(star['x'] + shake_x), int(star['y'] + shake_y)), size)
        
        # Draw particles with trails and effects
        for particle in self.particles:
            if particle['life'] > 0:
                # Draw particle trail
                if 'trail' in particle and len(particle['trail']) > 1:
                    for i, (tx, ty) in enumerate(particle['trail']):
                        trail_alpha = (i / len(particle['trail'])) * 0.5
                        trail_size = max(1, int(particle.get('size', 3) * trail_alpha))
                        trail_color = tuple(int(c * trail_alpha) for c in particle['color'][:3])
                        if trail_size > 0:
                            pygame.draw.circle(self.screen, trail_color,
                                             (int(tx + shake_x), int(ty + shake_y)), trail_size)
                
                # Draw main particle with pulsing effect
                life_ratio = particle['life'] / 40
                pulse = math.sin(self.time_elapsed * 0.5) * 0.3 + 0.7
                size = max(1, int(particle.get('size', 3) * life_ratio * pulse))
                
                # Rainbow particles for high combos
                if self.combo > 15:
                    hue = (self.rainbow_offset + particle['x']) % 360
                    color = self.hsv_to_rgb(hue, 100, 100)
                else:
                    color = particle['color'][:3]
                
                if size > 0:
                    pygame.draw.circle(self.screen, color,
                                     (int(particle['x'] + shake_x), int(particle['y'] + shake_y)), size)
                    # Add inner glow
                    if size > 2:
                        inner_size = max(1, size - 1)
                        inner_color = tuple(min(255, c + 50) for c in color)
                        pygame.draw.circle(self.screen, inner_color,
                                         (int(particle['x'] + shake_x), int(particle['y'] + shake_y)), inner_size)
        
        # Draw words
        for word in self.words:
            word.draw(self.screen)
            
        # Draw modern UI with glow effects
        self.draw_ui(shake_x, shake_y)
        
    def draw_ui(self, shake_x, shake_y):
        # Create UI panel background
        ui_surface = pygame.Surface((400, 200), pygame.SRCALPHA)
        pygame.draw.rect(ui_surface, (20, 20, 40, 180), ui_surface.get_rect(), border_radius=15)
        pygame.draw.rect(ui_surface, NEON_BLUE, ui_surface.get_rect(), width=2, border_radius=15)
        self.screen.blit(ui_surface, (10 + shake_x, 10 + shake_y))
        
        # Draw UI text with glow and Gen Z flair
        ui_items = [
            (f"SCORE: {self.score:,} 💰", NEON_GREEN, 30),
            (f"LEVEL: {self.level} 🎆", NEON_BLUE, 70),
            (f"LIVES: {'❤️' * self.lives}", NEON_PINK, 110),
            (f"BEST STREAK: {self.max_combo}x 🔥", GOLD, 150)
        ]
        
        for text, color, y_pos in ui_items:
            self.draw_glowing_text(text, self.font, color, 25 + shake_x, y_pos + shake_y)
        
        # Draw current combo with enhanced effects
        if self.combo > 0 and self.combo_display_timer > 0:
            combo_size = min(100, 36 + self.combo * 3)
            combo_font = pygame.font.Font(None, combo_size)
            pulse = math.sin(self.time_elapsed * 0.3) * 0.3 + 1
            
            # Chromatic aberration effect for high combos
            if self.combo > 15:
                combo_color = self.hsv_to_rgb((self.rainbow_offset * 3) % 360, 100, 100)
                combo_text = f"PERIODT QUEEN {self.combo}x! 👑🔥💫"
                # Draw with chromatic aberration
                self.draw_chromatic_text(combo_text, combo_font, combo_color, 
                                       SCREEN_WIDTH//2, 180 + shake_y, self.chromatic_offset)
            elif self.combo > 10:
                combo_color = self.hsv_to_rgb((self.rainbow_offset * 2) % 360, 100, 100)
                combo_text = f"ABSOLUTELY SLAYING {self.combo}x! 🔥🔥🔥"
                text_width = combo_font.size(combo_text)[0]
                self.draw_glowing_text(combo_text, combo_font, combo_color, 
                                     SCREEN_WIDTH//2 - text_width//2 + shake_x, 180 + shake_y)
            elif self.combo > 5:
                combo_color = (int(NEON_PINK[0] * pulse), int(NEON_PINK[1] * pulse), int(NEON_PINK[2] * pulse))
                combo_text = f"NO CAP {self.combo}x! 💫"
                text_width = combo_font.size(combo_text)[0]
                self.draw_glowing_text(combo_text, combo_font, combo_color, 
                                     SCREEN_WIDTH//2 - text_width//2 + shake_x, 200 + shake_y)
            else:
                combo_color = (int(NEON_YELLOW[0] * pulse), int(NEON_YELLOW[1] * pulse), int(NEON_YELLOW[2] * pulse))
                combo_text = f"COMBO {self.combo}x!"
                text_width = combo_font.size(combo_text)[0]
                self.draw_glowing_text(combo_text, combo_font, combo_color, 
                                     SCREEN_WIDTH//2 - text_width//2 + shake_x, 220 + shake_y)
        
        # Draw achievement popup
        if self.achievement_popup and self.achievement_timer > 0:
            self.draw_achievement_popup(shake_x, shake_y)
        
        # Draw typing area with modern design
        input_bg = pygame.Surface((600, 60), pygame.SRCALPHA)
        pygame.draw.rect(input_bg, (30, 30, 50, 200), input_bg.get_rect(), border_radius=10)
        pygame.draw.rect(input_bg, NEON_GREEN, input_bg.get_rect(), width=3, border_radius=10)
        self.screen.blit(input_bg, (SCREEN_WIDTH//2 - 300 + shake_x, SCREEN_HEIGHT - 80 + shake_y))
        
        typed_text = f"► {self.current_typed}"
        self.draw_glowing_text(typed_text, self.large_font, WHITE, 
                             SCREEN_WIDTH//2 - 280 + shake_x, SCREEN_HEIGHT - 65 + shake_y)
    
    def draw_glowing_text(self, text, font, color, x, y):
        # Ensure color is RGB tuple (3 values)
        if len(color) > 3:
            color = color[:3]
        
        # Draw glow effect with proper color handling
        for i in range(3):
            glow_intensity = max(50, 150 - i * 40)
            glow_color = tuple(min(255, max(0, int(c * (glow_intensity / 255)))) for c in color)
            
            try:
                glow_surf = font.render(text, True, glow_color)
                for dx, dy in [(-i-1, -i-1), (-i-1, i+1), (i+1, -i-1), (i+1, i+1)]:
                    self.screen.blit(glow_surf, (x + dx, y + dy))
            except:
                pass  # Skip if color is invalid
        
        # Draw main text
        try:
            main_text = font.render(text, True, color)
            self.screen.blit(main_text, (x, y))
        except:
            # Fallback to white if color is invalid
            main_text = font.render(text, True, WHITE)
            self.screen.blit(main_text, (x, y))
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB for rainbow effects"""
        h = h % 360
        s = s / 100
        v = v / 100
        
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    def show_achievement(self, text):
        """Show achievement popup with effects"""
        self.achievement_popup = text
        self.achievement_timer = 180  # 3 seconds at 60 FPS
        self.screen_shake = max(self.screen_shake, 8)
        self.camera_target_zoom = 1.15
    
    def draw_achievement_popup(self, shake_x, shake_y):
        """Draw the achievement popup with animation"""
        if not self.achievement_popup:
            return
        
        # Popup animation
        progress = 1 - (self.achievement_timer / 180)
        if progress < 0.2:
            scale = progress / 0.2  # Scale in
        elif progress > 0.8:
            scale = (1 - progress) / 0.2  # Scale out
        else:
            scale = 1
        
        # Popup background
        popup_width = 400
        popup_height = 80
        popup_x = SCREEN_WIDTH // 2 - popup_width // 2
        popup_y = 100
        
        # Scale the popup
        scaled_width = int(popup_width * scale)
        scaled_height = int(popup_height * scale)
        scaled_x = popup_x + (popup_width - scaled_width) // 2
        scaled_y = popup_y + (popup_height - scaled_height) // 2
        
        if scale > 0:
            popup_surf = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
            pygame.draw.rect(popup_surf, (50, 20, 80, 240), popup_surf.get_rect(), border_radius=15)
            pygame.draw.rect(popup_surf, GOLD, popup_surf.get_rect(), width=3, border_radius=15)
            self.screen.blit(popup_surf, (scaled_x + shake_x, scaled_y + shake_y))
            
            # Achievement text
            if scale > 0.5:  # Only show text when popup is large enough
                text_color = self.hsv_to_rgb((self.rainbow_offset * 3) % 360, 80, 100)
                text_surface = self.large_font.render(self.achievement_popup, True, text_color)
                text_x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
                text_y = popup_y + 25
                self.screen.blit(text_surface, (text_x + shake_x, text_y + shake_y))
    
    def removed_load_sounds(self):
        """Load sound effects (gracefully handles missing files)"""
        sound_files = {
            'word_destroy': 'sounds/destroy.wav',
            'combo_5': 'sounds/combo5.wav',
            'combo_10': 'sounds/combo10.wav',
            'achievement': 'sounds/achievement.wav',
            'life_lost': 'sounds/life_lost.wav',
            'game_over': 'sounds/game_over.wav',
            'level_up': 'sounds/level_up.wav',
            'typing': 'sounds/type.wav'
        }
        
        # Try to initialize pygame mixer
        try:
            pygame.mixer.init()
        except:
            self.sound_enabled = False
            print("🔇 Sound system disabled (no audio device)")
            return
        
        # Load sound files if they exist
        for sound_name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    print(f"🔊 Loaded {sound_name}")
                else:
                    print(f"🔇 Sound file missing: {file_path} (will run silently)")
            except Exception as e:
                print(f"🔇 Could not load {sound_name}: {e}")
    
    def removed_play_sound(self, sound_name):
        """Play sound effect if available"""
        if self.sound_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass  # Fail silently if sound can't play
    
    def init_background_themes(self):
        """Initialize different background themes for levels"""
        self.themes = {
            'default': {'name': 'Cyber Space', 'colors': [(20, 20, 40), (40, 20, 60)]},
            'discord': {'name': 'Discord Dark Mode', 'colors': [(35, 39, 42), (47, 49, 54)]},
            'instagram': {'name': 'Insta Vibes', 'colors': [(225, 48, 108), (255, 122, 89)]},
            'tiktok': {'name': 'TikTok Energy', 'colors': [(0, 0, 0), (255, 0, 80)]},
            'matrix': {'name': 'Matrix Code', 'colors': [(0, 20, 0), (0, 40, 0)]}
        }
    
    def init_theme_elements(self):
        """Initialize theme-specific background elements"""
        self.bg_elements = []
        
        # Add floating emojis and symbols based on level
        emoji_sets = {
            1: ['💻', '📱', '⚡', '🔥'],
            2: ['😎', '💯', '🚀', '✨'],
            3: ['👑', '💎', '🌟', '🎯'],
            4: ['🎮', '🕹️', '👾', '🤖']
        }
        
        current_emojis = emoji_sets.get(min(4, (self.level // 3) + 1), emoji_sets[1])
        
        for _ in range(20):
            self.bg_elements.append({
                'type': 'emoji',
                'emoji': random.choice(current_emojis),
                'x': random.randint(-100, SCREEN_WIDTH + 100),
                'y': random.randint(-100, SCREEN_HEIGHT + 100),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'rotation': 0,
                'scale': random.uniform(0.5, 1.5),
                'alpha': random.randint(30, 100)
            })
    
    def update_background_theme(self):
        """Update background elements"""
        for element in self.bg_elements:
            if element['type'] == 'emoji':
                element['x'] += element['vx']
                element['y'] += element['vy']
                element['rotation'] += 0.5
                
                # Wrap around screen
                if element['x'] < -100:
                    element['x'] = SCREEN_WIDTH + 100
                elif element['x'] > SCREEN_WIDTH + 100:
                    element['x'] = -100
                if element['y'] < -100:
                    element['y'] = SCREEN_HEIGHT + 100
                elif element['y'] > SCREEN_HEIGHT + 100:
                    element['y'] = -100
    
    def get_current_theme(self):
        """Get theme based on current level"""
        if self.level <= 3:
            return 'default'
        elif self.level <= 6:
            return 'discord'
        elif self.level <= 9:
            return 'instagram'
        elif self.level <= 12:
            return 'tiktok'
        else:
            return 'matrix'
        
        # Game over screen with modern design
        if self.game_over:
            self.draw_game_over_screen()
    
    def draw_game_over_screen(self):
        # Animated overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = min(180, self.time_elapsed * 3)
        overlay.fill((0, 0, 0, alpha))
        self.screen.blit(overlay, (0, 0))
        
        # Pulsing game over effect
        pulse = math.sin(self.time_elapsed * 0.1) * 0.3 + 1
        
        # Main game over panel
        panel_width, panel_height = 600, 400
        panel_x = SCREEN_WIDTH // 2 - panel_width // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
        
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel, (20, 20, 40, 220), panel.get_rect(), border_radius=20)
        pygame.draw.rect(panel, NEON_PINK, panel.get_rect(), width=4, border_radius=20)
        self.screen.blit(panel, (panel_x, panel_y))
        
        # Game over title with rainbow effect
        title_color = self.hsv_to_rgb((self.rainbow_offset * pulse) % 360, 100, 100)
        self.draw_glowing_text("GAME OVER! 😭📱", self.title_font, title_color, 
                             SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 120)
        
        # Stats display
        stats = [
            f"Final Score: {self.score:,}",
            f"Max Level: {self.level}",
            f"Best Combo: {self.max_combo}x"
        ]
        
        for i, stat in enumerate(stats):
            self.draw_glowing_text(stat, self.large_font, NEON_BLUE, 
                                 SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 - 40 + i * 40)
        
        # Instructions with Gen Z flair
        instruction_pulse = math.sin(self.time_elapsed * 0.2) * 50 + 200
        instruction_color = (instruction_pulse, instruction_pulse, 255)
        self.draw_glowing_text("Press SPACE to restart or ESC to rage quit 😤", self.font, instruction_color,
                             SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 + 120)
        
        # Add motivational Gen Z message
        if self.score > 1000:
            motivation = "You absolutely slayed bestie! 👑"
        elif self.score > 500:
            motivation = "That was lowkey fire though 🔥"
        elif self.score > 100:
            motivation = "Not bad, could be better tho 😏"
        else:
            motivation = "Oop, that was kinda sus ngl 😬"
        
        self.draw_glowing_text(motivation, self.font, NEON_GREEN,
                             SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 160)
    
    def draw_background_elements(self, shake_x, shake_y):
        """Draw themed background elements like floating emojis"""
        font = pygame.font.Font(None, 48)
        
        for element in self.bg_elements:
            if element['type'] == 'emoji':
                # Create rotated emoji surface
                emoji_surf = font.render(element['emoji'], True, (255, 255, 255, element['alpha']))
                
                if element['rotation'] != 0:
                    emoji_surf = pygame.transform.rotate(emoji_surf, element['rotation'])
                
                if element['scale'] != 1.0:
                    new_size = (int(emoji_surf.get_width() * element['scale']), 
                               int(emoji_surf.get_height() * element['scale']))
                    if new_size[0] > 0 and new_size[1] > 0:
                        emoji_surf = pygame.transform.scale(emoji_surf, new_size)
                
                # Apply transparency
                emoji_surf.set_alpha(element['alpha'])
                
                rect = emoji_surf.get_rect()
                rect.center = (element['x'] + shake_x, element['y'] + shake_y)
                self.screen.blit(emoji_surf, rect.topleft)
    
    def draw_chromatic_text(self, text, font, color, center_x, y, offset):
        """Draw text with chromatic aberration effect"""
        if offset <= 0:
            text_surf = font.render(text, True, color)
            rect = text_surf.get_rect()
            rect.centerx = center_x
            rect.y = y
            self.screen.blit(text_surf, rect.topleft)
            return
        
        # Red channel (shifted left)
        red_color = (color[0], 0, 0)
        red_surf = font.render(text, True, red_color)
        red_rect = red_surf.get_rect()
        red_rect.centerx = center_x - offset
        red_rect.y = y
        self.screen.blit(red_surf, red_rect.topleft)
        
        # Blue channel (shifted right)
        blue_color = (0, 0, color[2] if len(color) > 2 else color[1])
        blue_surf = font.render(text, True, blue_color)
        blue_rect = blue_surf.get_rect()
        blue_rect.centerx = center_x + offset
        blue_rect.y = y
        self.screen.blit(blue_surf, blue_rect.topleft)
        
        # Green channel (center)
        green_color = (0, color[1], 0)
        green_surf = font.render(text, True, green_color)
        green_rect = green_surf.get_rect()
        green_rect.centerx = center_x
        green_rect.y = y
        self.screen.blit(green_surf, green_rect.topleft)
            
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    self.handle_typing(event)
            
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = RageTypingGame()
    game.run()
