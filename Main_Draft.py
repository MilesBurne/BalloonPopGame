#main draft 5 by Miles Burne 19/3/19
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
    def __init__(self,screen_dimensions,points=0,level=1,from_save=False):
        #getting dimensions for screen
        self.screen_dimensions = screen_dimensions
        self.s_width, self.s_height = screen_dimensions[0], screen_dimensions[1]
        self.gameDisplay = 0 #this will hold the screen surface
        self.points = points
        self.level = level
        #references to objects
        self.Target_List = []
        self.Projectile = 0
        self.Quadratic = 0
        self.Crate = 0
        self.Wall = 0
        self.Indicators = []
        #default values for the equation
        self.default_a = -0.1
        self.default_b = 80
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
        #make screen
        self.gameDisplay = pygame.display.set_mode((self.s_width, self.s_height))
        
        #fill
        self.gameDisplay.fill((34,161,235))

        #axes creation
        #y_list = [(0,0),(0,s_height)]
        #x_list = [(0,((s_height/4)*3)),(s_width,((s_height/4)*3))]

        #axes initialisation
        #pygame.draw.lines(screen, (255,255,255), False, y_list, 2) # y
        pygame.draw.rect(self.gameDisplay, (26,137,14),[0, ((self.s_height/4)*3), (self.s_width), (self.s_height/4)],0) # creates rect for x

    #draws indicators to screen
    def draw_indicator(self):
        #if indicators have not been created create them
        if len(self.Indicators) == 0:
            #calls create indicators function
            self.create_indicators()
        for x in self.Indicators:
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
        indicatorTL = Indicator(self.gameDisplay,(indicatorTL_x,indicatorTL_y),(232, 48, 60),(26,137,14),light_colour=(252, 67, 67))
        #indicator2
        indicatorTR_y = target_y - (self.quad_text_height)/2 - 25
        indicatorTR_x = target_x + 45
        indicatorTR = Indicator(self.gameDisplay,(indicatorTR_x,indicatorTR_y),(52, 61, 229),(26,137,14),light_colour=(88,95,221))
        #indicator3
        indicatorBL_y = target_y + (self.quad_text_height)/2 + 25
        indicatorBL_x = target_x + 45
        indicatorBL = Indicator(self.gameDisplay,(indicatorBL_x,indicatorBL_y),(52, 61, 229),(26,137,14),point_down=True,light_colour=(88,95,221))
        #indicator4
        indicatorBR_y = target_y + (self.quad_text_height)/2 + 25
        indicatorBR_x = target_x - 140
        indicatorBR = Indicator(self.gameDisplay,(indicatorBR_x,indicatorBR_y),(232, 48, 60),(26,137,14),point_down=True,light_colour=(252, 67, 67))
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
            #LOSE??
            collided = True
        else:
            for x in self.Target_List:
                #checking collisons using target
                collision_bool = x.detect_collision(proj_rect)
                #if has collided
                if collision_bool == True:
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
        #hides quadratic if level correct
        if level % 5 != 0:
            self.crate_level = False
            self.quad_a = self.default_a
            self.quad_b = self.default_b
        if level >= self.quadratic_hide_level:
            self.show_quadratic_toggle = False
        if level in self.add_target_level:
            #moves start position for next target
            self.next_target_start -= 2/16
            target_start = ((self.screen_dimensions[0]*(self.next_target_start)),self.default_target_start[1])
            #creates new target
            self.Target_List.append(Target(self.gameDisplay, target_start))
        #makes each target difficulty higher
        for x in self.Target_List:
            x.collide()   
        if level%5 == 0:
            #print("go")
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
                             

    #method to move each target in Target_List
    def target_move(self):
        #cycles through targets
        for x in self.Target_List:
            #moves target
            x.move()

    #returns points and level if the game is quit before loss
    def save_game(self):
        return(self.points,self.level)
        
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
            #print(self.Quadratic.get_a())
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
            #collision detection
            if projectile_motion == True:
                collision = self.detect_collision()
                if collision == True: #therefore points have increased and collision has happened
                    projectile_motion = False
                #in case of no collision
                else:
                    projectile_motion = self.Projectile.move(projectile_motion) #projectile stops when movement stops
                    if projectile_motion == False:
                        self.points -= 50
            else:
                projectile_motion = self.Projectile.move(projectile_motion) #projectile stops when movement stops
            #handling crate display, has to be after collision detect so self.relative_coords exist
            self.Crate.display()
            self.Wall.display()
            if self.level % 5 == 0:
                self.relative_coord_display()
            '''
            #handling held keys
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT] == True and projectile_motion == False:
                if key_checker == 0:
                    key_checker = 0
                    self.quad_b -= 1
            elif keys_pressed[pygame.K_RIGHT] == True and projectile_motion == False:
                if key_checker == 0:
                    key_checker = 0
                    self.quad_b += 1
            elif keys_pressed[pygame.K_UP] == True and projectile_motion == False:
                if key_checker == 0 and self.level%5 != 0:
                    key_checker = 0
                    self.quad_a += 0.01
            elif keys_pressed[pygame.K_DOWN] == True and projectile_motion == False:
                if key_checker == 0 and self.level%5 != 0:
                    print("pressed")
                    key_checker = 0
                    self.quad_a -= 0.01
            if self.quad_a > 0:
                        self.quad_a = 0
            #key_checker to ensure that the values dont update too fast
            if key_checker < 10:
                key_checker += 0
            '''
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

                    


game = Game((1100,700))
game.run_game()
pygame.quit()

