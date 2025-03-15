from settings import *

class Spritesheet:
    def __init__(self, filename, pos, scale ,frame_h, frame_v, current_frame: Vector2):
        self.filename = filename
        self.pos = pos
        self.scale = scale
        self.frame = current_frame
        self.frame_h = frame_h
        self.frame_v = frame_v
        self.image = load_image(self.filename)
        self.texture = load_texture_from_image(self.image)
        self.rect = Rectangle(self.frame.x * self.image.width/self.frame_h, self.frame.y * self.image.height/self.frame_v, 
                 self.texture.width/self.frame_h , self.texture.height/self.frame_v )

    def draw(self):
        draw_texture_pro(
            self.texture, self.rect, 
            Rectangle(self.pos.x, self.pos.y, self.rect.width * self.scale, self.rect.height * self.scale), 
            Vector2(0, 0), 0, WHITE
        )   
             
class Animation:
    def __init__(self, start_frame, end_frame, speed, loop, reverse):
        self.start_frame, self.end_frame = start_frame, end_frame
        self.speed = speed
        self.loop = loop
        self.reverse = reverse
        

class AnimationPlayer:
    def __init__(self, spritesheet, speed, animation_dict: dict, default_animation, vertical_anim: bool, loop, reverse, callbacks: dict):
        self.spritesheet = spritesheet
        self.speed = speed
        self.current_animation = default_animation
        self.animation_dict = animation_dict
        self.animation_manager = self.animation_dict[self.current_animation]
        self.starting_frame = self.animation_manager["start_frame"]
        self.ending_frame =  self.animation_manager["end_frame"]
        self.callbacks = callbacks
        
        # some very important variables
        self.vertical_anim = vertical_anim
        self.loop = loop
        self.reverse = reverse

        self.spritesheet.frame = Vector2(self.starting_frame, self.spritesheet.frame.y)
        self.frame_counter = 0
        self.frame_attr = 'x' if not self.vertical_anim else 'y'
        
    def update(self):
        self.play(self.current_animation)
        self.animate()
        self.handle_callbacks()
        self.frame_counter += 1
        
        self.frame_attr = 'x' if not self.vertical_anim else 'y'
        
        if self.reverse:
            self.starting_frame, self.ending_frame = self.ending_frame, self.starting_frame
                
        self.spritesheet.rect.x = self.spritesheet.frame.x * (self.spritesheet.image.width / self.spritesheet.frame_h)
        self.spritesheet.rect.y = self.spritesheet.frame.y * (self.spritesheet.image.height / self.spritesheet.frame_v)
        
    
    def handle_callbacks(self):
        if self.current_animation == self.callbacks["falling"]["anim"]:
            if getattr(self.spritesheet.frame, self.frame_attr) == self.callbacks["falling"]["frame"]:
                self.callbacks['falling']['callback']()
    
    def animate(self):
        if self.frame_counter >= (framerate / self.speed):
            step = -1 if self.reverse else 1
            setattr(self.spritesheet.frame, self.frame_attr, getattr(self.spritesheet.frame, self.frame_attr) + step)
            
            if self.animation_finished(): 
                if self.loop:
                    setattr(self.spritesheet.frame, self.frame_attr, self.starting_frame)
                else:
                    setattr(self.spritesheet.frame, self.frame_attr, self.ending_frame)
            
            self.frame_counter = 0 
  
    def play(self, animation):
        if animation != self.current_animation:
            self.current_animation = animation
            self.animation_manager = self.animation_dict[animation]
            
            self.starting_frame = self.animation_manager["start_frame"]
            self.ending_frame = self.animation_manager["end_frame"]

            self.starting_frame = self.ending_frame if self.reverse else self.starting_frame
            
            if self.vertical_anim:
                self.spritesheet.frame.y = self.starting_frame
            else:
                self.spritesheet.frame.x = self.starting_frame
            self.frame_counter = 0

    def set_speed(self, new_speed):
        self.speed = new_speed

    def animation_finished(self):
        if self.reverse:
            return getattr(self.spritesheet.frame, self.frame_attr) <= self.ending_frame
        return getattr(self.spritesheet.frame, self.frame_attr) >= self.ending_frame
        
    def draw(self):
        self.spritesheet.draw()
    
    def run(self):
        self.update()
        self.draw()
