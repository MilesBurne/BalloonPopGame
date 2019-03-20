#main draft 3 by Miles Burne 19/3/19
#imports
import pygame
#custom imports
from Quadratic_Module import * 
from Projectile_Module import *
from Target_Module import *

#game class to handle the running of the game
class Game():
    #init, takes screen dimensions as (width,height), and points and level
    def __init__(self,screen_dimensions,points=0,level=1):
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
        #variables to control difficulty
        self.quadratic_hide_level = 5 #game hides quadratic on this level
        self.show_quadratic_toggle = True
        self.add_target_level = [10,20,30,40,50] #game adds a balloon on these levels
        self.current_target_level = 1
        #creates default starting x position for target
        self.default_target_start = ((self.screen_dimensions[0]/16*15),(self.screen_dimensions[1]/4*3))
        self.next_target_start = 15/16
        
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

    #this displays the quadratic equation to the screen
    def show_quadratic(self):
        #getting a and b and multiplying by ten to make the program more readable
        a = self.Quadratic.get_a()*100
        b = int(self.Quadratic.get_b()*100)
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
                print(hit_list)
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


    #method to increase the difficulty of the game
    def increase_difficulty(self):
        #hides quadratic if level correct
        if self.level >= self.quadratic_hide_level:
            self.show_quadratic_toggle = False
        if self.level in self.add_target_level:
            self.next_target_start -= 2/16
            target_start = ((self.screen_dimensions[0]*(self.next_target_start)),self.default_target_start[1])
            self.Target_List.append(Target(self.gameDisplay, target_start))
        for x in self.Target_List:
            x.collide()                        
            

    #method to move each target in Target_List
    def target_move(self):
        #cycles through targets
        for x in self.Target_List:
            #moves target
            x.move()
        
    #main portion of the game, acts as a main loop
    def run_game(self):
        #init pygame
        pygame.init()
        #draws the game
        self.draw_game()
        #adds a name for the window
        pygame.display.set_caption("Balloon Pop")
        #creates default a and b values 
        quad_a = -0.1
        quad_b = 80
        #creates start positions for object projectile
        projectile_start = (0,(self.screen_dimensions[1]/4*3))
        #instantiate quadratic object by calling make_quadratic function
        self.make_quadratic(quad_a,quad_b)
        #instantiate balloon object
        self.Target_List.append(Target(self.gameDisplay, self.default_target_start))
        self.Projectile = Projectile(self.gameDisplay, projectile_start,self.Quadratic)
        #controls movement of the projectile
        projectile_motion = False
        #creates the main game loop
        running = True
        while running:
            #updates screen after every gameloop
            pygame.display.flip()
            #draws the main screen to prevent overlaps
            self.draw_game()
            #updates quadratic with new values using the make_quadratic function and an optional value
            self.make_quadratic(quad_a,quad_b)
            #draws the quadratic path and equation for the first time, shows quadratic if toggle is true
            if self.show_quadratic_toggle == True:
                self.draw_quadratic()
            self.show_quadratic()
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
                    if event.key == pygame.K_UP and projectile_motion == False:
                        quad_a += 0.01
                    if event.key == pygame.K_DOWN and projectile_motion == False:
                        quad_a -= 0.01
                    #making sure that A is in a valid range, only needs to change when A is changed
                    if quad_a > 0:
                        quad_a = 0
                    
                    #changing B
                    if event.key == pygame.K_LEFT and projectile_motion == False:
                        quad_b -= 1
                    if event.key == pygame.K_RIGHT and projectile_motion == False:
                        quad_b += 1
                    
                    #launching projectile
                    if event.key == pygame.K_SPACE:
                        #launch projectile
                        projectile_motion = True


game = Game((1100,700))
game.run_game()
