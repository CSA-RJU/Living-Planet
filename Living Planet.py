##Copyright (C) 2019  Riley Underwood

## Practicum IT
## Started: 11/3/19
## v.0.7.5

## Last finished:
##  - Added a decent running animation
##  - Extended demo level and added a puzzle
##  - Changed the way levels are loaded

## To do:
##  - Fix minor bugs


##This program is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.

##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.

##You should have received a copy of the GNU General Public License
##along with this program.  If not, see <http://www.gnu.org/licenses/>.
##Also add information on how to contact you by electronic and paper mail.

##If the program does terminal interaction, make it output a short notice like this when it starts in an interactive mode:

##Living-Planet  Copyright (C) 2019  CSA-RJU
##This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
##This is free software, and you are welcome to redistribute it
##under certain conditions; type `show c' for details.
##The hypothetical commands show w' and show c' should show the appropriate parts of the General Public License. Of course, your program's commands might be different; for a GUI interface, you would use an "about box".

# [Python imports]
import pygame, random
from sys import exit
from vector2d import Vector2D

# region [Globals]
# Misc. globals:
global stage, level, carry_on, gameplay, paused, options, game_map, game_map_mg, map_size_x, map_size_y, player_temp_x, player_temp_y, title_screen
global stage_surface, stage_surface_mg, stage_start_adjust_x, player_start_adjust_x, stage_coords, player_coords, developer_mode, first_digit
# Controls:
global player_x, player_y, player_horizontal_acceleration_speed, player_horizontal_acceleration
global movement_horizontal_direction, stage_movement_x, player_vertical_acceleration, movement_vertical_direction
global player_vertical_acceleration_speed, stage_movement_y, land_adjust
# endregion

# region [Initialization]
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent()

pygame.mixer.pre_init(48000, 16, 20, 0)  # Frequency, size, channels, buffer size.

pygame.init()

# FPS
clock = pygame.time.Clock()
# endregion

# region [Screen stats]
SCREENWIDTH = 1280
SCREENHEIGHT = 720
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Living Planet")
# endregion

# region [Definitions]
# region Misc. definitions.
stage = "1"
level = "Demo"
stage_coords = [0, 0]
player_coords = [586, 0]
title_planet_frame = 10
player_frame = 0
brightness_change_wait = 0
brightness = 0
face = "right"
music_muted = False
god = False
developer_mode = False
# endregion

# region Horizontal stage movement
player_horizontal_acceleration_speed = 0
player_horizontal_acceleration = 0
movement_horizontal_direction = "none"
stage_movement_x = 0
max_speed_x = 10
stage_backdrop_movement_1 = [0 - 1280, 0]
stage_backdrop_movement_2 = [0, 0]
stage_backdrop_movement_3 = [0 + 1280, 0]
wall_to_right = False
wall_to_left = False
stage_start_adjust_x = 0
player_start_adjust_x = stage_start_adjust_x * -1
left_border_hit = False
# endregion

# region Vertical stage movement
player_vertical_acceleration_speed = 0
player_vertical_acceleration = 0
movement_vertical_direction = "none"
stage_movement_y = 0
max_speed_y = 15
touching_ground = False
touching_roof = False
hit_ground = 0
land_adjust = 0
# endregion

# region Transitions
global transition_start_black, transition_time, transition_speed, transition_start_type, transition_end_type, stage_card, stage_card_1, stage_card_2_1, stage_card_2_2, stage_card_2_3, stage_card_2_4, stage_card_2_5, stage_card_1_pos, stage_card_2_pos
transition_start_black = False
transition_load_black = False
transition_end_black = False
transition_start_type = "fast"
transition_end_type = "fast"
opacity = 0
transition_speed = 1  # How quickly the transition goes. (shade/frame)
transition_timer = 0
transition_time = 0  # How many frames the transition lasts for.
transition_time = 0
first_digit = 0
loading_frame = 0
stage_card = 0
stage_card_frame = 0

rotation_direction = 0.  # At 0, the object will not rotate.
# endregion
# endregion

# region [Surfaces]
transition_screen = pygame.Surface(screen.get_size())
transition_screen.fill((0, 0, 0))
transition_screen.set_alpha(opacity)

stage_surface = pygame.Surface(screen.get_size())
stage_surface.fill((255, 255, 254))
stage_surface.set_colorkey((255, 255, 254))

stage_surface_mg = pygame.Surface(screen.get_size())
stage_surface_mg.fill((255, 255, 254))
stage_surface_mg.set_colorkey((255, 255, 254))

# region [Images]
# region [Menus]
title_space = pygame.image.load('Images/Title Space.png').convert_alpha()
title_space = pygame.transform.scale(title_space, (1280, 720))

title_planet = pygame.image.load('Images/LP Outer View Dormant.png').convert_alpha()
title_planet = pygame.transform.scale(title_planet, (800, 800))
title_planet_pos = Vector2D(950, 250)
title_planet_rotation = -5.  # How rotated the image starts.
title_planet_rotation_speed = 30.  # Degrees per second.

title_text = pygame.image.load('Images/Title Text.png').convert_alpha()
title_text = pygame.transform.scale(title_text, (1280, 720))

title_text_highlight = pygame.image.load('Images/Title Text Highlight.png').convert_alpha()
title_text_highlight = pygame.transform.scale(title_text_highlight, (1280, 720))

paused_text = pygame.image.load('Images/Paused Text.png').convert_alpha()
paused_text = pygame.transform.scale(paused_text, (1280, 720))

options_text = pygame.image.load('Images/Options Text.png').convert_alpha()
options_text = pygame.transform.scale(options_text, (1280, 720))
options_music_on = pygame.image.load('Images/Options (Music on).png').convert_alpha()
options_music_on = pygame.transform.scale(options_music_on, (1280, 720))
options_music_off = pygame.image.load('Images/Options (Music off).png').convert_alpha()
options_music_off = pygame.transform.scale(options_music_off, (1280, 720))
# endregion

## region [Player]
player_idle = {"right": list(), "left": list()}
for i in range(1, 6):
    animation_image = pygame.image.load(f'Images/Player Idle ({i}).png').convert_alpha()
    animation_image = pygame.transform.scale(animation_image, (100, 100))
    player_idle["right"].append(animation_image)
    player_idle["left"].append(pygame.transform.flip(animation_image, True, False))
    
player_run = {"right": list(), "left": list()}
for i in range(0, 6):
    animation_image = pygame.image.load(f'Images/Player Run ({i}).png').convert_alpha()
    animation_image = pygame.transform.scale(animation_image, (100, 100))
    player_run["right"].append(animation_image)
    player_run["left"].append(pygame.transform.flip(animation_image, True, False))
    
