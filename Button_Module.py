#button class
class Button():
    #init, takes display surface, button name,  pos, colour and light colour.
    def __init__(self,gameDisplay,display_name,pos,colour,light_colour):
        #importing pygame locally
        import pygame
        self.pygame = pygame
        
        #creating game display
        self.gameDisplay = gameDisplay

        #creating pos for button in form of rect
        size = (200,100)
        self.rect = pygame.Rect(pos,size)

        #colours
        self.dark_colour = colour
        self.light_colour = light_colour

        #toggle for whether button displayed or not
        self.on_screen = False

        #creates light and dark surfaces
        self.dark_surface,self.light_surface = self._create_button_surfaces(display_name)

        #toggle for whether display surface should be light or not
        self.light_surface_display = False

        


    #creates the button surfaces, light colour and dark colour
    def _create_button_surfaces(self,display_name):
        #creates text to go on each surface
        self.text = display_name
        #getting font
        font_size = 20 #sets font size
        self.pygame.font.init() #init font module
        font_name = "calibri" #names font used
        myFont = self.pygame.font.SysFont(font_name,font_size) #creates font itself
        #renders text to create text_surface
        text_colour = (0,0,0)
        button_text = myFont.render(self.text,True,text_colour)
        button_text_rect = button_text.get_rect() #gets rect of surface for blitting
        #colours loop
        colour_loop = [self.dark_colour,self.light_colour]
        button_surface_array = []
        for colour in colour_loop:
            button_surface = self.pygame.Surface((self.rect.w,self.rect.h)) #creates button surface from rect
            button_surface.fill(colour)
            button_text_rect.center = button_surface.get_rect().center #setting location for blitting
            button_surface.blit(button_text,button_text_rect) #blits text to button
            button_surface_array.append(button_surface)
        return(button_surface_array[0],button_surface_array[1]) #returns button surfaces
        
    #displays button surface
    def display(self):
        #if button on screen
        if self.on_screen == True:
            #checks if used button is light
            if self.light_surface_display == True:
                button_surface = self.light_surface
            #else dark button
            else:
                button_surface = self.dark_surface
            #blitting button using rect as location
            self.gameDisplay.blit(button_surface,self.rect)
        #otherwise do not display
        else:
            pass

    #checks if mouse is over button surface, returns bool
    def is_hover(self):
        #cannot be hovering over is button not on screen
        if self.on_screen == False:
            return(False)
        #if on screen
        else:
            #gets mouse coords
            mouse_pos = self.pygame.mouse.get_pos()
            #checking if mouse in range
            if (self.rect.left <= mouse_pos[0] <= self.rect.right) and (self.rect.top <= mouse_pos[1] <= self.rect.bottom):
                #then mouse in range
                self.light_surface_display = True
                return(True)
            else:
                #mouse NOT in range
                self.light_surface_display = False
                return(False)

    #changes whether button is currently displayed or not
    def set_on_screen(self,boolean):
        self.on_screen = boolean

    #returns text of button
    def get_text(self):
        return(self.text)
        
