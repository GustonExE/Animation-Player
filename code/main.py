from settings import *
from spritesheet import *

init_window(screen_width, screen_height, 'Tilemap')
set_target_fps(framerate)


pos = Vector2(screen_width/2 - 40, screen_height/2 - 60)

with open("data/animations.json", "r") as f:
    animations = json.load(f)

animation = animations["animations"]

def print_falling():
    print("falling")

callbacks = {
    "falling": {
        "anim": "fall",
        "frame": animation["fall"]["end_frame"],
        "callback": print_falling
    }
}

default_animation = "idle"

gui_set_style(DEFAULT, TEXT_SIZE, 24)

spritesheet = Spritesheet("./assets/ivy.png", pos, 6, 17, 1, Vector2(0, 0))
animation_player = AnimationPlayer(spritesheet, 15, animation, default_animation, False, True, False, callbacks)
speed_value = 8
speed_pointer = ffi.new('float *', 8)
check_pointer = ffi.new('bool *', True)

def button_rect(x, y):
    return Rectangle(x, y, 160, 60)

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    
    idle_button = gui_button(button_rect(1100, 150 ), b"Idle")
    run_button = gui_button(button_rect(1100, 220 ), b"Run")
    jump_button = gui_button(button_rect(1100, 290 ), b"Jump")
    fall_button = gui_button(button_rect(1100, 360 ), b"Fall")
    
    
    bar_rect = Rectangle(get_screen_width() / 2 - 150, get_screen_height() - 100, 300, 40)
    check_rect = Rectangle(screen_width - 150, screen_height - 100, 50, 50)
    
    loop_checkbox = gui_check_box(check_rect, "Loop", check_pointer)
    gui_slider_bar(bar_rect, b"1", b"60", speed_pointer, 1, 60)
    
    speed_value = speed_pointer[0]
    
    animation_player.set_speed(speed_pointer[0])
    
    animation_player.loop = check_pointer[0]
    
    if idle_button:
        animation_player.play("idle")
    if run_button:
        animation_player.play("run")
    if jump_button:
        animation_player.play("jump")
    if fall_button:
        animation_player.play("fall")
    
    animation_player.loop = animation_player.animation_manager["loop"]
    animation_player.run()
    
    if is_key_pressed(KEY_ESCAPE):
        break
    draw_fps(10, 10)
    end_drawing()
    
close_window()