#Indicator_Module
#class to act as a light up button above and below changing values
class Indicator():
    #init, takes the position for the middle of the button, the colour, and a boolean for whether it points down, and the light colour of the triangle
    def __init__(self,gameDisplay,pos,colour,background_colour,point_down=False,light_colour=0):
        #imports pygame locally
        import pygame
        self.pygame = pygame
        
        #creating game display
        self.gameDisplay = gameDisplay
        
        #getting size of screen
        self.display_w, self.display_h = self.pygame.display.Info().current_w, self.pygame.display.Info().current_h

        #variable to control whether the triangle is displayed or not
        self.on_screen = True

        #controls whether the traingle points down or not
        self.point_down = point_down
        
        #position for triangle
        self.position = pos

        #colour of triangle and background
        self.background_colour = background_colour
        self.colour = colour
        if light_colour == 0:
            light_colour = (min(colour[0]+20,255),min(colour[1]+20,255),min(colour[2]+20,255))
        self.light_colour = light_colour

        #controls whether the current colour is light or not
        self.current_light = False

        #size for the triangle
        self.size = (70,50)

        #creates surface to be blit, and the tri_point_list
        self.tri_point_list = 0
        self.blitting_surface = 0
        self._create_rect()

    #creates the rect
    def _create_rect(self):       
        #creating surface
        self.blitting_surface = self.pygame.Surface(self.size)
        #gets rect of surface
        surface_rect = self.blitting_surface.get_rect()
        #if triangle should point up
        if self.point_down == False:
            #creating the triangle pointlist for use in draw function
            self.tri_point_list = (surface_rect.bottomleft,surface_rect.bottomright,surface_rect.midtop)
        #if should point down
        else:
            #creating the triangle pointlist for use in draw function
            self.tri_point_list = (surface_rect.topleft,surface_rect.topright,surface_rect.midbottom)


    #hides or shows the surface
    def set_visible(self, boolean):
        self.on_screen = boolean

    #draws the triangle to the screen
    def draw_to_screen(self):
        #if on screen
        if self.on_screen == True:
            #if colour meant to be light
            if self.current_light == True:
                used_colour = self.light_colour
            #if colour dark
            else:
                used_colour = self.colour
            #filling surface with background colour
            self.blitting_surface.fill(self.background_colour)
            #drawing triangle to surface
            self.pygame.draw.polygon(self.blitting_surface,used_colour,self.tri_point_list) #width = 0 therefore closed
            #drawing to game surface
            temp_rect = self.blitting_surface.get_rect()
            temp_rect.center = self.position
            self.gameDisplay.blit(self.blitting_surface,temp_rect)
        else:
            pass

    #sets the colour to light or dark
    def set_colour(self,light_colour=False):
        self.current_light = light_colour
        
            
