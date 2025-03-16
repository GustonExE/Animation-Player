from settings import *
from spritesheet import *

init_window(screen_width, screen_height, 'Animation Player')
set_target_fps(framerate)

pos = Vector2(screen_width / 2 - 60, screen_height / 2 - 80)

def print_falling():
    print('falling')

def print_idling():
    print("idling")

default_animation = "idle"

gui_set_style(DEFAULT, TEXT_SIZE, 24)

spritesheet = Spritesheet("./assets/ivy.png", pos, 8, 17, 1, Vector2(0, 0))

animations = {
    "idle": Animation(spritesheet, 0, 3, True, speed=10),
    "run": Animation(spritesheet, 4, 11, True, speed=12),
    "jump": Animation(spritesheet, 12, 14, False, speed=8),
    "fall": Animation(spritesheet, 15, 16, False, speed=6)
}
animation_player = AnimationPlayer(animations, default_animation)

current_animation = animation_player.current_animation
speed_pointer = ffi.new('float *', current_animation.speed)

def button_rect(x, y):
    return Rectangle(x, y, 160, 60)

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    
    current_animation = animation_player.current_animation
    
    
    if gui_button(button_rect(1100, 150), b"Idle"):
        animation_player.play("idle")
    if gui_button(button_rect(1100, 220), b"Run"):
        animation_player.play("run")
    if gui_button(button_rect(1100, 290), b"Jump"):
        animation_player.play("jump")
    if gui_button(button_rect(1100, 360), b"Fall"):
        animation_player.play("fall")

    bar_rect = Rectangle(get_screen_width() / 2 - 150, get_screen_height() - 100, 300, 40)
    gui_slider_bar(bar_rect, b"1", b"60", speed_pointer, 1, 60)
    
    speed_value = speed_pointer[0]
    
    current_animation.set_speed(speed_value)
    animation_player.run()
    
    if is_key_pressed(KEY_ESCAPE):
        break

    draw_fps(10, 10)
    end_drawing()

close_window()
