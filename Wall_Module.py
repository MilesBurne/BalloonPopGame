#wall module
class Wall():
    #init
    def __init__(self,gameDisplay):
        #imports pygame locally
        import pygame
        self.pygame = pygame
        
        #creating game display
        self.gameDisplay = gameDisplay
        
        #getting size of screen
        self.display_w, self.display_h = self.pygame.display.Info().current_w, self.pygame.display.Info().current_h

        #pos for the wall
        self.wall_pos = (int(self.display_w*1/3),int(self.display_h/4*3))

        #variable to control whether the wall is displayed or not
        self.on_screen = False

        #getting the image for the target
        self.image = self._load_image()

        #size for the object
        self.size = (50,200)
        
        #resizing image to a managable scale
        self.image = self.pygame.transform.smoothscale(self.image,(self.size))
        self.rect = self.image.get_rect()

        #creating location of wall
        self.rect.midbottom = self.wall_pos

    #loads the image cleanly
    def _load_image(self):
        #filename for use in loading
        filename = "wall.jpg"
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
            return(True) #returns True if collision is detected
        else:
            return(False)

    #changes on_screen to False or True
    def set_visible(self,boolean):
        self.on_screen = boolean

     #displays the wall to the screen
    def display(self):
        #doesn't blit if on_screen is False
        if self.on_screen == False:
            return(0)
        else:
            #blits rect to screen
            self.gameDisplay.blit(self.image, self.rect)

    #returns height of wall
    def get_height(self):
        return(self.rect[3])
