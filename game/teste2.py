game_state, music_on, sound_on, key_cooldown = "menu", True, True, 0
platforms, obstacles, enemies = [], [], []

# --- NEW REUSABLE ANIMATION CLASS ---
class AnimationController:
    """Manages animation state and frame switching for an Actor."""
    def __init__(self, actor, animations, initial_state):
        self.actor = actor
        self.animations = animations
        self.state = initial_state
        self.frame_index = 0
        self.timer = 0

    def set_state(self, new_state):
        """Changes the current animation state."""
        if self.state != new_state and new_state in self.animations:
            self.state = new_state
            self.frame_index = 0 # Reset animation when state changes
            self.timer = 0

    def update(self):
        """Updates the animation frame based on the timer and duration."""
        if self.state not in self.animations:
            return

        anim_data = self.animations[self.state]
        frames = anim_data["frames"]
        duration = anim_data["duration"]

        self.timer += 1
        if self.timer >= duration:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.actor.image = frames[self.frame_index]

# --- BASE ENTITY CLASS (Optional but good for shared physics) ---
class Entity:
    """Base class for all moving entities with basic physics."""
    def __init__(self, x, y, image_name):
        self.actor = Actor(image_name, (x, y))
        self.vel_y, self.gravity = 0, 0.5
        self.dead, self.on_ground = False, False

    def rect(self):
        # Default rect for collision (can be overridden)
        return Rect(self.actor.x - 8, self.actor.y - 16, 16, 32)

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.actor.y += self.vel_y

    def check_platform_collisions(self):
        self.on_ground = False
        hr = self.rect()
        for b in platforms:
            br = Rect(b.x - 9, b.y - 9, 18, 18)
            # Simplified collision check for falling onto a platform
            if hr.colliderect(br) and self.vel_y > 0 and self.actor.y < b.y:
                self.actor.y = b.y - 18
                self.vel_y = 0
                self.on_ground = True

# --- REFACTORED HERO CLASS ---
class Hero(Entity): # Inherits from Entity
    def __init__(self, x, y):
        # Define all animation states for the Hero
        hero_animations = {
            "idle": {"frames": ["hero_idle1", "hero_idle2", "hero_idle3", "hero_idle4"], "duration": 12},
            "walk": {"frames": ["hero_walk1", "hero_walk2", "hero_walk3", "hero_walk4"], "duration": 8},
            # Add "jump", "fall", "death" animations here as needed
        }
        
        # Initialize base Entity with the starting image
        super().__init__(x, y, hero_animations["idle"]["frames"][0])
        
        # Use composition for animation
        self.animator = AnimationController(self.actor, hero_animations, "idle")

    def update(self): 
        if self.dead:
            return
        self.handle_input()
        self.apply_gravity()
        self.check_platform_collisions()
        
        # Delegate animation update to the controller
        self.animator.update()
    
    def handle_input(self):
        move = 0
        if keyboard.left:
            self.actor.x -= 3
            move = -1
        elif keyboard.right:
            self.actor.x += 3
            move = 1
        
        if self.on_ground and keyboard.up:
            self.vel_y = -10
        
        self.actor.flip_x = move < 0
        
        # Update animation state based on movement
        new_state = "walk" if move else "idle"
        self.animator.set_state(new_state)

# --- REFACTORED ENEMY CLASS ---
class Enemy(Entity): # Inherits from Entity
    def __init__(self, x, y, left, right):
        # Define the single animation state for the Enemy
        enemy_animations = {
            "walk": {"frames": ["enemy_walk1", "enemy_walk2", "enemy_walk3"], "duration": 8},
        }
        
        # Initialize base Entity with the starting image
        super().__init__(x, y, enemy_animations["walk"]["frames"][0])
        
        # Enemy-specific properties
        self.left_limit, self.right_limit = left, right
        self.direction = 1 # 1 for right, -1 for left
        
        # Use composition for animation
        self.animator = AnimationController(self.actor, enemy_animations, "walk")

    def rect(self):
        # Enemy has a smaller collision box
        return Rect(self.actor.x - 8, self.actor.y - 8, 16, 16)

    def update(self):
        # Movement logic
        self.actor.x += self.direction * 2
        if self.actor.x <= self.left_limit or self.actor.x >= self.right_limit:
            self.direction *= -1
            self.actor.flip_x = self.direction < 0
        
        # Delegate animation update to the controller
        self.animator.update()

