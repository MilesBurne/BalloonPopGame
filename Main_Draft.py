#Main_Draft by Miles Burne 14/3/19
'''
This is the second main draft for the game, it links multiple modules together
in different files.
'''

#imports
import pygame
#custom imports
from Quadratic_Module import * 
from Projectile_Module import *
from Target_Module import *

#creates the board and draws the axes, takes width and height of screen
def draw_game(screen_dimensions):
    #screen sizes
    s_width, s_height = screen_dimensions[0], screen_dimensions[1]
    
    #make screen
    gameDisplay = pygame.display.set_mode((s_width, s_height))
    
    #fill
    gameDisplay.fill((34,161,235))

    #axes creation
    #y_list = [(0,0),(0,s_height)]
    #x_list = [(0,((s_height/4)*3)),(s_width,((s_height/4)*3))]

    #axes initialisation
    #pygame.draw.lines(screen, (255,255,255), False, y_list, 2) # y
    pygame.draw.rect(gameDisplay, (26,137,14),[0, ((s_height/4)*3), (s_width), (s_height/4)],0) # creates rect for x

    return(gameDisplay)

#this displays the quadratic equation to the screen, takes quadratic equation and the gameDisplay
def show_quadratic(quadratic, gameDisplay):
    #getting size of screen
    display_w, display_h = pygame.display.Info().current_w, pygame.display.Info().current_h
    #reference for object quadratic
    quad = quadratic
    #getting a and b and multiplying by ten to make the program more readable
    a = quad.get_a()*100
    b = int(quad.get_b()*100)
    c = quad.get_c()
    #splitting the text into multiple portions to allow for multiple colours, also rounds a and b to ensure they arent too large
    a_text = (str(round(a, 4)))
    x2_text = ("x\N{SUPERSCRIPT TWO} +") #uses \N{SUPERSCRIPT TWO} to get x^2 as superscript
    b_text = (str(round(b, 4)))
    xc_text = ("x + "+str(c))
    #getting font
    pygame.font.init() #init the font module
    font_name = "calibri" #naming the font used 
    myFont = pygame.font.SysFont(font_name,60) #init the font itself, form(font_name, size)
    #rendering text, creates surface with input: text, anti-alias, rgb colour
    a_surface = myFont.render(a_text, True, (232, 48, 60)) 
    x2_surface = myFont.render(x2_text, True, (0,0,0))
    b_surface = myFont.render(b_text, True, (52, 61, 229))
    xc_surface = myFont.render(xc_text, True, (0,0,0))
    #creates width and height for text surface
    text_width = (a_surface.get_rect()[2]+x2_surface.get_rect()[2]+b_surface.get_rect()[2]+xc_surface.get_rect()[2])
    text_height = (x2_surface.get_rect()[3])
    #creates text surface based off of dimensions
    text_surface = pygame.Surface((text_width, text_height))
    #filling text surface with correct colour (green)
    text_surface.fill((26,137,14))
    #getting rect of surface
    text_rect = text_surface.get_rect()
    #renders the surfaces to text_surface
    text_surface.blit(a_surface, (0,0))
    text_surface.blit(x2_surface, (a_surface.get_width(),0))
    text_surface.blit(b_surface, (a_surface.get_width()+x2_surface.get_width(),0))
    text_surface.blit(xc_surface, (a_surface.get_width()+x2_surface.get_width()+b_surface.get_width(),0))
    '''
    #sizing text_surface
    change_w = int((display_w*3/5))
    change_h = int((display_w*3/5)/text_rect[2] *text_rect[3])
    text_surface = pygame.transform.smoothscale(text_surface, (change_w,change_h))
    #getting rect of surface
    text_rect = text_surface.get_rect()
    '''
    #positioning text_rect
    text_rect.centerx = gameDisplay.get_rect().centerx         
    text_rect.centery = (gameDisplay.get_rect().centery + display_h*3/8)
    #renders to game display
    gameDisplay.blit(text_surface, text_rect)

#displays the points of the user
def levelpoint_display(gameDisplay, points, level):
    #getting size of screen
    display_w, display_h = pygame.display.Info().current_w, pygame.display.Info().current_h
    #defining the text
    pre_points_text = ("Score: ")
    points_text = str(points)
    pre_level_text =  ("Level: ")
    level_text = str(level)
    #getting font
    pygame.font.init() #init the font module
    font_name = "calibri" #naming the font used 
    myFont = pygame.font.SysFont(font_name,20) #init the font itself, form(font_name, size)
    #rendering text, creates surface with input: text, anti-alias, rgb colour
    pre_points_surface = myFont.render(pre_points_text, True, (0,0,0)) 
    points_surface = myFont.render(points_text, True, ((239, 26, 26)))
    pre_level_surface = myFont.render(pre_level_text, True, (0,0,0)) 
    level_surface = myFont.render(level_text, True, ((239, 26, 26)))
    #creates width and height of surface
    text_width = max((pre_points_surface.get_rect()[2]+points_surface.get_rect()[2]),(pre_level_surface.get_rect()[2]+level_surface.get_rect()[2]))
    text_height = (pre_points_surface.get_rect()[3]+pre_level_surface.get_rect()[3])
    #creates text surface based off of dimensions
    text_surface = pygame.Surface((text_width, text_height))
    #filling text surface with correct colour (blue)
    text_surface.fill((34,161,235))
    #getting rect of surface
    text_rect = text_surface.get_rect()
    #renders the surfaces to text_surface
    text_surface.blit(pre_points_surface, (0,0))
    text_surface.blit(points_surface, (pre_points_surface.get_width(),0))
    text_surface.blit(pre_level_surface, (0,pre_points_surface.get_height()))
    text_surface.blit(level_surface, (pre_level_surface.get_width(),pre_points_surface.get_height()))
    #renders to game display
    gameDisplay.blit(text_surface, (0,0))
    

