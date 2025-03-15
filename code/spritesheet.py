from settings import *

class Spritesheet:
    def __init__(self, filename, pos, scale, frame_h, frame_v, current_frame: Vector2):
        self.filename = filename
        self.pos = pos
        self.scale = scale
        self.frame = current_frame
        self.frame_h = frame_h
        self.frame_v = frame_v
        self.image = load_image(self.filename)
        self.texture = load_texture_from_image(self.image)
        self.rect = Rectangle(self.frame.x * self.image.width / self.frame_h, self.frame.y * self.image.height / self.frame_v, 
                              self.texture.width / self.frame_h, self.texture.height / self.frame_v)

    def draw(self):
        draw_texture_pro(
            self.texture, self.rect, 
            Rectangle(self.pos.x, self.pos.y, self.rect.width * self.scale, self.rect.height * self.scale), 
            Vector2(0, 0), 0, WHITE
        )
            
        
class Animation:
    def __init__(self, spritesheet, start_frame, end_frame, loop, 
                 vertical_anim: bool=False, speed: float = 10, 
                 reverse: bool = False):
        
        # Variables
        self.spritesheet = spritesheet
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.loop = loop
        self.speed = speed
        self.reverse = reverse
        self.vertical_anim = vertical_anim
        
        
        self.frame_attr = 'y' if self.vertical_anim else 'x'
        self.initial_frame = self.end_frame if self.reverse else self.start_frame
        setattr(self.spritesheet.frame, self.frame_attr, self.initial_frame)
        
        self.current_frame = getattr(self.spritesheet.frame, self.frame_attr)

        self.frame_counter = 0

    def update(self):
        self.animate()
        
        self.current_frame = getattr(self.spritesheet.frame, self.frame_attr)
        print(self.initial_frame)
        
        self.spritesheet.rect.x = self.spritesheet.frame.x * (self.spritesheet.image.width / self.spritesheet.frame_h)
        self.spritesheet.rect.y = self.spritesheet.frame.y * (self.spritesheet.image.height / self.spritesheet.frame_v)
        
    def animate(self):
        if self.frame_counter >= (framerate / self.speed):
            step = -1 if self.reverse else 1
            new_frame = self.current_frame + step
            setattr(self.spritesheet.frame, self.frame_attr, new_frame)

            if self.is_finished():
                if self.loop:
                    # Reset to the correct loop start
                    new_frame = self.end_frame if self.reverse else self.start_frame
                    setattr(self.spritesheet.frame, self.frame_attr, new_frame)
                else:
                    # Ensure it stops at the correct frame
                    new_frame = self.start_frame if self.reverse else self.end_frame
                    setattr(self.spritesheet.frame, self.frame_attr, new_frame)

            self.current_frame = new_frame
            self.frame_counter = 0  # Reset counter

        self.frame_counter += 1





    def set_speed(self, new_speed):
        self.speed = new_speed

    def reset(self):
        setattr(self.spritesheet.frame, self.frame_attr, self.start_frame)
        self.frame_counter = 0

    def is_finished(self):
        if self.reverse:
            return self.current_frame <= self.start_frame  # Stop at start when reversing
        return self.current_frame >= self.end_frame 

    def draw(self):
        self.spritesheet.draw()

    def run(self):
        self.update()
        self.draw()

class AnimationPlayer:
    def __init__(self, animation_dict, default_animation):
        self.animation_dict = animation_dict
        self.current_animation = self.animation_dict[default_animation]

    def play(self, animation_name):
        if animation_name in self.animation_dict:
            self.current_animation = self.animation_dict[animation_name]
            self.current_animation.reset()  # Reset animation when switching

    def run(self):
        self.current_animation.update()  # Update animation frames
        self.current_animation.draw()    # Draw the updated frame

        
# class AnimationPlayer:              
#     def __init__(self, spritesheet, animation_dict: dict, default_animation: str, callbacks: dict):
#         self.spritesheet = spritesheet
#         self.current_animation = default_animation
#         self.animation_dict = animation_dict
#         self.animation = self.animation_dict[self.current_animation]
#         self.starting_frame = self.animation.start_frame
#         self.ending_frame = self.animation.end_frame
#         self.speed = self.animation.speed
#         self.callbacks = callbacks
#         self.vertical_anim = self.animation.vertical_anim
#         self.loop = self.animation.loop
#         self.reverse = self.animation.reverse
#         self.spritesheet.frame = Vector2(self.starting_frame, self.spritesheet.frame.y)
#         self.frame_counter = 0
#         self.frame_attr = 'y' if self.vertical_anim else 'x'
        
#     def update(self):
#         self.play(self.current_animation)
#         self.animate()
#         self.handle_callbacks()
#         self.frame_counter += 1
#         self.spritesheet.rect.x = self.spritesheet.frame.x * (self.spritesheet.image.width / self.spritesheet.frame_h)
#         self.spritesheet.rect.y = self.spritesheet.frame.y * (self.spritesheet.image.height / self.spritesheet.frame_v)
    
#     def handle_callbacks(self):
        
#             if self.current_animation in self.callbacks:
#                 if getattr(self.spritesheet.frame, self.frame_attr) == self.callbacks[self.current_animation]["frame"]:
#                     self.callbacks[self.current_animation]['callback']()
    
#     def animate(self):
#         if self.frame_counter >= (framerate / self.speed):
#             step = -1 if self.reverse else 1
#             setattr(self.spritesheet.frame, self.frame_attr, getattr(self.spritesheet.frame, self.frame_attr) + step)
#             if self.animation_finished(): 
#                 if self.loop:
#                     setattr(self.spritesheet.frame, self.frame_attr, self.starting_frame)
#                 else:
#                     setattr(self.spritesheet.frame, self.frame_attr, self.ending_frame)
#             self.frame_counter = 0
  
#     def play(self, animation):
#         if animation != self.current_animation:
#             self.current_animation = animation
#             self.animation = self.animation_dict[animation]
#             self.starting_frame = self.animation.start_frame
#             self.ending_frame = self.animation.end_frame
#             self.speed = self.animation.speed
#             self.reverse = self.animation.reverse
#             self.loop = self.animation.loop
#             self.vertical_anim = self.animation.vertical_anim
#             self.frame_attr = 'y' if self.vertical_anim else 'x'
            
            
#             if self.reverse:
#                 self.starting_frame = self.ending_frame
#             if self.vertical_anim:
#                 self.spritesheet.frame.y = self.starting_frame
#             else:
#                 self.spritesheet.frame.x = self.starting_frame
#             self.frame_counter = 0

#     def set_speed(self, new_speed):
#         self.speed = new_speed

#     def animation_finished(self):
#         if self.reverse:
#             return getattr(self.spritesheet.frame, self.frame_attr) <= self.ending_frame
#         return getattr(self.spritesheet.frame, self.frame_attr) >= self.ending_frame
        
#     def draw(self):
#         self.spritesheet.draw()
    
#     def run(self):
#         self.update()
#         self.draw()