player_jump = {"right": list(), "left": list()}
for i in range(1, 4):
    animation_image = pygame.image.load(f'Images/Player Jump ({i}).png').convert_alpha()
    animation_image = pygame.transform.scale(animation_image, (100, 100))
    player_jump["right"].append(animation_image)
    player_jump["left"].append(pygame.transform.flip(animation_image, True, False))
# endregion

## region [Levels]
darkness = pygame.image.load('Images/Darkness.png').convert_alpha()
darkness = pygame.transform.scale(darkness, (2560, 1440))

stage_1_background = pygame.image.load('Images/Stage 1 Background.png').convert_alpha()
stage_1_background = pygame.transform.scale(stage_1_background, (1280, 720))
stage_1_backdrop = pygame.image.load('Images/Stage 1 Backdrop.png').convert_alpha()
stage_1_backdrop = pygame.transform.scale(stage_1_backdrop, (1280, 720))
torch_light = pygame.image.load('Images/Torch Light.png').convert_alpha()
torch_light = pygame.transform.scale(torch_light, (150, 150))

stage_2_background = pygame.image.load('Images/Stage 2 Background.png').convert_alpha()
stage_2_background = pygame.transform.scale(stage_2_background, (1280, 720))
# endregion

# region [Loading screen]
loading_screen = pygame.image.load('Images/Loading Screen.png').convert_alpha()
loading_screen = pygame.transform.scale(loading_screen, (1280, 720))

loading_frame_1 = pygame.image.load('Images/Loading Frame (1).png').convert_alpha()
loading_frame_1 = pygame.transform.scale(loading_frame_1, (90, 90))
loading_frame_2 = pygame.image.load('Images/Loading Frame (2).png').convert_alpha()
loading_frame_2 = pygame.transform.scale(loading_frame_2, (90, 90))
loading_frame_3 = pygame.image.load('Images/Loading Frame (3).png').convert_alpha()
loading_frame_3 = pygame.transform.scale(loading_frame_3, (90, 90))
loading_frame_4 = pygame.image.load('Images/Loading Frame (4).png').convert_alpha()
loading_frame_4 = pygame.transform.scale(loading_frame_4, (90, 90))
loading_frame_5 = pygame.image.load('Images/Loading Frame (5).png').convert_alpha()
loading_frame_5 = pygame.transform.scale(loading_frame_5, (90, 90))
# endregion
# endregion

# region [Music]
title_song = pygame.mixer.music.load('Audio/Pure Numbness.wav')
# endregion

# region FUNCTIONS

def Load_Game_Data():
    global stage, level, music_muted, developer_mode
    game_data_load = open('Game Data.txt', "r")
    line = game_data_load.readline()  # Reads the first line once to get it started.
    linesplit = line.split(":")
    for a in linesplit:
        a = a.strip(" \n")
        stage = (f'Stage {a}')
    line = game_data_load.readline()  # Assures that the program checks more than one line.
    linesplit = line.split(":")
    for b in linesplit:
        b = b.strip(" \n")
        level = (f'Level {b}')
    line = game_data_load.readline()  # Assures that the program checks more than one line.
    linesplit = line.split(":")
    for c in linesplit:
        c = c.strip(" \n")
        if c == "False":
            c = False
        else:
            c = True
        music_muted = c
    line = game_data_load.readline()  # Assures that the program checks more than one line.
    linesplit = line.split(":")
    for d in linesplit:
        d = d.strip(" \n")
        if d == "False":
            d = False
        else:
            d = True
        developer_mode = d
    game_data_load.close()
Load_Game_Data()

def Save_Game_Data():
    global stage, level, music_muted, developer_mode
    game_data_save = open('Game Data.txt', "w")
    stagesplit = stage.split(" ")
    for a in stagesplit:
        a = a
    game_data_save.write(f'Stage: {a}\n')
    levelsplit = level.split(" ")
    for b in levelsplit:
        b = b
    game_data_save.write(f'Level: {b}\n')
    game_data_save.write(f'music_muted: {music_muted}\n')
    game_data_save.write(f'developer_mode: {developer_mode}\n')
    game_data_save.close()

def Title_Screen():
    global every_on, carry_on, title_screen, stage, gameplay, paused, options
    every_on = True
    gameplay = False
    paused = False
    options = False

    Titlesong = pygame.mixer.music.load('Audio/Pure Numbness.wav')
    if not music_muted:
        if title_screen is True:
            pygame.mixer.music.play(-1)

    title_screen = True


def New_Game():
    global stage, level, gameplay
    stage = "Stage 1"
    level = "Level Test"
    gameplay = True

    # Stuff for doing a transition:
    global transition_start_black, transition_time, transition_speed, carry_on, transition_start_type, transition_end_type, title_screen
    carry_on = False
    opacity = 0
    loading_frame = 1
    transition_start_black = True
    transition_start_type = "fast"
    transition_end_type = "slow"
    transition_speed = 1  # How quickly the transition goes. (shade/frame)
    transition_time = 100  # How many frames the transition lasts for.

    title_screen = False


def Load_Game():
    global stage, level, gameplay
    gameplay = True

    # Stuff for doing a transition:
    global transition_start_black, transition_time, transition_speed, carry_on, transition_start_type, transition_end_type, title_screen
    carry_on = False
    opacity = 0
    loading_frame = 1
    transition_start_black = True
    transition_start_type = "fast"
    transition_end_type = "slow"
    transition_speed = 1  # How quickly the transition goes. (shade/frame)
    transition_time = 100  # How many frames the transition lasts for.

    title_screen = False


def Load_Map(level):
    global game_map, game_map_mg, map_size_x, map_size_y, player_temp_x, player_temp_y
    game_map = []
    game_map_mg = []
    if level != "none":
        # Middle ground
        map_load = open(f'Maps/{stage} {level} MG.LPM', "r")
        line = map_load.readline()  # Reads the first line once to get it started.
        linesplit = line.split(",")
        line = map_load.readline()
        while line:  # Assures the program runs through the whole file.
            linesplit = line.split("'")
            column = []
            for f in linesplit:
                f = f.strip(" \n")
                column.append(f)
            game_map_mg.append(column)
            line = map_load.readline()  # Assures that the program checks more than one line.
        map_load.close()

        # Stage with hit boxes
        map_load = open(f'Maps/{stage} {level}.LPM', "r")
        line = map_load.readline()  # Reads the first line once to get it started.
        linesplit = line.split(",")
        map_size_x = int(linesplit[0])
        map_size_y = int(linesplit[1])
        player_temp_x = int(linesplit[2])
        player_temp_y = int(linesplit[3])
        line = map_load.readline()
        while line:  # Assures the program runs through the whole file.
            linesplit = line.split("'")
            column = []
            for f in linesplit:
                f = f.strip(" \n")
                column.append(f)
            game_map.append(column)
            line = map_load.readline()  # Assures that the program checks more than one line.
        map_load.close()


