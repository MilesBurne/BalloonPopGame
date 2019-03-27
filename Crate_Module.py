#crate class
class Crate():
    #init
    def __init__(self, surface):
        #imports pygame and random locally
        import pygame
        self.pygame = pygame
        import random
        self.random = random 

        #getting the image for the target
        self.image = self._load_image()

        #size for the object
        self.size = (100,100)
        
        #resizing image to a managable scale
        self.image = self.pygame.transform.smoothscale(self.image,(self.size))
        self.rect = self.image.get_rect()

        #adding total game surface which will display image
        self.gameDisplay = surface
        
        #getting size of screen
        self.display_w, self.display_h = self.pygame.display.Info().current_w, self.pygame.display.Info().current_h

        #these are the coords displayed to the screen, relative to cannon launch
        self.relative_coords = (0,0)

        #variable to control whether the crate is displayed or not
        self.on_screen = False

    #loads the image cleanly
    def _load_image(self):
        #filename for use in loading
        filename = "box.png"
        #loads file, if fails to load game is quit after displaying an error
        try:
            image = self.pygame.image.load(filename)
        except ImportError:
            print("Error: File '"+filename+"' is not present")
            quit()
        #returning image
        return(image)

    #tests for collisons with other rects, takes the rect and returns bool
    def detect_collision(self, collide_rect):
        #cannot collide if not visible
        if self.on_screen == False:
            return(False)
        #tests if target rect has collided with another rect
        if self.rect.colliderect(collide_rect) == True:
            self.on_screen = False
            return(True) #returns True if collision is detected
        else:
            return(False)

    #creates the blocks random location relative in a range, creates modified coords relative to cannon for this
    def create_new_location(self): #coords will be mapped from rect.bottom
        #creating the y value, and the maximum and minimum x values, all values are rounded with int to allow coord use
        y_value = int((self.display_h*3/4) + 0) # game floor starts at 3/4 * display height
        minimum_x_value = int((self.display_w*1/3) + self.size[0]/2) #wall starts at 1/3 * display width and coords are for centre of block
        maximum_x_value = int((self.display_w) - self.size[1]/2) #end of screen as coords are mapped from block centre
        #creates x value with random module
        x_value = self.random.randint(minimum_x_value,maximum_x_value)
        #creates actual coords in form of rect
        self.rect.midbottom = (x_value, y_value)
        #creates relative coords to cannon
        relative_x = x_value/100
        relative_y = 0
        self.relative_coords = (relative_x,relative_y)
        #makes sure display method knows that crate is on screen
        self.on_screen = True

    
    #returns the relative coords of the crate
    def get_relative_coords(self):
        return(self.relative_coords)

    #returns actual location
    def get_actual_coords(self):
        return(self.rect)

    #displays the crate to the screen, if the crate has been hit, 
    def display(self):
        #doesn't blit if on_screen is False
        if self.on_screen == False:
            return(0)
        else:
            #blits rect to screen
            self.gameDisplay.blit(self.image, self.rect)

    #changes on_screen to False or True
    def set_visible(self,boolean):
        self.on_screen = boolean
            
            
        
        
        



        
        
