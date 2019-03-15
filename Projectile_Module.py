#Projectile Module by Miles Burne 13/03/19

#projectile class, takes the size for the projectile
class Projectile():
    #init, takes the surface of the screen, the start position, and the Quadratic class, as well as an optional input of size
    def __init__(self, surface, pos, Quadratic, size=15):
        #imports pygame locally
        import pygame
        self.pygame = pygame
        
        #gets the reference for the quadratic class, which updates the equation from the players input
        self.Quadratic = Quadratic
        
        #adding total game surface which will display image
        self.gameDisplay = surface

        #getting size of screen
        self.display_w, self.display_h = self.pygame.display.Info().current_w, self.pygame.display.Info().current_h
        
        #grabbing the image to create first surface
        self.image = self._load_image()

        #resizing image to a managable scale
        self.image = self.pygame.transform.smoothscale(self.image,(size,size))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], (-1*self.Quadratic.get_y(pos[0]+10))+((self.display_h/4)*3) #changing position of rect to blit object
        self.reset_pos = self.rect.topleft #adding the position the image will reset to

        #used to control when the projectile is moving
        self.moving = False
        
    #first move to display ball, blits the ball at position 1
    def first_move(self):
        self.gameDisplay.blit(self.image, self.reset_pos)

        
    #private method to get the image for the projectile surface
    def _load_image(self):
        #filename for use in loading
        filename = "Cannonball.png"
        #loads file, if fails to load game is quit after displaying an error
        try:
            image = self.pygame.image.load(filename)
        except ImportError:
            print("Error: File '"+filename+"' is not present")
            quit()
        #returning image
        return(image)

    #returns current rect
    def get_rect(self):
        return(self.rect)

    #resets the projectile to its starting position
    def reset(self):
        #resets the projectile to position 1
        self.gameDisplay.blit(self.image, self.reset_pos)
        #resetting the rect
        self.rect.centerx, self.rect.centery = self.reset_pos[0], self.reset_pos[1]
        self.moving = False

    #move function, uses the quadratic from self.quadratic
    def move(self,moving=False):
        self.moving = moving
        #used to return True if object has moved
        has_moved = False
        #controls if the projectile should be moving or not
        if self.moving == True:

            #checking if projectile at end of screen or below minimum boundary
            if self.rect[0]+((self.rect[3]/4)*3) >= self.display_w or self.rect[1] >= (self.display_h*3/4)+(self.rect[3]/2):
                self.reset()
            else:
                #making new positions based of of current position
                new_x = self.rect.centerx+10
                new_y = (-1*self.Quadratic.get_y(self.rect.centerx+10))+((self.display_h/4)*3) #as in pygame top of screen is y = 0, values need to be changed
                #changes rect, used for detecting collisions
                self.rect.centerx = new_x
                self.rect.centery = new_y
                #blitting image
                self.gameDisplay.blit(self.image, (self.rect.topleft))
                #object has moved therefore True
                has_moved = True
            return(has_moved)
        #if shouldnt be moving
        else:
            #blits projectile where it should start
            self.gameDisplay.blit(self.image, self.reset_pos)
            return(has_moved)
        
        #method to return the data of the projectile
        def get_data(self):
            return(self.speed,self.variance,self.size)
        
        #method to change the data of the projectile
        def change_data(self, speed, variance, size):
            self.speed = speed
            self.variance = variance
            self.size = size
         
            
