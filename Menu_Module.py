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
        #creates buttons arrays
        self.screen_1 = [self.play_button,self.exit_button]
        self.screen_2 = [self.new_button,self.load_button]
        self.screens = [0,self.screen_1,self.screen_2]
        #array with all buttons
        self.buttons = [self.play_button,self.exit_button,self.new_button,self.load_button]

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
            
    #switches between screens
    def set_screen(self,screen_number):
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
    
    #starts a loaded game from save function
    def load_game(self):
        points, level = self.save.load()
        loaded = True
    
    #starts a new game
    def new_game(self):
        pass
    
    #qutis the game
    def quit_game():
        self.pygame.quit()
        quit()

    #displays main title
        
    #main method, starts main menu
    def main_menu(self):
        #sets first screen
        self.set_screen(1)
        #creates menu loop
        menu_loop = True
        #starts loop
        while menu_loop:
            self.pygame.display.flip()
            #draws game board
            self.draw_display()
            #displays buttons
            self.display_buttons()
            #handles the hover of the mouse
            self.hover_handle()
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
        
        
        
    
