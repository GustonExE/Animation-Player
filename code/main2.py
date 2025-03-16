from settings import *
from spritesheet import *

init_window(screen_width, screen_height, "test")
set_target_fps(framerate)

pos = Vector2(0, 0)

spritesheet = Spritesheet("./assets/trainer_sheet_two.png", pos, Vector2(2, 2), 10, 1, Vector2(0,0))
spritesheet.pos = Vector2(screen_width/2 - spritesheet.rect.width/2, 
                          screen_height/2 - spritesheet.rect.height)
animations = {
    "girl": Animation(spritesheet, 0, 4, True),
    "boy": Animation(spritesheet, 5, 9, True)
}
animation_player = AnimationPlayer(animations, "girl")

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    
    
    draw_rectangle_rec(spritesheet.sprite_box, RED)
    animation_player.run()
    
    if is_key_pressed(KEY_L):
        animation_player.play("boy")
    if is_key_pressed(KEY_J):
        animation_player.play('girl')
    
    if is_key_pressed(KEY_ESCAPE):
        break
    end_drawing()
    
close_window()