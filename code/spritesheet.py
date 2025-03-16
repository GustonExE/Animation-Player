from settings import *

# Manages loading and unloading of textures to avoid redundant loading
class ResourceManager:
    images = {}  # Stores loaded textures

    @staticmethod
    def load_texture(filename):
        # Load texture only if it's not already loaded
        if filename not in ResourceManager.images:
            image = load_image(filename)  # Load image from file
            texture = load_texture_from_image(image)  # Convert to texture
            unload_image(image)  # Free the image from memory
            ResourceManager.images[filename] = texture  # Store texture
        return ResourceManager.images[filename]

    @staticmethod
    def unload_texture(filename):
        # Unload texture if it exists
        if filename in ResourceManager.images:
            unload_texture(ResourceManager.images[filename])
            del ResourceManager.images[filename]

# Handles spritesheets and extracting specific frames
class Spritesheet:
    def __init__(self, filename, pos, scale: Vector2, frame_h, frame_v, current_frame: Vector2):
        self.filename = filename
        self.pos = pos  # Position on screen
        self.scale = Vector2(scale.x, scale.y)  # Scaling factor
        self.frame = current_frame  # Current frame in the spritesheet
        self.frame_h = frame_h  # Total horizontal frames
        self.frame_v = frame_v  # Total vertical frames
        self.texture = ResourceManager.load_texture(self.filename)  # Load texture
        
        # Define the section of the spritesheet to display
        self.rect = Rectangle(
            self.frame.x * (self.texture.width / self.frame_h), 
            self.frame.y * (self.texture.height / self.frame_v), 
            (self.texture.width / self.frame_h), 
            (self.texture.height / self.frame_v)
        )
        self.sprite_box = Rectangle(self.pos.x, self.pos.y, self.rect.width * self.scale.x, self.rect.height * self.scale.y)
        
    def destroy(self):
        ResourceManager.unload_texture(self.filename)  # Unload texture
    
    def draw(self):
        self.sprite_box.x = self.pos.x
        self.sprite_box.y = self.pos.y
        
        # Draw the selected frame at the specified position with scaling
        draw_texture_pro(
            self.texture, self.rect, self.sprite_box, 
            Vector2(0, 0), 0, WHITE
        )

# Handles function callbacks at specific animation frames
class Callback:
    def __init__(self, callback_frame, callback_func, *args, **kwargs):
        self.callback_frame = callback_frame  # Frame at which to trigger
        self.callback_func = callback_func  # Function to call
        self.args = args if args else ()  # Additional arguments
        self.kwargs = kwargs if kwargs else {}  # Additional keyword arguments
    
    def run(self):
        self.callback_func(*self.args, **self.kwargs)  # Execute callback

# Handles animation logic for a spritesheet
class Animation:
    def __init__(self, spritesheet, start_frame, end_frame, loop, 
                 vertical_anim: bool=False, speed: float = 10, 
                 reverse: bool = False, callbacks: list={}):
        
        self.spritesheet = spritesheet  # Spritesheet reference
        self.start_frame = start_frame  # First frame
        self.end_frame = end_frame  # Last frame
        self.loop = loop  # Should the animation loop?
        self.speed = speed  # Animation speed
        self.reverse = reverse  # Play animation in reverse?
        self.vertical_anim = vertical_anim  # Vertical or horizontal animation
        self.callbacks = callbacks  # Callbacks dictionary
        
        self.frame_attr = 'y' if self.vertical_anim else 'x'  # Determine frame direction
        self.initial_frame = self.end_frame if self.reverse else self.start_frame  # Start at correct frame
        setattr(self.spritesheet.frame, self.frame_attr, self.initial_frame)  # Set frame
        
        self.current_frame = getattr(self.spritesheet.frame, self.frame_attr)  # Store current frame
        self.frame_counter = 0  # Frame counter for timing

    def update(self):
        self.animate()  # Update animation frame
        self.handle_callbacks()  # Trigger callbacks
        
        # Update texture rectangle position
        self.current_frame = getattr(self.spritesheet.frame, self.frame_attr)
        self.spritesheet.rect.x = self.spritesheet.frame.x * (self.spritesheet.texture.width / self.spritesheet.frame_h)
        self.spritesheet.rect.y = self.spritesheet.frame.y * (self.spritesheet.texture.height / self.spritesheet.frame_v)
        # Sync sprite_box with pos
        self.spritesheet.sprite_box.x = self.spritesheet.pos.x
        self.spritesheet.sprite_box.y = self.spritesheet.pos.y
        
    def animate(self):
        # Check if enough time has passed for the next frame
        if self.frame_counter >= (get_fps() / self.speed):
            step = -1 if self.reverse else 1
            new_frame = self.current_frame + step
            setattr(self.spritesheet.frame, self.frame_attr, new_frame)

            if self.is_finished():
                if self.loop:
                    # Reset to start or end depending on reverse flag
                    new_frame = self.end_frame if self.reverse else self.start_frame
                    setattr(self.spritesheet.frame, self.frame_attr, new_frame)
                else:
                    # Stop at the correct frame
                    new_frame = self.start_frame if self.reverse else self.end_frame
                    setattr(self.spritesheet.frame, self.frame_attr, new_frame)
            
            self.current_frame = new_frame
            self.frame_counter = 0  # Reset counter
        
        self.frame_counter += 1  # Increment counter

    def handle_callbacks(self):
        if not is_empty(self.callbacks):
            invalid_callbacks = []  # Store invalid keys
            for callback in list(self.callbacks):
                try:
                    self.callbacks[callback].run()  # Run callback
                except AttributeError:
                    invalid_callbacks.append(callback)  # Mark for removal
                    print("Warning /!\: Callback object must be of type Callback!")
            for callback in invalid_callbacks:
                self.callbacks.pop(callback)  # Remove invalid callbacks

    def set_speed(self, new_speed):
        self.speed = new_speed
    
    def set_loop(self, loop):
        self.loop = loop
        
    def set_reversed(self, reverse):
        self.reverse = reverse
    
    def set_animation_vertical(self, vertical_anim):
        self.vertical_anim = vertical_anim

    def reset(self):
        setattr(self.spritesheet.frame, self.frame_attr, self.start_frame)
        self.frame_counter = 0

    def is_finished(self):
        return (self.reverse and self.current_frame <= self.start_frame) or \
               (not self.reverse and self.current_frame >= self.end_frame)

    def draw(self):
        self.spritesheet.draw()

    def run(self):
        self.update()
        self.draw()

# Handles multiple animations and switching between them
class AnimationPlayer:
    def __init__(self, animation_dict, default_animation):
        self.animation_dict = animation_dict  # Dictionary of animations
        self.default_animation = default_animation  # Default animation name
        self.current_animation = self.animation_dict[self.default_animation]  # Current animation
        self.play(self.default_animation)
        
    def play(self, animation_name):
        if animation_name in self.animation_dict:
            self.current_animation = self.animation_dict[animation_name]
            self.current_animation.reset()  # Reset animation when switching

    def destroy(self):
        for animation in self.animation_dict.values():
            animation.spritesheet.destroy()  # Destroy all spritesheets

    def run(self):
        self.current_animation.update()  # Update animation frames
        self.current_animation.draw()  # Draw the updated frame