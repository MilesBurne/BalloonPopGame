#Final Product by Miles Burne 1/4/19
#imports
import pygame
import random
import math
#custom imports
from Quadratic_Module import * 
from Projectile_Module import *
from Target_Module import *
from Save_Module import *
from Crate_Module import *
from Wall_Module import *
from Indicator_Module import *

#game class to handle the running of the game
class Game():
    #init, takes screen dimensions as (width,height), and points and level
    def __init__(self,gameDisplay,points=0,level=1,from_save=False):
        #getting size of screen
        self.s_width, self.s_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen_dimensions = (self.s_width,self.s_height)
        self.gameDisplay = gameDisplay #this will hold the screen surface
        self.points = points
        self.level = level
        #references to objects
        self.Target_List = []
        self.Projectile = 0
        self.Quadratic = 0
        self.Crate = 0
        self.Wall = 0
        self.Indicators = []
        #previously used values used to replace values after the crate levels
        self.prev_a = -0.1
        self.prev_b = 80
        #toggle for crate level
        self.crate_level = False
        #creates the target b for the crate
        self.crate_target_b = 0
        #variables to control difficulty
        self.quadratic_hide_level = 5 #game hides quadratic on this level
        self.show_quadratic_toggle = True
        self.add_target_level = [10,20,30,40,50] #game adds a balloon on these levels
        self.current_target_level = 1
        #creates default starting x position for target
        self.default_target_start = ((self.screen_dimensions[0]/16*15),(self.screen_dimensions[1]/4*3))
        self.next_target_start = 15/16
        #creates the game, also calls 'create_loaded_game' if the game has been loaded from a save
        self.create_game()
        #counter for detecting the loss
        self.loss_counter = 0
        #checking if game has been created from a save or not
        if from_save == True:
            self.create_loaded_game()

    #creates the games objects
    def create_game(self):
        #init pygame
        pygame.init()
        #draws the game
        self.draw_game()
        #adds a name for the window
        pygame.display.set_caption("Balloon Pop")
        #creates default a and b values 
        self.quad_a = -0.1
        self.quad_b = 80
        #creates start positions for object projectile
        projectile_start = (0,(self.screen_dimensions[1]/4*3))
        #instantiate quadratic object by calling make_quadratic function
        self.make_quadratic(self.quad_a,self.quad_b)
        #instantiate objects
        self.Target_List.append(Target(self.gameDisplay, self.default_target_start))
        self.Projectile = Projectile(self.gameDisplay, projectile_start,self.Quadratic)
        self.Crate = Crate(self.gameDisplay)
        self.Wall = Wall(self.gameDisplay)

    #creates equation for crate hitting
    def create_crate_equation(self,c=9.7):
        #defining variables to be used
        wall_height = self.Wall.get_height() +50 #maximum a little higher than wall height
        ball_height = self.Quadratic.get_c()
        crate_distance = self.Crate.get_actual_coords().midbottom[0]
        #formuli to find A and B 
        A_find = ((2/(crate_distance**2))*(ball_height-(2*wall_height)))
        B_find = ((-1/crate_distance)*((A_find*(crate_distance**2)) + ball_height))
        self.quad_a = round(A_find,4)*100
        self.crate_target_b = round(B_find,2)

    #is run if the game detects it is loaded from a save
    def create_loaded_game(self):
        #increases the level of the game procedurally
        for x in range(1,self.level+1):
            self.increase_difficulty(x)
        
    #creates the board and draws the axes
    def draw_game(self):
        #fill
        self.gameDisplay.fill((34,161,235))
        #creates green
        pygame.draw.rect(self.gameDisplay, (26,137,14),[0, ((self.s_height/4)*3), (self.s_width), (self.s_height/4)],0) # creates rect for x

    #draws indicators to screen
    def draw_indicator(self):
        #if indicators have not been created create them
        if len(self.Indicators) == 0:
            #calls create indicators function
            self.create_indicators()
        for x in self.Indicators:
            #up and down indicators should be shaded on every 5th level
            if (x.get_direction() == "u" or x.get_direction() == "d") and self.level % 5 == 0:
                x.set_shaded(True)
            #otherwise normal colour
            else:
                x.set_shaded(False)
            #draws
            x.draw_to_screen()

    #creates the position for indicators, indicators are created from TL,TR,BL,BR
    def create_indicators(self):
        #gets the center of text
        target_x= self.gameDisplay.get_rect().centerx         
        target_y = (self.gameDisplay.get_rect().centery + self.s_height*3/8)
        #indicator1
        indicatorTL_y = target_y - (self.quad_text_height)/2 - 25
        indicatorTL_x = target_x - 140
        indicatorTL = Indicator(self.gameDisplay,(indicatorTL_x,indicatorTL_y),(232, 48, 60),(26,137,14),direction="u",light_colour=(252, 67, 67))
        #indicator2
        indicatorTR_y = target_y - (self.quad_text_height)/2 - 25
        indicatorTR_x = target_x + 50
        indicatorTR = Indicator(self.gameDisplay,(indicatorTR_x,indicatorTR_y),(52, 61, 229),(26,137,14),direction="r",light_colour=(88,95,221))
        #indicator3
        indicatorBL_y = target_y + (self.quad_text_height)/2 + 25
        indicatorBL_x = target_x + 50
        indicatorBL = Indicator(self.gameDisplay,(indicatorBL_x,indicatorBL_y),(52, 61, 229),(26,137,14),direction="l",light_colour=(88,95,221))
        #indicator4
        indicatorBR_y = target_y + (self.quad_text_height)/2 + 25
        indicatorBR_x = target_x - 140
        indicatorBR = Indicator(self.gameDisplay,(indicatorBR_x,indicatorBR_y),(232, 48, 60),(26,137,14),direction="d",light_colour=(252, 67, 67))
        #adds to indicators list
        self.Indicators = [indicatorTL,indicatorTR,indicatorBL,indicatorBR]

    #switches the colour of the indicators, takes input of indicator reference(TL:1,TR:2,BR:3,BL:4) and "light"/"dark"
    def change_indicator_colour(self,spec_indicator,colour="dark"):
        indicator_val = spec_indicator-1
        #changes colour of corresponding indicators to specified colour  
        if colour.lower() == "dark":
            self.Indicators[indicator_val].set_colour(False)
        elif colour.lower() == "light":
            self.Indicators[indicator_val].set_colour(True)
        else:
            pass #colour will not change
        
    #this displays the quadratic equation to the screen
    def show_quadratic(self):
        #getting a and b and multiplying by ten to make the program more readable
        a = self.Quadratic.get_a()#*100
        b = self.Quadratic.get_b()#*100)
        c = self.Quadratic.get_c()
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
        text_rect.centerx = self.gameDisplay.get_rect().centerx         
        text_rect.centery = (self.gameDisplay.get_rect().centery + self.s_height*3/8)
        #for use in indicator module
        self.quad_text_height = text_rect[3]
        #renders to game display
        self.gameDisplay.blit(text_surface, text_rect)

    #displays the points of the user
    def levelpoint_display(self):
        #defining the colour for the points and level
        pointLevelColour = (239, 26, 26)
        #defining the text
        pre_points_text = ("Score: ")
        points_text = str(self.points)
        pre_level_text =  ("Level: ")
        level_text = str(self.level)
        #getting font
        pygame.font.init() #init the font module
        font_name = "calibri" #naming the font used 
        myFont = pygame.font.SysFont(font_name,20) #init the font itself, form(font_name, size)
        #rendering text, creates surface with input: text, anti-alias, rgb colour
        pre_points_surface = myFont.render(pre_points_text, True, (0,0,0)) 
        points_surface = myFont.render(points_text, True, (pointLevelColour))
        pre_level_surface = myFont.render(pre_level_text, True, (0,0,0)) 
        level_surface = myFont.render(level_text, True, (pointLevelColour))
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
        self.gameDisplay.blit(text_surface, (0,0))

    #draws the relative coords for the crate to the screen
    def relative_coord_display(self):
        #colour for the x part of coords (blue)
        x_colour = (19, 62, 219)
        #getting the location of the crate as rect
        crate_location = self.Crate.get_actual_coords()
        #creating the location for the coords display
        target_location = (crate_location.midbottom[0],crate_location.midbottom[1]-2)
        #creating the text to be displayed
        pre_x_string = ("(")
        x_string = str(self.Crate.get_relative_coords()[0])
        post_x_string = (",0)")
        #getting font
        pygame.font.init() #init the font module
        font_name = "calibri" #naming the font used 
        myFont = pygame.font.SysFont(font_name,16) #init the font itself, form(font_name, size)
        #rendering text, creates surface with input: text, anti-alias, rgb colour
        pre_x_surface = myFont.render(pre_x_string, True, (0,0,0)) 
        x_surface = myFont.render(x_string, True, (x_colour))
        post_x_surface = myFont.render(post_x_string, True, (0,0,0))
        #creates width and height of surface
        text_width = (pre_x_surface.get_rect()[2]+x_surface.get_rect()[2]+post_x_surface.get_rect()[2])
        text_height = (pre_x_surface.get_rect()[3])
        #creates text surface based off of dimensions
        text_surface = pygame.Surface((text_width, text_height))
        #filling text surface with correct colour (brown)
        text_surface.fill((140,70,0))
        #getting rect of surface and changing location of it
        text_rect = text_surface.get_rect()
        text_rect.midbottom = target_location
        #renders the surfaces to text_surface
        text_surface.blit(pre_x_surface, (0,0))
        text_surface.blit(x_surface, (pre_x_surface.get_width(),0))
        text_surface.blit(post_x_surface, (pre_x_surface.get_width()+x_surface.get_width(),0))
        #renders to game display
        self.gameDisplay.blit(text_surface, text_rect)

    #draws the quadratic graph to the screen
    def draw_quadratic(self):
        #draw the equation by creating many small lines
        for x in range(0, self.s_width):
            if x%2 and x%5:
                y = (-1*self.Quadratic.get_y(x)) + (self.s_height/4)*3  #establishes minimum height by shifting graph up by set amount
                if y < ((self.s_height/4)*3):
                    line_list = [(x,y),((x+1),((-1*self.Quadratic.get_y(x+1)) +(self.s_height/4)*3))] #puts two points in a 2D array, the original point and the next one along
                    pygame.draw.aalines(self.gameDisplay, (0,0,0), False, line_list, True) #draws an AA line, which blends the line to make it smoother. Set True to False to disable this
                else:
                    break
            else:
                pass
    
    #instantiates the quadratic equation object, or changes the values if the equation object is passed in
    def make_quadratic(self,a,b):
        #when just a and b passed in
        if self.Quadratic == 0:
            #fiddling a and b to ensure that quadratics are not too high
            a = a/100
            b = b/100
            #initial c
            c = 9.7
            #init quadratic equation
            self.Quadratic = quadratic_equation(a,b,c)
        #when quadratic reference has been passed in
        else:
            #fiddling a and b to ensure that quadratics are not too high
            a = a/100
            b = b/100
            #changes equation
            self.Quadratic.change_var(a,b)

    #creates a list of if a target is hit
    def create_hit_list(self):
        hit_list = []
        for x in self.Target_List:
            hit_list.append(x.is_target_hit())
        return(hit_list)

    #changes the state of all targets to unhit
    def unhit_target(self):
        for x in self.Target_List:
            x.set_target_hit(False)

    #method to detect collisions of the main objects
    def detect_collision(self):
        #variable to detect collision
        collided = False
        #getting rect of projectile
        proj_rect = self.Projectile.get_rect()
        #if projectile hits crate
        if self.Crate.detect_collision(proj_rect) == True:
            self.loss_counter = 0 #hit therefore resetting counter
            self.Projectile.reset()
            self.level += 1
            self.points += 100
            self.hide_show_targets(True)
            self.Crate.set_visible(False)
            self.Wall.set_visible(False)
            collided = True
            self.increase_difficulty()
        #if projectile hits wall
        if self.Wall.detect_collision(proj_rect) == True:
            self.Projectile.reset()
            self.points -= 100
            self.loss_counter += 1
            collided = True
        else:
            for x in self.Target_List:
                #checking collisons using target
                collision_bool = x.detect_collision(proj_rect)
                #if has collided
                if collision_bool == True:
                    self.loss_counter = 0 #hit therefore resetting counter
                    collided = True
                    self.Projectile.reset()
                    #THIS target is hit
                    x.reset()
                    #points for each successful hit
                    self.points += 10 #10 points per hit
                    #creates hit_list
                    hit_list = self.create_hit_list()
                    #checks if level can increase
                    if False not in hit_list:
                        self.points += 100
                        self.level+=1
                        self.unhit_target()
                        self.increase_difficulty()
                    collided = True
                else:
                    pass
        return(collided)

    #hides or shows all the targets
    def hide_show_targets(self,boolean):
        for x in self.Target_List:
            x.set_visible(boolean)

    #method to increase the difficulty of the game, takes artificial_level as a default value of 0
    def increase_difficulty(self,artificial_level=0):
        #used for leveling up from a save file, if the level passed in is not 0
        if artificial_level != 0:
            level = artificial_level
        else:
            level = self.level
        #if prev level was crate level, replaces equation with previous
        if (level-1) % 5 == 0:
            self.crate_level = False
            self.quad_a = float(self.prev_a)
            self.quad_b = float(self.prev_b)
        #if level greater than minimum hide quadratic level, then hides quadratic
        if level >= self.quadratic_hide_level:
            self.show_quadratic_toggle = False
        #if level is in the add target level list
        if level in self.add_target_level:
            #moves start position for next target
            self.next_target_start -= 2/16
            target_start = ((self.screen_dimensions[0]*(self.next_target_start)),self.default_target_start[1])
            #creates new target
            self.Target_List.append(Target(self.gameDisplay, target_start))
        #makes each target difficulty higher
        for x in self.Target_List:
            x.collide()   
        #if 5 is a factor of level number, it is crate level
        if level%5 == 0:
            #saves previous equation
            self.prev_a = str(self.quad_a)
            self.prev_b = str(self.quad_b)
            #creates toggle for crate level
            self.crate_level = True 
            #hide all the targets
            self.hide_show_targets(False)
            #create the crate at new position
            self.Crate.create_new_location()
            #creates the new equation
            self.create_crate_equation()
            #create the wall at new position
            self.Wall.set_visible(True)
        #otherwise normal level
        else:
            #disables all objects in crate level
            self.crate_level = False
            self.hide_show_targets(True)
            self.Wall.set_visible(False)
            self.Crate.set_visible(False)
                             

    #method to move each target in Target_List
    def target_move(self):
        #cycles through targets
        for x in self.Target_List:
            #moves target
            x.move()

    #returns points and level if the game is quit before loss
    def save_game(self):
        return(self.points,self.level,True) #returns points, level and boolean to say game has been quit by user

    #called if the game is lost
    def lose_game(self):
        return(self.points,self.level,False) #returns points, level and boolean to say game has been lost
        
    #main portion of the game, acts as a main loop
    def run_game(self):
        #controls movement of the projectile
        projectile_motion = False
        #creates the main game loop
        running = True
        #key checker to ensure not too fast
        key_checker = 0
        #starts game clock to keep fps locked
        clock = pygame.time.Clock()
        #variables to control indicator colour ticks
        K_UP_TRI = 0
        K_DOWN_TRI = 0
        K_LEFT_TRI = 0
        K_RIGHT_TRI = 0
        while running:
            #caps fps to value
            clock.tick(100)
            #updates screen after every gameloop
            pygame.display.flip()
            #draws the main screen to prevent overlaps
            self.draw_game()
            #updates quadratic with new values using the make_quadratic function and an optional value
            self.make_quadratic(self.quad_a,self.quad_b)
            #draws the quadratic path and equation for the first time, shows quadratic if toggle is true
            if self.show_quadratic_toggle == True:
                self.draw_quadratic()
            self.show_quadratic()
            #draws indicators
            self.draw_indicator()
            #draws the level and points to the screen
            self.levelpoint_display()
            #moves target
            self.target_move()
            #detecting loss
            if self.loss_counter == 3:
                #lose game is missed so many times
                return(self.lose_game())
            #collision detection
            if projectile_motion == True:
                collision = self.detect_collision()
                if collision == True: #therefore collision has happened
                    projectile_motion = False
                #in case of no collision
                else:
                    projectile_motion = self.Projectile.move(projectile_motion) #projectile stops when movement stops
                    #therefore has missed
                    if projectile_motion == False:
                        self.points -= 50 #missed so losing points
                        self.loss_counter += 1 
            else:
                projectile_motion = self.Projectile.move(projectile_motion) #projectile stops when movement stops
            #handling crate display, has to be after collision detect so self.relative_coords exist
            self.Crate.display()
            self.Wall.display()
            if self.level % 5 == 0:
                self.relative_coord_display()

            #event handling using pygame events
            for event in pygame.event.get():
                #if quit
                if event.type == pygame.QUIT:
                    #if the game is quit without a loss, game data is returned
                    return(self.save_game())
                    

                #if keyboard press
                if event.type == pygame.KEYDOWN:
                    #if key is escape
                    if event.key == pygame.K_ESCAPE:
                        #if the game is quit without a loss, game data is returned
                        return(self.save_game())
                        
                    #changing A
                    if self.level % 5 != 0:
                        if event.key == pygame.K_UP and projectile_motion == False:
                            self.quad_a += 0.01
                            K_UP_TRI = 5
                            #switches indicator colour to light
                            self.change_indicator_colour(1,"light")
                        if event.key == pygame.K_DOWN and projectile_motion == False:
                            self.quad_a -= 0.01
                            K_DOWN_TRI = 5
                            #switches indicator colour to light
                            self.change_indicator_colour(4,"light")
                    #making sure that A is in a valid range, only needs to change when A is changed
                    if self.quad_a > 0:
                        self.quad_a = 0
                    
                    #changing B
                    if event.key == pygame.K_LEFT and projectile_motion == False:
                        K_LEFT_TRI = 5
                        if self.level % 5 != 0:
                            self.quad_b -= 1
                            #switches indicator colour to light
                            self.change_indicator_colour(3,"light")
                        else:
                            self.quad_b -= 1
                            #switches indicator colour to light
                            self.change_indicator_colour(3,"light")
                    if event.key == pygame.K_RIGHT and projectile_motion == False:
                        K_RIGHT_TRI = 5
                        if self.level % 5 != 0:
                            self.quad_b += 1
                            #switches indicator colour to light
                            self.change_indicator_colour(2,"light")
                        else:
                            self.quad_b += 1
                            #switches indicator colour to light
                            self.change_indicator_colour(2,"light")
                    
                    #launching projectile
                    if event.key == pygame.K_SPACE:
                        #launch projectile
                        projectile_motion = True
                        
            #switches all indicators back to dark
            #up control
            if K_UP_TRI == 0:
                self.change_indicator_colour(1,"dark")
            else:
                K_UP_TRI -= 1
            #up control
            if K_DOWN_TRI == 0:
                self.change_indicator_colour(4,"dark")
            else:
                K_DOWN_TRI -= 1
            #up control
            if K_LEFT_TRI == 0:
                self.change_indicator_colour(3,"dark")
            else:
                K_LEFT_TRI -= 1
            #up control
            if K_RIGHT_TRI == 0:
                self.change_indicator_colour(2,"dark")
            else:
                K_RIGHT_TRI -= 1