def Load_Stage():
    # Grabbing the player
    global map_size_x, map_size_y, player_x, player_y, stage_movement_x, stage_movement_y, stage_surface, stage_surface_mg, stage_start_adjust_x, player_start_adjust_x, stage_coords

    player_x = int((player_temp_x - 1) * 50)
    player_y = int((player_temp_y - 1) * 50)
    stage_movement_x = 0
    stage_movement_y = 0
    stage_coords = [0, 0]

    if 0 >= (0 - float(player_x) + 590):  # Adjusts the stage to start off by hugging the screen border if the stage is too big.
        stage_start_adjust_x = (0 - float(player_x) + 590) * -1
        player_start_adjust_x = stage_start_adjust_x * -1

    stage_surface = pygame.Surface(((map_size_x * 50), (map_size_y * 50)))
    stage_surface.fill((255, 255, 254))
    stage_surface.set_colorkey((255, 255, 254))

    stage_surface_mg = pygame.Surface(((map_size_x * 50), (map_size_y * 50)))
    stage_surface_mg.fill((255, 255, 254))
    stage_surface_mg.set_colorkey((255, 255, 254))

    # Grabbing the blocks
    global game_map, game_map_mg, stage
    block_0 = pygame.image.load('Images/Blocks/Block 0.png').convert_alpha()
    block_0 = pygame.transform.scale(block_0, (50, 50))
    block_c = pygame.image.load('Images/Blocks/Block Chest.png').convert_alpha()
    block_c = pygame.transform.scale(block_c, (50, 50))
    block_cap_c = pygame.image.load('Images/Blocks/Block Chest 0.png').convert_alpha()
    block_cap_c = pygame.transform.scale(block_cap_c, (50, 50))
    if stage == "Stage 1":  # Loads in the blocks in stage 1.
        block_l = pygame.image.load('Images/Blocks/Block Torch.png').convert_alpha()
        block_cap_l = pygame.image.load('Images/Blocks/Block Torch 0.png').convert_alpha()
        block_2 = pygame.image.load('Images/Blocks/Stage 1/Block 2.png').convert_alpha()
        block_3 = pygame.image.load('Images/Blocks/Stage 1/Block 3.png').convert_alpha()
        block_cap_3 = pygame.image.load('Images/Blocks/Stage 1/Block #.png').convert_alpha()
        block_5 = pygame.image.load('Images/Blocks/Stage 1/Block 5.png').convert_alpha()
        block_cap_5 = pygame.image.load('Images/Blocks/Stage 1/Block %.png').convert_alpha()
        block_7 = pygame.image.load('Images/Blocks/Stage 1/Block 7.png').convert_alpha()
    elif stage == "Stage 2":
        block_l = pygame.image.load('Images/Blocks/Block Torch.png').convert_alpha()
        block_cap_l = pygame.image.load('Images/Blocks/Block Torch 0.png').convert_alpha()
        block_2 = pygame.image.load('Images/Blocks/Stage 2/Block 02.png').convert_alpha()
        block_3 = pygame.image.load('Images/Blocks/Stage 2/Block 03.png').convert_alpha()
        block_cap_3 = pygame.image.load('Images/Blocks/Block Missing.png').convert_alpha()
        block_5 = pygame.image.load('Images/Blocks/Stage 2/Block 05.png').convert_alpha()
        block_cap_5 = block_cap_3
        block_7 = pygame.image.load('Images/Blocks/Stage 2/Block 07.png').convert_alpha()

    block_l = pygame.transform.scale(block_l, (50, 50))
    block_cap_l = pygame.transform.scale(block_cap_l, (50, 50))
    block_2 = pygame.transform.scale(block_2, (50, 50))
    block_3 = pygame.transform.scale(block_3, (50, 50))
    block_cap_3 = pygame.transform.scale(block_cap_3, (50, 50))
    block_4 = pygame.transform.flip(block_3, True, False)
    block_cap_4 = pygame.transform.flip(block_cap_3, True, False)
    block_5 = pygame.transform.scale(block_5, (50, 50))
    block_cap_5 = pygame.transform.scale(block_cap_5, (50, 50))
    block_6 = pygame.transform.flip(block_5, True, False)
    block_cap_6 = pygame.transform.flip(block_cap_5, True, False)
    block_7 = pygame.transform.scale(block_7, (50, 50))
    block_8 = pygame.transform.flip(block_7, True, False)
    block_w = pygame.transform.flip(block_2, False, True)
    block_e = pygame.transform.flip(block_3, False, True)
    block_cap_e = pygame.transform.flip(block_cap_3, False, True)
    block_r = pygame.transform.flip(block_4, False, True)
    block_cap_r = pygame.transform.flip(block_cap_4, False, True)
    block_t = pygame.transform.flip(block_5, False, True)
    block_cap_t = pygame.transform.flip(block_cap_5, False, True)
    block_y = pygame.transform.flip(block_6, False, True)
    block_cap_y = pygame.transform.flip(block_cap_6, False, True)

    block_pos = lambda x, y: (int((((x * 50) - float(player_x) + 590) + stage_start_adjust_x)),
                              int(((y * 50) - float(player_y)) + 310))

    block_type_list = ['[0]', '[c]', '[C]', '[l]', '[L]', '[2]', '[3]', '[#]', '[4]', '[$]', '[5]', '[%]', '[6]', '[^]', '[7]', '[8]', '[w]', '[e]', '[E]', '[r]', '[R]', '[t]', '[T]', '[y]', '[Y]']
    if stage == "Stage 1" or stage == "Stage 2":
        block_id_list = [block_0, block_c, block_cap_c, block_l, block_cap_l, block_2, block_3, block_cap_3, block_4, block_cap_4, block_5, block_cap_5, block_6, block_cap_6, block_7, block_8, block_w, block_e, block_cap_e, block_r, block_cap_r, block_t, block_cap_t, block_y, block_cap_y]
        
    if level != "none":
        for y in range(map_size_y):  # Runs through the map list separating every line in the y axis.
            for x in range(map_size_x):  # Runs through the map list separating every item in the x axis in every separation line of the y axis.
                if stage == "Stage 1" or stage == "Stage 2":  # Renders every block in the level and blits it to the stage surface.
                    for i in range(0, 25):
                        if game_map[y][x] == block_type_list[i]:  # v-- Detects what block goes in which place and blits them. --v
                            stage_surface.blit(block_id_list[i], block_pos(x, y))
                        if game_map_mg[y][x] == block_type_list[i]:  # v-- Detects what block goes in which place and blits them. --v
                            stage_surface_mg.blit(block_id_list[i], block_pos(x, y))

