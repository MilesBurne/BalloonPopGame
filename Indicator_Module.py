#Indicator_Module
#class to act as a light up button above and below changing values
class Indicator():
    #init, takes the position for the middle of the button, the colour, and a value to indicate the direction of the triangle(u,d,l,r), and the light colour of the triangle
    def __init__(self,gameDisplay,pos,colour,background_colour,direction="u",light_colour=0):
        #imports pygame locally
        import pygame
        self.pygame = pygame
        
        #creating game display
        self.gameDisplay = gameDisplay
        
        #getting size of screen
        self.display_w, self.display_h = self.pygame.display.Info().current_w, self.pygame.display.Info().current_h

        #variable to control whether the triangle is displayed or not
        self.on_screen = True

        #controls where the traingle points to
        self.direction = direction
        
        #position for triangle
        self.position = pos

        #colour of triangle and background
        self.background_colour = background_colour
        self.colour = colour
        if light_colour == 0:
            light_colour = (min(colour[0]+20,255),min(colour[1]+20,255),min(colour[2]+20,255))
        self.light_colour = light_colour

        #sets the 'shade' out colour
        self.shade_colour_dark = (144,144,144)#grey
        self.shade_colour_light = (144,144,144)#grey

        #sets the default colours
        self.default_dark_colour = colour
        self.default_light_colour = light_colour

        #controls whether the current colour is light or not
        self.current_light = False

        #sizes for the triangle
        self.u_d_size = (50,50)
        self.l_r_size = (50,50)

        #creates surface to be blit, and the tri_point_list
        self.tri_point_list = 0
        self.blitting_surface = 0
        self._create_rect()

    #creates the rect
    def _create_rect(self):
        #changing size based on direction
        if self.direction == "u" or self.direction == "d":
            #creating surface
            self.blitting_surface = self.pygame.Surface(self.u_d_size)
            #gets rect of surface
            surface_rect = self.blitting_surface.get_rect()
        else:
            #creating surface
            self.blitting_surface = self.pygame.Surface(self.l_r_size)
            #gets rect of surface
            surface_rect = self.blitting_surface.get_rect()
        #if triangle should point up
        if self.direction == "u":
            #creating the triangle pointlist for use in draw function
            self.tri_point_list = (surface_rect.bottomleft,surface_rect.bottomright,surface_rect.midtop)
        #if should point down
        elif self.direction == "d":
            #creating the triangle pointlist for use in draw function
            self.tri_point_list = (surface_rect.topleft,surface_rect.topright,surface_rect.midbottom)
        #if points left
        elif self.direction == "l":
            #creating the triangle pointlist for use in draw function
            self.tri_point_list = (surface_rect.topright,surface_rect.bottomright,surface_rect.midleft)
        #if points right
        elif self.direction == "r":
            #creating the triangle pointlist for use in draw function
            self.tri_point_list = (surface_rect.topleft,surface_rect.bottomleft,surface_rect.midrigh