#Menu Class
class Menu():
    #init
    def __init__(self):
        #importing pygame locally
        import pygame
        self.pygame = pygame

        #imports save module and button module locally
        import Save_Module
        self.save = Save_Module.Save_Game() #creates Save_Game instance
        import Button_Module
        self.Button_Module = Button_Module
        
        #makes game display
        self.screen_size = (1100,700)
        self.gameDisplay = self._create_display()

        #game display sizes
        self.s_width, self.s_height = self.pygame.display.Info().current_w, self.pygame.display.Info().current_h

        #array holding each button position
        self.button_positions = ()

        #creates buttons
        self._create_buttons()

        #variable to denote the current screen
        self.current_screen = 1

        #variable to hold the surface text of the points and level
        self.p_s_surface = 0

        #lose image creation
        self.loseImage = self._load_image("Lose.png")
        self.loseRect = self.loseImage.get_rect()
        self.loseRect.centerx, self.loseRect.centery = 550,200

        #title image creation
        self.titleImage = self._load_image("Title.png")
        self.titleRect = self.titleImage.get_rect()
        self.titleRect.centerx, self.titleRect.centery = 580,200
        #display image array
        self.display_images = [0,self.titleImage,self.titleImage,self.loseImage]
        self.display_image_rect = [0,self.titleRect,self.titleRect,self.loseRect]
        self.currentImage = self.titleImage #holds current image to be displayed
        self.current_image_rect = self.titleRect
        
    #private method to get the image for the projectile surface
    def _load_image(self,filename):
        #loads file, if fails to load game is quit after displaying an error
        try:
            image = self.pygame.image.load(filename)
        except ImportError:
            print("Error: File '"+filename+"' is not present")
            quit()
        #returning image
        return(image)

    #creates buttons
    def _create_buttons(self):
        #creates pos for buttons
        l_button_pos = (200,400)
        r_button_pos = (700,400)
        #colours for buttons
        d_green = (54,196,54)
        l_green = (58,216,58)
        d_red = (232, 48, 60)
        l_red = (252, 67, 67)
        #play button
        self.play_button = self.Button_Module.Button(self.gameDisplay,"Play",l_button_pos,d_green,l_green)
        #exit button
        self.exit_button = self.Button_Module.Button(self.gameDisplay,"Exit",r_button_pos,d_red,l_red)
        #new_game button
        self.new_button = self.Button_Module.Button(self.gameDisplay,"New Game",l_button_pos,d_green,l_green)
        #load_game button
        self.load_button = self.Button_Module.Button(self.gameDisplay,"Load Game",r_button_pos,d_green,l_green)
        #menu button
        self.menu_button = self.Button_Module.Button(self.gameDisplay,"Main Menu",l_button_pos,d_green,l_green)
        #creates buttons arrays
        self.screen_1 = [self.play_button,self.exit_button]
        self.screen_2 = [self.new_button,self.load_button]
        self.screen_3 = [self.menu_button,self.exit_button]
        self.screens = [0,self.screen_1,self.screen_2,self.screen_3]
        #array with all buttons
        self.buttons = [self.play_button,self.exit_button,self.new_button,self.load_button,self.menu_button]

    #handle actions for each button
    def handle_action(self,action_index):
        #if play button pressed
        if action_index == 0:
            self.set_screen(2)
        #if exit button pressed
        elif action_index == 1:
            self.quit_game()
        #if new button pressed
        elif action_index == 2:
            self.new_game()
        #if load button pressed
        elif action_index == 3:
            self.load_game()
        elif action_index == 4:
            self.set_screen(1)
            
    #switches between screens
    def set_screen(self,screen_number):
        #sets the current_screen attribute
        self.current_screen = screen_number
        #sets current display images
        self.currentImage = self.display_images[screen_number]
        self.current_image_rect = self.display_image_rect[screen_number]
        #loops through buttons on screen
        for x in self.screens[screen_number]:
            #special case for load game text
            if x.get_text() != "Load Game":
                x.set_on_screen(True) 
            #if file for load is present 
            elif self.save.is_file_present() == True:
                x.set_on_screen(True) 
            #otherwise dont show
            else:
                x.set_on_screen(False)
            #loop through other buttons
            for y in self.buttons:
                #if button not on screen
                if y not in self.screens[screen_number]:
                    y.set_on_screen(False)

    #displays buttons
    def display_buttons(self):
        #loop through buttons
        for x in self.buttons:
            x.display() #displays

    #handles hovering over buttons
    def hover_handle(self):
        for x in self.buttons:
            x.is_hover()
    
    #creates gameDisplay
    def _create_display(self):
        #make screen
        gameDisplay = self.pygame.display.set_mode(self.screen_size)
        return(gameDisplay)
                                                     
    #draws gameDisplay
    def draw_display(self):
        #fill
        self.gameDisplay.fill((34,161,235))
        #creates green box
        self.pygame.draw.rect(self.gameDisplay, (26,137,14),[0, ((self.s_height/4)*3), (self.s_width), (self.s_height/4)],0) # creates rect for x

    #draws title
    def draw_images(self):
        #draws image
        self.gameDisplay.blit(self.currentImage, self.current_image_rect)
    
    #starts a loaded game from save function
    def load_game(self):
        #preparing values from save
        points, level = self.save.load()
        loaded = True
        #instance of game
        game = Game(self.gameDisplay,points,level,loaded)
        self.set_screen(1) #sets screen to main menu
        points,level,save_bool = game.run_game() #runs game and waits for return of boolean with save data
        if save_bool == True:
            self.save.save(points,level)
        else:
            self.create_display_lose(points,level)
            self.set_screen(3)
            #deletes file
            self.save.delete()
    
    #starts a new game
    def new_game(self):
        #creates game instance
        game = Game(self.gameDisplay)
        self.set_screen(1)
        points,level,save_bool = game.run_game()
        if save_bool == True:
            self.save.save(points,level)
        else:
            self.create_display_lose(points,level)
            self.set_screen(3)
            #deletes file
            self.save.delete()
    
    #qutis the game
    def quit_game(self):
        self.pygame.quit()
        quit()

    #displays the score and level on the lose screen
    def create_display_lose(self,points,level):
        #creates text to be displayed to the user
        points_text = ("Points: ")
        points_val = str(points)
        level_text = ("Level: ")
        level_val = str(level)
        #getting font
        font_size = 40 #sets font size
        pygame.font.init() #init font module
        font_name = "calibri" #names font used
        myFont = pygame.font.SysFont(font_name,font_size) #creates font itself
        #renders text to create text_surface
        text_colour = (0,0,0)
        level_points_colour = (239, 26, 26)
        #creates text surfaces
        points_text_surface = myFont.render(points_text,True,text_colour)
        points_val_surface = myFont.render(points_val,True,level_points_colour)
        level_text_surface = myFont.render(level_text,True,text_colour)
        level_val_surface = myFont.render(level_val,True,level_points_colour)
        #creates rects from surfaces
        points_text_rect = points_text_surface.get_rect() 
        points_val_rect = points_val_surface.get_rect()
        level_text_rect = level_text_surface.get_rect() 
        level_val_rect = level_val_surface.get_rect()
        #creates surface to house the two other surfaces
        blitting_surface = pygame.Surface((max(points_text_rect.w+points_val_rect.w,level_text_rect.w+level_val_rect.w),(points_text_rect.h+level_text_rect.h)))
        #fills surface with correct colour
        blitting_surface.fill((34,161,235))
        #blits the two surfaces onto surface
        blitting_surface.blit(points_text_surface,(0,0))
        blitting_surface.blit(points_val_surface,(points_text_rect.w,0))
        blitting_surface.blit(level_text_surface,(14,points_text_rect.h))
        blitting_surface.blit(level_val_surface,(14+level_text_rect.w,points_text_rect.h)) #+14 to ensure that the colons line up
        #saves blitting surface as self
        self.p_s_surface = blitting_surface

    #displays the points and level reached by the user after they lose
    def display_lose(self):
        #creates rect as location to blit object
        display_rect = self.p_s_surface.get_rect()
        display_rect.center = (550,350) #sets location for blitting
        #blits
        self.gameDisplay.blit(self.p_s_surface,display_rect)
    
    #main method, starts main menu
    def main_menu(self):
        #sets first screen
        self.set_screen(1)
        #creates menu loop
        menu_loop = True
        #sets fps with pygame clock
        clock = pygame.time.Clock()
        #starts loop
        while menu_loop:
            #setting fps
            clock.tick(100)
            #updates game surface
            self.pygame.display.flip()
            #draws game surface
            self.draw_display()
            #draws title
            self.draw_images()
            #displays buttons
            self.display_buttons()
            #handles the hover of the mouse
            self.hover_handle()
            #displays score and level if the player has lost the game
            if self.current_screen == 3:
                self.display_lose()
            #event handling
            for event in self.pygame.event.get():
                #if quit
                if event.type == self.pygame.QUIT:
                    self.pygame.quit()
                    quit()
                #if keyboard quit
                if event.type == self.pygame.KEYDOWN:
                    #if key is escape
                    if event.key == self.pygame.K_ESCAPE:
                        self.pygame.quit()
                        quit()
                #if mouse pressed
                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    #sets button pressed to 0
                    button_pressed = 0
                    #find which button pressed
                    for x in self.buttons:
                        #if mouse over button
                        if x.is_hover() == True:
                            button_pressed = x                            
                    #action number is index of action in array
                    if button_pressed != 0:
                        action_number = self.buttons.index(button_pressed)
                        #call handle_action
                        self.handle_action(action_number)
                    else:
                        pass
    
menu = Menu()
menu.main_menu()