#draws the quadratic graph to the screen,  takes quadratic equation and the gameDisplay
def draw_quadratic(quadratic, gameDisplay):
    #getting size of screen
    display_w, display_h = pygame.display.Info().current_w, pygame.display.Info().current_h

    #reference for object quadratic
    quad = quadratic
    
    #init pygame
    pygame.init()

    #draw the equation by creating many small lines
    for x in range(0, display_w):
        if x%2 and x%5:
            y = (-1*quad.get_y(x)) + (display_h/4)*3  #establishes minimum height by shifting graph up by set amount
            if y < ((display_h/4)*3):
                line_list = [(x,y),((x+1),((-1*quad.get_y(x+1)) +(display_h/4)*3))] #puts two points in a 2D array, the original point and the next one along
                pygame.draw.aalines(gameDisplay, (0,0,0), False, line_list, True) #draws an AA line, which blends the line to make it smoother. Set True to False to disable this
            else:
                break
        else:
            pass

#instantiates the quadratic equation object, or changes the values if the equation object is passed in
def make_quadratic(a,b,Quadratic=0):
    #when just a and b passed in
    if Quadratic == 0:
        #fiddling a and b to ensure that quadratics are not too high
        a = a/100
        b = b/100
        #initial c
        c = 9.7
        #init quadratic equation
        quad = quadratic_equation(a,b,c)
        #returns reference to object
        return(quad)
    #when quadratic reference has been passed in
    else:
        #fiddling a and b to ensure that quadratics are not too high
        a = a/100
        b = b/100
        #creatng quadratic variable for use
        quad = Quadratic
        #changes equation
        quad.change_var(a,b)
        return(quad)

#function to detect collisions of the two main objects
def detect_collision(Target,Projectile,points, level):
    tar = Target
    proj = Projectile
    #getting rect of projectile
    proj_rect = proj.get_rect()
    #checking collisons using target
    collision_bool = tar.detect_collision(proj_rect)
    if collision_bool == True:
        proj.reset()
        tar.reset()
        points += 50
        level += 1
        return(points,level,True)
    else:
        return(points,level,False)
    
#main portion of the game, acts as a main loop
def main():
    #init pygame
    pygame.init()
    #creates screen size
    screen_dimensions = (1100,700)
    #gets the screen from draw_game function
    gameDisplay = draw_game(screen_dimensions)
    #defines players current points and current level
    points = 0
    level = 1
    #creates default a and b values 
    quad_a = -0.1
    quad_b = 80
    #creates start positions for objects
    target_start = ((screen_dimensions[0]/4*3),(screen_dimensions[1]/4*3))
    projectile_start = (0,(screen_dimensions[1]/4*3))
    #instantiate quadratic object by calling make_quadratic function
    quadratic = make_quadratic(quad_a,quad_b)
    #instantiate balloon object
    target = Target(gameDisplay, target_start)
    projectile = Projectile(gameDisplay, projectile_start,quadratic)
    #controls movement of the projectile
    projectile_motion = False
    #creates the main game loop
    running = True
    while running:
        #updates screen after every gameloop
        pygame.display.flip()
        #draws the main screen to prevent overlaps
        draw_game(screen_dimensions)
        #updates quadratic with new values using the make_quadratic function and an optional value
        quadratic = make_quadratic(quad_a,quad_b,quadratic)
        #draws the quadratic path and equation for the first time
        draw_quadratic(quadratic, gameDisplay)
        show_quadratic(quadratic, gameDisplay)
        #draws the level and points to the screen
        levelpoint_display(gameDisplay,points,level)
        #moves target
        target.move()
        #collision detection
        if projectile_motion == True:
            points,level,collision = detect_collision(target,projectile,points,level)
            if collision == True: #therefore points have increased and collision has happened
                projectile_motion = False
            #in case of no collision
            else:
                projectile_motion = projectile.move(projectile_motion) #projectile stops when movement stops
                if projectile_motion == False:
                    points -= 50
        else:
            projectile_motion = projectile.move(projectile_motion) #projectile stops when movement stops
        #event handling using pygame events
        for event in pygame.event.get():
            #if quit
            if event.type == pygame.QUIT:
                running = False
                break

            #if keyboard press
            if event.type == pygame.KEYDOWN:
                #if key is escape
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

                #changing A
                if event.key == pygame.K_UP:
                    quad_a += 0.01
                if event.key == pygame.K_DOWN:
                    quad_a -= 0.01
                #making sure that A is in a valid range, only needs to change when A is changed
                if quad_a > 0:
                    quad_a = 0
                
                #changing B
                if event.key == pygame.K_LEFT:
                    quad_b -= 1
                if event.key == pygame.K_RIGHT:
                    quad_b += 1
                
                #launching projectile
                if event.key == pygame.K_SPACE:
                    #launch projectile
                    projectile_motion = True
                
                    
        

                
                
main()
pygame.quit()
    
