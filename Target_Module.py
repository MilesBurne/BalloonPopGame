#target class
class Target():
    import pygame
    #init, takes input of the speed, variance and size and position to load to begin with
    def __init__(self, surface, pos, speed=0.2, variance=0.2, size=150):
        #imports pygame and random locally
        import pygame
        self.pygame = pygame
        import random
        self.random = random
        #getting the image for the target
        self.image = self._load_image()
        
        #resizing image to a managable scale
        self.image = self.pygame.transform.smoothscale(self.image,(size,size))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = pos[0], pos[1] #changing position of rect to blit object
        self.reset_rect = pygame.Rect(self.rect.x,self.rect.y,self.rect.w,self.rect.h) #adding the position the image will reset to, create this rect explicitly as otherwise python references instead    

        #adding total game surface which will display image
        self.gameDisplay = surface
        
        #getting size of screen
        self.display_w, self.display_h = self.pygame.display.Info().current_w, self.pygame.display.Info().current_h
        
        #these variables define the changing features of the target's movement which change as the level increases
        self.speed = speed #speed of balloon movement
        self.variance = variance #side to side motion of balloon
        self.size = size #size of balloon 
        self._left_toggle = [False, False, True, True, True, False] #used to control whether the target goes left or right on next motion.
        self._left_toggle_count = 0

        #variable to toggle if balloon is hit
        self.target_hit = True
        
    #method to get if balloon hit
    def is_target_hit(self):
        return(self.target_hit)
    
    #method to change if balloon hit
    def set_target_hit(self,hit):
        self.target_hit = hit
        
    #private method used on collision with another rect
    def collide(self):
        #defines the values each variable will change by
        speed_change = 0.1
        variance_change = 0.1
        size_change = -10
        size_minimum = 10
        max_speed = 6.0
        #picks a random number 
        random_difficult = self.random.randint(0,2)
        #changes speed
        if random_difficult == 0 and self.speed < max_speed:#changes speed
            self.speed += speed_change
        elif random_difficult == 1:#changes variance
            self.variance += variance_change
        elif random_difficult == 2 and self.size > size_minimum:#changes size if size is greater than a minimum
            self.size += size_change
            self.image = self.pygame.transform.smoothscale(self.image,(self.size,self.size))
            self.rect = self.image.get_rect()
            self.rect.centerx, self.rect.bottom = self.reset_rect[0], self.reset_rect[1] #changing position of rect to blit object
            print(self.size)
        else: #otherwise size is less than or equal to minimum therefore:
            self.variance += variance_change
        #changes the size of rect to ensure that collison still works
        self.rect.w,self.rect.h = self.image.get_rect().w,self.image.get_rect().h

    #blits the object for the first time 
    def move_first(self):
        self.gameDisplay.blit(self.image, (self.rect[0],self.rect[1]))
    
    #returns the rect of the target
    def get_rect(self):
        return(self.rect)
    
    #loads the image cleanly
    def _load_image(self):
        #filename for use in loading
        filename = "BalloonRed.png"
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
        #tests if target rect has collided with another rect
        if self.rect.colliderect(collide_rect) == True:
            self.target_hit = True
            return(True) #returns True if collision is detected
        else:
            return(False)

    #used to reset the balloon to its starting point
    def reset(self):
        #resets the balloon to position 1
        self.gameDisplay.blit(self.image, self.reset_rect)
        #resetting the rect
        self.rect = self.pygame.Rect(self.reset_rect.x,self.reset_rect.y,self.reset_rect.w,self.reset_rect.h) #adding the position the image will reset to, create this rect explicitly as otherwise python references instead       
    
    #method for the movement of the target
    def move(self):
        #used to return True if object has moved
        has_moved = False
        #checking if balloon is not above the current screen height plus half the object height 
        if self.rect[1] <= -1*(0.8*self.rect[3]):
            self.reset()
        #otherwise balloon is still below screen top, and therefore movement can happen
        else:
            #flipping the variance sign to make the target move left and right
            if self._left_toggle[self._left_toggle_count]:
                used_variance = self.variance
            else:
                used_variance = (-1*self.variance)
            #checking that the count is less than the length
            if self._left_toggle_count == len(self._left_toggle)-1:
                self._left_toggle_count = 0
            else:
                self._left_toggle_count += 1
            #creating new positions using variance and speed
            new_x = int(round((self.rect[0]-((self.display_w/100)*used_variance))))
            new_y = int(self.rect[1]-((self.display_h/100)*self.speed))

            #changes rect, used for detecting collisions
            self.rect.x = new_x
            self.rect.y = new_y
            #creates new position for balloon
            new_pos = (new_x,new_y)
            #blitting image
            self.gameDisplay.blit(self.image, new_pos)
            #object has moved therefore True
            has_moved = True
        #return statement
        return(has_moved)