# --- GAME SETUP AND MAIN LOOP (Rest of your original code) ---

hero = Hero(100, 100)
enemies.extend([Enemy(300, 200, 260, 340), Enemy(500, 150, 460, 560)])

def load_map(path): # ! MAPA
    try:
        with open(path) as f:
            for y, line in enumerate(f.read().strip().split("\n")):
                for x, val in enumerate(line.split(",")):
                    if val in ["21", "22", "23"]:
                        img = "block1"
                    elif val in ["153", "154", "155", "156"]:
                        img = "cloud"
                    else:
                        continue
                    a = Actor(img)
                    a.x, a.y = x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2
                    platforms.append(a)
    except Exception as e:
        print("Erro ao carregar mapa:", e)

def load_obstacles(path):
    for y, line in enumerate(open(path).read().strip().split("\n")):
        for x, val in enumerate(line.split(",")):
            if val != "-1":
                a = Actor("obstacle")
                a.x, a.y = x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2
                obstacles.append(a)

# NOTE: The file paths below are likely incorrect for the sandbox environment.
# They are kept here to match your original code structure, but you will need
# to adjust them to run the game on your machine.
# load_map('C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv')
# load_obstacles('C:/Users/PC/Documents/GitHub/roguelike/game/obstacles.csv')

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.play("bg_music")
    else:
        music.stop()

def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        sounds.menu_click.play()

def start_music():
    if music_on:
        music.play("bg_music")

def draw_menu():
    screen.clear()
    screen.draw.text("MAIN MENU", center=(WIDTH // 2, 80), fontsize=50, color="white")
    for i, txt in enumerate([
        "1 - Start Game",
        f"2 - Music: {'ON' if music_on else 'OFF'}",
        f"3 - Sounds: {'ON' if sound_on else 'OFF'}",
        "4 - Exit"
    ]):
        screen.draw.text(txt, center=(WIDTH // 2, 180 + i * 70), fontsize=40)

def update_menu():
    global game_state, key_cooldown
    if key_cooldown > 0:
        key_cooldown -= 1
        return
    if keyboard.K_1:
        start_game()
    elif keyboard.K_2:
        toggle_music()
        if sound_on: sounds.menu_click.play()
        key_cooldown = 10
    elif keyboard.K_3:
        toggle_sound()
        key_cooldown = 10
    elif keyboard.K_4:
        exit()

def start_game():
    global game_state
    if sound_on: sounds.menu_click.play()
    game_state = "playing"

def update():
    if game_state == "menu":
        update_menu()
        return
    if hero.dead:
        return
    hero.update()
    for e in enemies:
        e.update()
    check_collisions()

def check_collisions():
    global game_state
    r = hero.rect()
    for e in enemies:
        if r.colliderect(e.rect()):
            hero.dead = True
            game_state = "dead"
            return
    for o in obstacles:
        if r.colliderect(Rect(o.x - 8, o.y - 8, 16, 16)):
            hero.dead = True
            game_state = "dead"

def draw():
    screen.clear()
    
    if game_state == "menu":
        draw_menu()
        return
    for b in platforms:
        b.draw()
    for o in obstacles:
        o.draw()
    for e in enemies:
        e.actor.draw()
    hero.actor.draw()

    if game_state == "dead":
        screen.draw.text(
            "YOU DIED!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60,
            color="red", shadow=(2, 2)
        )
start_music()
# pgzrun.go() # Commented out to avoid running in the sandbox