def Stage_Card():
    global stage_card, stage, gameplay, stage_card_1, stage_card_2_1, stage_card_2_2, stage_card_2_3, stage_card_2_4, stage_card_2_5, stage_card_1_pos, stage_card_2_pos
    if gameplay == True:
        if stage == "Stage 1":
            stage_card_1 = pygame.image.load('Images/Stage Card Home Planet (1).png').convert_alpha()
            stage_card_1 = pygame.transform.scale(stage_card_1, (960, 480))
            stage_card_2_1 = pygame.image.load('Images/Stage Card Home Planet (2) (1).png').convert_alpha()
            stage_card_2_2 = pygame.image.load('Images/Stage Card Home Planet (2) (2).png').convert_alpha()
            stage_card_2_3 = pygame.image.load('Images/Stage Card Home Planet (2) (3).png').convert_alpha()
            stage_card_2_4 = pygame.image.load('Images/Stage Card Home Planet (2) (4).png').convert_alpha()
            stage_card_2_5 = pygame.image.load('Images/Stage Card Home Planet (2) (5).png').convert_alpha()

        if stage == "Stage 1":
            stage_card_2_1 = pygame.transform.scale(stage_card_2_1, (960, 480))
            stage_card_2_2 = pygame.transform.scale(stage_card_2_2, (960, 480))
            stage_card_2_3 = pygame.transform.scale(stage_card_2_3, (960, 480))
            stage_card_2_4 = pygame.transform.scale(stage_card_2_4, (960, 480))
            stage_card_2_5 = pygame.transform.scale(stage_card_2_5, (960, 480))

            stage_card_1_pos = [1280, 120]
            stage_card_2_pos = [-960, 120]

            stage_card = True

def Animation(frame):
    global first_digit
    # Shows the first digit of the variable responsible for counting frames
    stopper = 0
    for i in str(frame):
        stopper += 1  # Stops in what ever place the # indicates.
        if stopper == 1:
            first_digit = int(i)

def Pause():  # Pauses the game.
    global paused
    paused = True

def Unpause():  # Unpauses the game.
    global paused
    paused = False

def Options():  # Unpauses the game.
    global options
    options = True

def Unoptions():  # Unpauses the game.
    global options
    options = False
# endregion

# region RUNNING THE GAME
every_on = True
carry_on = True
title_screen = True
gameplay = False
paused = False
options = False
pygame.mixer.music.stop()
Title_Screen()

