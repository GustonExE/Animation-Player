from pyray import *
from raylib import *
import math, os, sys, json

screen_width = 1280
screen_height = 720
framerate = 60

# Useful methods
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def lerp(start, end, t):
    return start + (end - start) * clamp(t, 0, 1)

def is_empty(obj):
    return isinstance(obj, (list, tuple, dict, set)) and len(obj) == 0

# Timer 
class Timer:
    def __init__(self, duration: int, repeat = False, autostart = False, func = None):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.repeat = repeat
        self.func = func
		
        if autostart:
            self.activate()

    def activate(self):
        self.active = True
        self.start_time = get_time()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        if self.active:
            if get_time() - self.start_time >= self.duration:
                if self.func and self.start_time: self.func()
                self.deactivate()

# Particle system       
class Particle:
    def __init__(self, pos: Vector2, velocity:Vector2, radius: int, color):
        self.pos = pos
        self.velocity = velocity
        self.radius = radius
        self.color = color 
        
        self.alive = True
        
    def update(self):        
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y
        self.velocity.y += 0.1
        self.radius -= 0.1
        
        if self.radius <= 0:
            self.alive = False
    
    def draw(self):
        draw_circle_v(self.pos, self.radius, self.color)
        
class ParticleSystem:
    def __init__(self, delay_duration: int):
        self.group = []
        self.delay = Timer(delay_duration, False, True, None)
        
        
    def update(self):
        self.delay.update()
        for particle in self.group[:]:
            particle.update()
            if particle.alive:
                particle.draw()
            else:
                self.group.remove(particle)
        
    def add(self, particle):
        if not self.delay.active:
            self.group.append(particle)
            self.delay.activate()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            