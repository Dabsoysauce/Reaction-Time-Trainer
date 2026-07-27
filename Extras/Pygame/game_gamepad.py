"""
This is a demo game using Pygame. It interfaces with the user
via the keyboard and the 2.4 GHz wireless USB controller.
The aim of the game is to move the player (the dot) until it hits 
the image.
    arrow keys: move the player
    space bar:  bring the player back to the center
    arrow pad on the left of the controller: move the player
    
There appears to be a bug in Pygame. The result is that this
program crashes after a few minutes. It is reported that 
running this in Python2 may work but we have not tested this.    
"""


# General libraries
import time
import random
import os
# Libraries for the gamepad
from evdev import InputDevice, categorize
# Libraries for pygame
import pygame
from pygame.locals import *


# Check if the gamepad is connected
# You need to adjust the event number if the wrong input device is read
gamepad = InputDevice('/dev/input/event4')
print(gamepad)
print("")
print("Close the game window to end the program")

pygame.init()
#pygame.camera.init()

dim_field = (400,400)
dim_player = (30,30)
step = 5
title = "Demo game"

FPS = 50
BLUE = (0,0,255)
TRANSPARENT = (0,0,0,0)
color_text_hit = (255,0,0)



def reset_target(dim_field, dim_target):
    target_x = random.randrange(0, dim_field[0]-dim_target[0])
    target_y = random.randrange(0, dim_field[1]-dim_target[1])
    return (target_x, target_y)
    
def collide(coord_obj1, coord_obj2, mask_obj1, mask_obj2):
    offset_x = coord_obj2[0] - coord_obj1[0]
    offset_y = coord_obj2[1] - coord_obj1[1]
    return mask_obj1.overlap(mask_obj2, (offset_x, offset_y)) != None


try:
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(dim_field)
    pygame.display.set_caption(title)
    
    timer_text_hit = USEREVENT+1

    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 50)
    text_hit = font.render("BOOM", True, color_text_hit)

    background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "grass.jpg")), dim_field)
    target = pygame.image.load(os.path.join("assets", "mohan.png"))
    #transColor = target.get_at((0,0))
    #target.set_colorkey(transColor)
    #print(target.get_alpha())
    #target.convert()
    #print(target.get_alpha())
    target.set_colorkey((255,255,255))
    #target.convert_alpha()
    #target.fill(TRANSPARENT)
    #target.set_colorkey((174, 115, 93))
    #target.set_alpha(50)
    mask_target = pygame.mask.from_surface(target)

    dim_target = target.get_size()
    target_exists = False

    player = pygame.Surface(dim_player).convert_alpha()
    player.fill(TRANSPARENT)
    pygame.draw.circle(player,(0,0,255),(dim_player[0]//2,dim_player[1]//2),dim_player[0]//2)
    mask_player = pygame.mask.from_surface(player)

    coord_text_hit = (dim_field[0]//2,dim_field[1]//2)
    coord_player = coord_text_hit


        
    #cam = pygame.camera.Camera("/dev/video0",(640,480))
    #cam.start()
    #background = cam.get_image()

    run = True
    show_text_hit = False
    framerate = FPS
    x_inc = 0;
    y_inc = 0;
    while run:
    
        clock.tick(framerate)

        screen.blit(background, (0, 0))

        if not target_exists:
            target_exists = True
            coord_target = reset_target(dim_field, dim_target)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    coord_player = coord_text_hit
                    framerate = FPS
            if event.type == timer_text_hit:
                show_text_hit = False
                pygame.time.set_timer(timer_text_hit, 0)

        # Process the gamepad events
        # This implementation is non-blocking
        newbutton = False
        newstick  = False
        try:
                for event in gamepad.read():            # Use this option (and comment out the next line) to react to the latest event only
                    #event = gamepad.read_one()         # Use this option (and comment out the previous line) when you don't want to miss any event
                    eventinfo = categorize(event)
                    if event.type == 1:
                        newbutton = True
                        codebutton  = eventinfo.scancode
                        valuebutton = eventinfo.keystate
                    elif event.type == 3:
                        newstick = True
                        codestick  = eventinfo.event.code
                        valuestick = eventinfo.event.value
                        
                    if (newstick):
                        if (codestick == 0):
                            if (valuestick == 0):
                                x_inc = -1
                            elif (valuestick == 255):
                                x_inc = 1
                            else:
                                x_inc = 0
                        if (codestick == 1):
                            if (valuestick == 0):
                                y_inc = -1
                            elif (valuestick == 255):
                                y_inc = 1
                            else:
                                y_inc = 0
        except:
                pass

        delta_x = 0
        delta_y = 0
        
        # If there was a gamepad event, show it
        #if newbutton:
        #        print("Button: ",codebutton,valuebutton)
        #if newstick:
        #        print("Stick : ",codestick,valuestick)

        # Option 1: keep moving as long as pressed
        option = 1
        if (option == 1):
            if (x_inc != 0):
                delta_x += x_inc*step
            if (y_inc != 0):
                delta_y += y_inc*step
                        
        # Option 2: move once with each press
        else:
            if (newstick and codestick == 0):
                if (valuestick == 0):
                    delta_x -= step
                elif (valuestick == 255):
                    delta_x += step
            if (newstick and codestick == 1):
                if (valuestick == 0):
                    delta_y -= step
                elif (valuestick == 255):
                    delta_y += step            
                           
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP]):
            delta_y -= step;
        if (keys[pygame.K_DOWN]):
            delta_y += step;
        if (keys[pygame.K_RIGHT]):
            delta_x += step;
        if (keys[pygame.K_LEFT]):
            delta_x -= step;
            

            
        coord_player = (coord_player[0]+delta_x, coord_player[1]+delta_y)                                        

        if collide(coord_target, coord_player, mask_target, mask_player):
            pygame.display.set_caption(title + ': boom!')
            pygame.time.set_timer(timer_text_hit, 500)
            show_text_hit = True
            coord_target = reset_target(dim_field, dim_target)
            framerate *= 2
        else:
            pygame.display.set_caption(title)
            
            
        screen.blit(target, coord_target)
        #target_rect = pygame.Rect(coord_target,(40,40))
        #print(target.get_rect().size)
        #player_rect = pygame.Rect(coord_player,(40,40))
        #pygame.draw.rect(screen,(0,0,0),target_rect)
        #pygame.draw.rect(screen,(0,0,0),player_rect)
        #if player_rect.colliderect(target_rect): 
        #    pygame.display.set_caption(title + ': boom!')
            
            
        screen.blit(player, coord_player)
        if show_text_hit:
            screen.blit(text_hit, coord_text_hit)
        
        pygame.display.update()    
    
    
    pygame.display.quit()
    pygame.quit()
  

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    gamepad.close()  
    pygame.display.quit()
    pygame.quit()    