transition_screen = pygame.Surface(screen.get_size())
while every_on:  # Anything that updates ever.
    # print(clock)  # Prints the frame rate.

    mousexy = pygame.mouse.get_pos()
    # print(mousexy)

    # To pause/quit the game
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            # When "P" is pressed
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                if paused is False:
                    Pause()
                elif paused is True:
                    Unpause()
                    if options is True:
                        Unoptions()
            if event.key == pygame.K_a or event.key == pygame.K_d and carry_on is True and gameplay is True:
                player_run_frame = 68
            if event.key == pygame.K_g and developer_mode:
                if god:
                    god = False
                elif not god:
                    god = True
                
        if event.type == pygame.QUIT:
            Save_Game_Data()
            every_on = False
        # region [Buttons]
        # Moving the mouse:
        if event.type == pygame.MOUSEMOTION:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if carry_on:
                # Title screen buttons:
                if title_screen is True and transition_end_black is False and options is False:  # Only on title screen and after a transition has finished can this happen.
                    # New Game button
                    if 408 <= mousexy[0] <= 875 and 304 <= mousexy[1] <= 384:
                        New_Game()
                    # Load Game button
                    if 408 <= mousexy[0] <= 875 and 408 <= mousexy[1] <= 488:
                        Load_Game()
                    # Options button
                    if 408 <= mousexy[0] <= 875 and 508 <= mousexy[1] <= 588:
                        Options()
                    # Leave button
                    if 408 <= mousexy[0] <= 875 and 612 <= mousexy[1] <= 692:
                        Save_Game_Data()
                        carry_on = False
                        every_on = False
                    # Extras button
                    if 408 <= mousexy[0] <= 875 and 719 <= mousexy[1] <= 799:
                        if not developer_mode:
                            developer_mode = True
                            print("Developer mode activated.")
                        elif developer_mode:
                            developer_mode = False
                            print("Developer mode disabled.")
                            
                # Pause buttons:
                elif paused and transition_end_black is False and options is False:  # When paused and after a transition has finished can this happen.
                    # Resume button
                    if 408 <= mousexy[0] <= 875 and 304 <= mousexy[1] <= 384:
                        Unpause()
                    # Main Menu button
                    if 408 <= mousexy[0] <= 875 and 408 <= mousexy[1] <= 488:
                        # Stuff for doing a transition:
                        carry_on = False
                        level = "none"
                        opacity = 0
                        loading_frame = 1
                        transition_start_black = True
                        transition_start_type = "fast"
                        transition_end_type = "fast"
                        transition_speed = 1  # How quickly the transition goes. (shade/frame)
                        transition_time = 100  # How many frames the transition lasts for.
                        Title_Screen()
                    # Options button
                    if 408 <= mousexy[0] <= 875 and 508 <= mousexy[1] <= 588:
                        Options()
                    # Leave button
                    if 408 <= mousexy[0] <= 875 and 612 <= mousexy[1] <= 692:
                        Save_Game_Data()
                        carry_on = False
                        every_on = False
                    # Extras button
                    if 408 <= mousexy[0] <= 875 and 719 <= mousexy[1] <= 799:
                        if not developer_mode:
                            developer_mode = True
                            print("Developer mode activated.")
                        elif developer_mode:
                            developer_mode = False
                            print("Developer mode disabled.")

                # Options buttons:
                elif paused or title_screen is True and transition_end_black is False and options is True:  # When paused and after a transition has finished can this happen.
                    # Return button
                    if 408 <= mousexy[0] <= 875 and 304 <= mousexy[1] <= 384:
                        Unoptions()
                    # Resume
                    if 408 <= mousexy[0] <= 875 and 408 <= mousexy[1] <= 488:
                        print("Nothing yet")
                    # Music Mute button
                    if 408 <= mousexy[0] <= 875 and 508 <= mousexy[1] <= 588:
                        if music_muted:
                            music_muted = False
                            pygame.mixer.music.play(-1)
                        elif not music_muted:
                            music_muted = True
                            pygame.mixer.music.stop()
                    # Leave button
                    if 408 <= mousexy[0] <= 875 and 612 <= mousexy[1] <= 692:
                        Save_Game_Data()
                        carry_on = False
                        every_on = False
        # endregion

    light_pos = list()
    in_darkness = False
    if carry_on:  # When not paused.

        # region [Title screen]
        if title_screen is True:

            # region [Planet stuff]
            rotated_title_planet = pygame.transform.rotate(title_planet, title_planet_rotation)  # Return the rotated_title_planet surface object
            # w, h = rotated_title_planet.get_size()
            title_planet_draw_pos = Vector2D(title_planet_pos.x - 800 / 2, title_planet_pos.y - 800 / 2)

            time_passed = clock.tick()
            time_passed_seconds = time_passed / 1000.0

            title_planet_rotation += rotation_direction * title_planet_rotation_speed * time_passed_seconds

            # Blitting images.
            screen.blit(title_space, (0, 0))
            screen.blit(rotated_title_planet, [int(axis) for axis in title_planet_draw_pos])
            if options is False:
                screen.blit(title_text, (0, 0))

            # Rotating planet on title screen.
            if title_planet_frame >= 1:
                title_planet_frame -= 1
            else:
                title_planet_frame = 160
                if rotation_direction == 0 or rotation_direction == .01:
                    rotation_direction = -.01
                else:
                    rotation_direction = .01
            # endregion
            
        else:
            if gameplay is False:
                screen.blit(title_space, (0, 0))
        # endregion
        
        # region [Controls]
        if title_screen is False and not paused and transition_end_black is False:  # When Playing the game.
            
            # region [Left]
            if key[pygame.K_a] or key[pygame.K_LEFT]:
                if not wall_to_left:
                    face = "left"
                    if movement_horizontal_direction != "left":
                        movement_horizontal_direction = "left"
                        player_horizontal_acceleration = 0
                        player_horizontal_acceleration_speed = 0
                    if player_horizontal_acceleration > -max_speed_x and movement_horizontal_direction == "left":  # Left.
                        player_horizontal_acceleration_speed += -.08
                        player_horizontal_acceleration += (-.16 + player_horizontal_acceleration_speed)
                        if player_horizontal_acceleration < -max_speed_x:  # Max speed.
                            player_horizontal_acceleration = -max_speed_x
                            player_horizontal_acceleration_speed = 0
                elif player_horizontal_acceleration < 0 and movement_horizontal_direction != "right":  # Idle after moving left.
                    player_horizontal_acceleration_speed += .08
                    player_horizontal_acceleration += (.16 + player_horizontal_acceleration_speed)
                    if player_horizontal_acceleration > 0:  # When idle, the acceleration will round to 0 if it is close enough.
                        player_horizontal_acceleration = 0
                        player_horizontal_acceleration_speed = 0
                if wall_to_left:
                    player_horizontal_acceleration = 0
                    player_horizontal_acceleration_speed = 0
            # endregion
            
            # region [Right]
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                if not wall_to_right:
                    face = "right"
                    if movement_horizontal_direction != "right":
                        movement_horizontal_direction = "right"
                        player_horizontal_acceleration = 0
                        player_horizontal_acceleration_speed = 0
                    if player_horizontal_acceleration < max_speed_x and movement_horizontal_direction == "right":  # Right.
                        player_horizontal_acceleration_speed += .08
                        player_horizontal_acceleration += (.16 + player_horizontal_acceleration_speed)
                        if player_horizontal_acceleration > max_speed_x:  # Max speed.
                            player_horizontal_acceleration = max_speed_x
                            player_horizontal_acceleration_speed = 0
                elif player_horizontal_acceleration > 0 and movement_horizontal_direction != "left":  # Idle after moving right.
                    player_horizontal_acceleration_speed += -.08
                    player_horizontal_acceleration += (-.16 + player_horizontal_acceleration_speed)
                    if player_horizontal_acceleration < 0:  # When idle, the acceleration will round to 0 if it is close enough.
                        player_horizontal_acceleration = 0
                        player_horizontal_acceleration_speed = 0

                if wall_to_right:
                    player_horizontal_acceleration = 0
                    player_horizontal_acceleration_speed = 0
            # endregion
            
            if not key[pygame.K_a] and not key[pygame.K_d] and not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:  # Not pressing "a" or "d".
                movement_horizontal_direction = "none"
                
            if not god:
                # region [Up (Jumping)]
                if key[pygame.K_w] and touching_ground or key[pygame.K_UP] and touching_ground or key[pygame.K_SPACE] and touching_ground:
                    hit_ground = 1 #Only happens for one frame. (Used to set landing animation)
                    if player_vertical_acceleration == 0:
                        player_vertical_acceleration = max_speed_y  # This # controls the speed of the jump. (Starting higher and decreasing)
                    touching_ground = False

                if not touching_ground:
                    if key[pygame.K_w] or key[pygame.K_UP] and not touching_roof or key[pygame.K_SPACE] and not touching_roof:
                        if player_vertical_acceleration > 0:
                            player_vertical_acceleration -= .5  # This # controls how high the player jumps. (The lower the number the higher the jump)
                        elif player_vertical_acceleration > -max_speed_y:  # This # controls the speed of the jump. (Starting higher and decreasing)
                            player_vertical_acceleration -= 1
                        elif player_vertical_acceleration > 0:
                            player_vertical_acceleration = 0
                    else:
                        if player_vertical_acceleration > 0:
                            player_vertical_acceleration -= 1  # This # controls how high the player jumps. (The lower the number the higher the jump)
                        elif player_vertical_acceleration > -max_speed_y:  # This # controls the speed of the jump. (Starting higher and decreasing)
                            player_vertical_acceleration -= 1
                        elif player_vertical_acceleration > 0:
                            player_vertical_acceleration = 0

                if touching_ground:
                    player_vertical_acceleration = 0
                # endregion
                
            if god:
                # region [Down]
                if key[pygame.K_s] or key[pygame.K_DOWN]:
                    if movement_vertical_direction != "down":
                        movement_vertical_direction = "down"
                        player_vertical_acceleration = 0
                        player_vertical_acceleration_speed = 0
                    if player_vertical_acceleration > -max_speed_x and movement_vertical_direction == "down":  # Left.
                        player_vertical_acceleration_speed += -.8
                        player_vertical_acceleration += (-.16 + player_vertical_acceleration_speed)
                        if player_vertical_acceleration < -max_speed_x:
                            player_vertical_acceleration = -max_speed_x
                            player_vertical_acceleration_speed = 0
                elif player_vertical_acceleration < 0 and movement_vertical_direction != "up":  # Idle after moving left.
                    player_vertical_acceleration_speed += .08
                    player_vertical_acceleration += (.16 + player_vertical_acceleration_speed)
                    if player_vertical_acceleration > 0:  # When idle, the acceleration will round to 0 if it is close enough.
                        player_vertical_acceleration = 0
                        player_vertical_acceleration_speed = 0
                elif not key[pygame.K_w] and not key[pygame.K_SPACE] and not key[pygame.K_s]:  # Not pressing "w" or "s".
                    movement_vertical_direction = "none"
                # endregion

                # region [Up]
                if key[pygame.K_w] or key[pygame.K_UP] or key[pygame.K_SPACE]:
                    if movement_vertical_direction != "up":
                        movement_vertical_direction = "up"
                        hit_ground = 1
                        player_vertical_acceleration = 0
                        player_vertical_acceleration_speed = 0
                    if player_vertical_acceleration < max_speed_x and movement_vertical_direction == "up":  # Right.
                        player_vertical_acceleration_speed += .08
                        player_vertical_acceleration += (.16 + player_vertical_acceleration_speed)
                        if player_vertical_acceleration > max_speed_x:
                            player_vertical_acceleration = max_speed_x
                            player_vertical_acceleration_speed = 0
                elif player_vertical_acceleration > 0 and movement_vertical_direction != "down":  # Idle after moving right.
                    player_vertical_acceleration_speed += -.08
                    player_vertical_acceleration += (-.16 + player_vertical_acceleration_speed)
                    if player_vertical_acceleration < 0:  # When idle, the acceleration will round to 0 if it is close enough.
                        player_vertical_acceleration = 0
                        player_vertical_acceleration_speed = 0

                elif not key[pygame.K_w] and not key[pygame.K_UP] and not key[pygame.K_SPACE] and not key[pygame.K_s] and not key[pygame.K_DOWN]:  # Not pressing "w" or "s".
                    movement_vertical_direction = "none"
                # endregion
        # endregion
        
        # region Stages
        if gameplay is True:
            if not paused:
                if stage_coords[0] <= 0 and movement_horizontal_direction == "left":
                    stage_movement_x += int(player_horizontal_acceleration)
                elif movement_horizontal_direction == "right":
                    stage_movement_x += int(player_horizontal_acceleration)
                stage_movement_y += int(player_vertical_acceleration)

                touching_ground = False  # Resets the block sensor (if the player is touching the block).
                touching_roof = False
                wall_to_right = False
                wall_to_left = False

                # region [Border Collision]
                # Left and Right
                if  570 <= (((-1 * 50) - float(player_x)) + 590) - stage_movement_x <= 660:
                    stage_movement_x = (round(stage_movement_x / 50) * 50) + 21
                    wall_to_left = True
                if  570 <= (((map_size_x * 50) - float(player_x)) + 590) - stage_movement_x <= 660:
                    stage_movement_x = (round(stage_movement_x / 50) * 50) - 21
                    wall_to_right = True

                # Up and down
    ##            if  360 <= (((-1 * 50) - float(player_y)) + 310) + stage_movement_y <= 410:
    ##                stage_movement_y = (round(stage_movement_y / 50) * 50)
    ##                touching_roof = True
                if  360 <= (((map_size_y * 50) - float(player_y)) + 310) + stage_movement_y <= 410:
                    stage_movement_y = (round(stage_movement_y / 50) * 50)
                    touching_ground = True

            block_pos = lambda x, y: (int((((x * 50) - float(player_x) + 590) + stage_start_adjust_x)),
                              int(((y * 50) - float(player_y)) + 310))
                
            for y in range(map_size_y):  # Runs through the map list separating every line in the y axis.
                for x in range(map_size_x):  # Runs through the map list separating every item in the x axis in every separation line of the y axis.
                    if stage == "Stage 1" or stage == "Stage 2":

                        # region [Light Source]
                        if game_map[y][x] == '[l]' or game_map[y][x] == '[L]':  # v-- Detects what block goes in which place and blits them. --v
                            light_pos.append(block_pos(x - 1, y - 1))
                            # stage_surface.blit(light_surface, block_pos(x - 1, y - 1))
                        # endregion

                        if not paused:
                            # region [Ground Collision]
        # The player's border ---v            v-- The selected block's current position --v
                            if (360 <= (((y * 50) - float(player_y)) + 310) + stage_movement_y <= 410) and (  # If touching the block at all:
                                    570 <= (((x * 50) - float(player_x)) + 590) - stage_movement_x <= 660):
                                if game_map[y][x] == '[2]' or game_map[y][x] == '[3]' or game_map[y][x] == '[4]' or game_map[y][x] == '[#]' or game_map[y][x] == '[$]':  # Defines the hit box for ground blocks.
                                    if player_vertical_acceleration <= 0:  # If moving down or not at all:
                                        stage_movement_y = (round(stage_movement_y / 50) * 50)
                                        touching_ground = True
                                        if hit_ground == 1:  # The immediate frame when the player lands from falling.
                                            hit_ground = 0
                                            player_frame = 49
                                    if game_map[y][x] == '[3]' or game_map[y][x] == '[4]' or game_map[y][x] == '[#]' or game_map[y][x] == '[$]':  # Defines the hit box for corner ground blocks.
                                        if (((y * 50) - float(player_y)) + 310) + stage_movement_y <= 409:
                                            if game_map[y][x] == '[3]' or game_map[y][x] == '[#]':
                                                stage_movement_x = (round(stage_movement_x / 50) * 50) - 21
                                                touching_ground = False
                                                wall_to_right = True
                                            if game_map[y][x] == '[4]' or game_map[y][x] == '[$]':
                                                stage_movement_x = (round(stage_movement_x / 50) * 50) + 21
                                                touching_ground = False
                                                wall_to_left = True
                            # endregion


                        if (310 <= (((y * 50) - float(player_y)) + 310) + stage_movement_y <= 410) and (  # If touching the block at all (about head area):
                                590 <= (((x * 50) - float(player_x)) + 590) - stage_movement_x <= 640):
                            if game_map[y][x] == '[0]' or game_map[y][x] == '[C]' or game_map[y][x] == '[L]':
                                in_darkness = True

                        if not paused:
                            # region [Walls]
                            if (310 <= (((y * 50) - float(player_y)) + 310) + stage_movement_y <= 410) and (  # If touching the block at all:
                                    570 <= (((x * 50) - float(player_x)) + 590) - stage_movement_x <= 660):
                                if game_map[y][x] == '[7]' or game_map[y][x] == '[%]' or game_map[y][x] == '[T]':  # Defines the hit box for left walls.
                                    stage_movement_x = (round(stage_movement_x / 50) * 50) - 21
                                    wall_to_right = True
                                elif game_map[y][x] == '[8]' or game_map[y][x] == '[^]' or game_map[y][x] == '[Y]':  # Defines the hit box for right walls.
                                    stage_movement_x = (round(stage_movement_x / 50) * 50) + 21
                                    wall_to_left = True
                            # endregion

                            # region [Roof Collision]
        # The player's border ---v            v-- The selected block's current position --v
                            if (280 <= (((y * 50) - float(player_y)) + 310) + stage_movement_y <= 410) and (  # If touching the block at all:
                                    570 <= (((x * 50) - float(player_x)) + 590) - stage_movement_x <= 660):
                                if game_map[y][x] == '[w]' or game_map[y][x] == '[e]' or game_map[y][x] == '[r]':  # Defines the hit box for left walls.
                                    stage_movement_y = (round((stage_movement_y / 50) * 50) - player_vertical_acceleration)
                                    touching_roof = True
                                    if game_map[y][x] == '[e]' or game_map[y][x] == '[r]' or game_map[y][x] == '[E]' or game_map[y][x] == '[R]':  # Defines the hit box for corner ground blocks.
                                        if (((y * 50) - float(player_y)) + 410) + stage_movement_y >= 309:
                                            if game_map[y][x] == '[e]' or game_map[y][x] == '[E]':
                                                if (((x * 50) - float(player_x)) + 590) - stage_movement_x >= 650:
                                                    stage_movement_x = (round(stage_movement_x / 50) * 50) - 21
                                                    touching_roof = False
                                                    wall_to_right = True
                                            if game_map[y][x] == '[r]' or game_map[y][x] == '[R]':
                                                if (((x * 50) - float(player_x)) + 590) - stage_movement_x <= 580:
                                                    stage_movement_x = (round(stage_movement_x / 50) * 50) + 21
                                                    touching_roof = False
                                                    wall_to_left = True
                            # endregion
                    
                if touching_ground or touching_roof:
                    player_vertical_acceleration = 0
                    if not touching_ground:
                        player_vertical_acceleration_speed = 0

                # region [Backdrop movement]
                if left_border_hit is False:
                    stage_backdrop_movement_1[0] = (0 - 1280 - (stage_movement_x / 16))
                stage_backdrop_movement_1[1] = (0 + (stage_movement_y / 32))
                if left_border_hit is False:
                    stage_backdrop_movement_2[0] = (0 - (stage_movement_x / 16))
                stage_backdrop_movement_2[1] = (0 + (stage_movement_y / 32))

                # Loops the backdrop so that it feels infinite:
                if stage_backdrop_movement_1[0] < -1280:
                    stage_backdrop_movement_1[0] += 2560
                elif stage_backdrop_movement_1[0] > 1280:
                    stage_backdrop_movement_1[0] -= 2560
                if stage_backdrop_movement_2[0] < -1280:
                    stage_backdrop_movement_2[0] += 2560
                elif stage_backdrop_movement_2[0] > 1280:
                    stage_backdrop_movement_2[0] -= 2560
                # endregion

            if stage == "Stage 1":
                screen.blit(stage_1_background, (0, 0))
                screen.blit(stage_1_backdrop, (int(stage_backdrop_movement_2[0]), int(stage_backdrop_movement_1[1])))
                screen.blit(stage_1_backdrop, (int(stage_backdrop_movement_1[0]), int(stage_backdrop_movement_1[1])))
            if stage == "Stage 2":
                screen.blit(stage_2_background, (0, 0))
            
            # region Stage movement
            stage_coords[0] = (0 - stage_movement_x) - stage_start_adjust_x
            if stage_coords[0] >= 0:  # Adjusts the screen to not move past the left border.
                left_border_hit = True
                stage_coords[0] = 0
                player_coords[0] = (590 + stage_movement_x) + stage_start_adjust_x  # Makes the player on screen move instead of the stage.
            else:
                left_border_hit = False
            stage_coords[1] = (0 + stage_movement_y)
            screen.blit(stage_surface, (int(stage_coords[0]), int(stage_coords[1])))
            # endregion

            # region Player animation
            # Setting a frame rate for the loading animation.
            if not paused:
                if player_frame >= 11:  # (a) Must be 10 more than b.
                    player_frame -= 1  # (b) Speed of animation (frame of game/frame of animation) (Bigger # = faster)
                else:
                    player_frame = 59  # (c) First digit must be the number of frames and last digit must be b less than a multiple of 10.

                Animation(player_frame)

            # Blitting the different frames of the idle animation.
            player = player_idle[face][first_digit - 1]
                        
            # Running animation.
            if movement_horizontal_direction != "none":
                if player_run_frame >= 12:  # (a) Must be 10 more than b.
                    player_run_frame -= 2  # (b) Speed of animation (frame of game/frame of animation) (Bigger # = faster)
                else:
                    player_run_frame = 58   # (c) First digit must be the number of frames and last digit must be b less than a multiple of 10.

                Animation(player_run_frame)
                if player_horizontal_acceleration <= 4 and player_horizontal_acceleration >= -4 or first_digit >= 6:
                    player = player_run[face][0]
                else:
                    player = player_run[face][first_digit]
                    
            # Jumping animation.
            if not touching_ground:
                if player_vertical_acceleration > 3:
                    player = player_jump[face][0]
                if 3 >= player_vertical_acceleration >= -3:
                    player = player_jump[face][1]
                if player_vertical_acceleration < -3:
                    player = player_jump[face][2]
            if left_border_hit is True:
                screen.blit(player, (int(player_coords[0]), 310))  # (x, y) Moves the player to adjust for stage not moving.
            else:
                screen.blit(player, (590, 310))  # (x, y) Prints the player at the center of the screen.

            if not paused:
                brightness_change_wait += 1
                if brightness_change_wait >= 4:  # Controls how fast the light flickers. Higher # = slower flicker.
                    brightness_change_wait = 0
                if brightness_change_wait == 0:
                    brightness_change = random.randrange(0, 2)
                    if brightness <= 1:  # Sets the min. brightness.
                        brightness += brightness_change
                    elif brightness >= 4:  # Sets the max. brightness.
                        brightness -= brightness_change
                    else:  # Changes the brightness randomly.
                        if brightness_change == 0:
                            brightness_change = -1
                        brightness += brightness_change
                        
            if in_darkness:
                screen.blit(darkness, ((int(player_coords[0]) - 1230), (-360)))  # Shadow that surrounds the player in dark areas.

            for pos in light_pos:
                pos = list(pos)
                pos[0] -= int(stage_movement_x)
                pos[1] += int(stage_movement_y)
                for nope in range(brightness):
                    screen.blit(torch_light, pos)
                    
            if not in_darkness:
                screen.blit(stage_surface_mg, (int(stage_coords[0]), int(stage_coords[1])))  # Blocks that hide caves and indoors.
                
            # region [Stage Cards]
            if stage_card is True and not paused:
                if 120 > stage_card_1_pos[0] or stage_card_1_pos[0] > 200:  # This makes the card zoom in and out quickly.
                    stage_card_1_pos[0] -= 60
                    stage_card_2_pos[0] += 60
                elif 120 <= stage_card_1_pos[0] <= 200:  # When centered on screen, the card will transition slower.
                    stage_card_1_pos[0] -= 1
                    stage_card_2_pos[0] += 1
                    
                # Stage card animation.
                # Setting a frame rate for the loading animation.
                if stage_card_frame >= 12:  # (a) Must be divisible by itself and 10 more than b.
                    stage_card_frame -= 2  # (b) Speed of animation (frame of game/frame of animation) (Bigger # = faster)
                else:
                    stage_card_frame = 58  # (c) Must be divisible by itself, first digit must be the number of frames and last digit must be b less than a multiple of 10.

                Animation(stage_card_frame)
                        
            if stage_card is True:
                if first_digit == 1:
                    screen.blit(stage_card_2_5, (stage_card_2_pos[0], stage_card_2_pos[1]))
                elif first_digit == 2:
                    screen.blit(stage_card_2_4, (stage_card_2_pos[0], stage_card_2_pos[1]))
                elif first_digit == 3:
                    screen.blit(stage_card_2_3, (stage_card_2_pos[0], stage_card_2_pos[1]))
                elif first_digit == 4:
                    screen.blit(stage_card_2_2, (stage_card_2_pos[0], stage_card_2_pos[1]))
                elif first_digit == 5:
                    screen.blit(stage_card_2_1, (stage_card_2_pos[0], stage_card_2_pos[1]))
                screen.blit(stage_card_1, (stage_card_1_pos[0], stage_card_1_pos[1]))
                
                if stage_card_1_pos[0] <= -960 and stage_card_2_pos[0] >= 1280:
                    stage_card = False
            # endregion
            # endregion

            # region [Menus]
            # Pause menu
            if title_screen is False and paused and options is False:
                screen.blit(paused_text, (0, 0))

        # Options menu
        if paused and options is True or title_screen is True and options is True:
            screen.blit(options_text, (0, 0))
            if not music_muted:
                screen.blit(options_music_on, (0, 0))
            if music_muted:
                screen.blit(options_music_off, (0, 0))

        # Button highlights
        if transition_end_black is False and paused or title_screen is True or options is True:  # Only after a transition has finished can this happen.
            # 1st button
            if 408 <= mousexy[0] <= 875 and 305 <= mousexy[1] <= 385:
                screen.blit(title_text_highlight, (0, 0))
            # 2nd button
            if 408 <= mousexy[0] <= 875 and 408 <= mousexy[1] <= 488:
                screen.blit(title_text_highlight, (0, 104))
            # 3rd button
            if 408 <= mousexy[0] <= 875 and 508 <= mousexy[1] <= 588: 
                screen.blit(title_text_highlight, (0, 204))
            # 4th button
            if 408 <= mousexy[0] <= 875 and 612 <= mousexy[1] <= 692:
                screen.blit(title_text_highlight, (0, 308))
            # Secret button
            if 408 <= mousexy[0] <= 875 and 719 <= mousexy[1] <= 799 and options is False:
                screen.blit(title_text_highlight, (0, 415))
            # endregion
        # endregion

    # region Transitions
    # Fading in:
    if transition_start_type == "fast" or transition_start_type == "slow":
        if transition_start_black is True and transition_end_black is False:
            if opacity < 255:  # max opacity.
                opacity += (transition_speed * 2)  # How quickly the transition goes. (shade/frame)
                if carry_on:
                    transition_screen.set_alpha(opacity)
                else:
                    transition_screen.set_alpha(opacity / (transition_speed * 10))
                screen.blit(transition_screen, (0, 0))
            else:  # Passing on the transition phase.
                transition_start_black = False
                transition_load_black = True
                transition_timer = 0
                Load_Map(level)
                Load_Stage()
                pygame.mixer.music.stop()
                
    # Loading screen:
    if transition_timer < transition_time and transition_load_black is True:
        transition_timer += 1
        opacity = 255
        transition_screen.set_alpha(opacity)
        # screen.blit(transition_screen, (0, 0))
        screen.fill((0, 0, 0))
        screen.blit(loading_screen, (0, 0))

        # Loading Animation
        ## Setting a frame rate for the loading animation.
        if loading_frame >= 11:  # (a) Must be divisible by itself and 10 more than b.
            loading_frame -= 1  # (b) Speed of animation (frame of game/frame of animation) (Bigger # = faster)
        else:
            loading_frame = 59  # (c) Must be divisible by itself, first digit must be the number of frames and last digit must be b less than a multiple of 10.

        Animation(loading_frame)

        # Blitting the different frames of the loading animation.
        if first_digit == 1:
            screen.blit(loading_frame_5, (595, 500))
        elif first_digit == 2:
            screen.blit(loading_frame_4, (595, 500))
        elif first_digit == 3:
            screen.blit(loading_frame_3, (595, 500))
        elif first_digit == 4:
            screen.blit(loading_frame_2, (595, 500))
        elif first_digit == 5:
            screen.blit(loading_frame_1, (595, 500))
    else:  # Passing on the transition phase.
        if transition_load_black is True:
            transition_timer = 0
            transition_load_black = False
            transition_end_black = True
            carry_on = True
            if title_screen is True:  # Playing music
                Titlesong = pygame.mixer.music.load('Audio/Pure Numbness.wav')
                if not music_muted:
                    pygame.mixer.music.play(-1)
            else:
                if stage == "Stage 1":  # v-- Plays music when loading stops. --v
                    Stage_1 = pygame.mixer.music.load('Audio/Home World Theme.wav')
                    if not music_muted:
                        pygame.mixer.music.play(-1)
                elif stage == "Stage 2":
                    Stage_1 = pygame.mixer.music.load('Audio/Success.wav')
                    if not music_muted:
                        pygame.mixer.music.play(-1)
                        
    # Fading out:
    if transition_end_black is True and transition_start_black is False:
        if opacity > 0:
            if transition_end_type == "fast":
                opacity -= (transition_speed * 5)  # How quickly the transition goes. (shade/frame)
            elif transition_end_type == "slow":
                opacity -= (transition_speed * 2)  # How quickly the transition goes. (shade/frame)
            if carry_on:
                transition_screen.set_alpha(opacity)
            else:
                transition_screen.set_alpha(opacity)
            screen.blit(transition_screen, (0, 0))
        else:  # Ending the transition phase.
            transition_end_black = False
            Stage_Card()
    # endregion

    # region Extras at End
    # Refresh Screen
    pygame.display.flip()
    # FPS
    clock.tick(60)
    # endregion

pygame.quit()
exit()
# endregion
