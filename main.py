#!/usr/bin/env python3

import turtle, game, os, sys

class MainMenu(object):
    '''Main menu creates a 800 x 600 window to allow you to view the controls,
    change the grid size, start the game, and quit the game.'''

    current_screen = 'main'
    game_on = False

    def __init__(self):
        self.keyboard_bindings()

    def create_screen(self):
        '''Create medium sized main menu.'''
        self.current_screen == 'main'
        self.width, self.height = (800, 600)
        self.screen = turtle.Screen()
        self.screen.bgcolor('black')
        self.screen.bgpic('main_menu.gif')
        self.screen.setup(self.width, self.height, startx=None, starty=None)
        self.screen.title('TRON')
        self.screen.tracer(0)

    def set_cursor(self):
        """
        Controlled by cursor_up and cursor_down functions.
        Main: Start = 3, Controls = 2, Quit = 1
        Grid Size: Small = 1, Medium = 2, Large = 3
        Controls: None. Hides turtle. Only return key functions."""
        if self.current_screen == 'main':
            if self.pen.cursor_pos == 1:
                self.pen.setposition(-50, -130)
            elif self.pen.cursor_pos == 2:
                self.pen.setposition(-80, -15)
            else: # Position 3
                self.pen.setposition(-50, 95)
        elif self.current_screen == 'grid_size':
            if self.pen.cursor_pos == 1:
                self.pen.setposition(-310, -15)
            elif self.pen.cursor_pos == 2:
                self.pen.setposition(-75, -15)
            else: # Position 3
                self.pen.setposition(195, -15)
        else:
            pass

    def cursor_up(self):
        '''Increase cursor pos by 1.'''
        if self.pen.cursor_pos < 3:
            self.pen.cursor_pos += 1

    def cursor_down(self):
        '''Decrease cursor pos by 1.'''
        if self.pen.cursor_pos > 1:
            self.pen.cursor_pos -= 1

    def keyboard_bindings(self):
        '''Sets bindings depending on which screen is displayed.'''
        turtle.listen()
        if self.current_screen == 'main':
            turtle.onkeypress(self.cursor_up, 'Up')
            turtle.onkeypress(self.cursor_up, 'w')
            turtle.onkeypress(self.cursor_down, 'Down')
            turtle.onkeypress(self.cursor_down, 's')
        elif self.current_screen == 'grid_size':
            turtle.onkeypress(self.cursor_up, 'Right')
            turtle.onkeypress(self.cursor_up, 'd')
            turtle.onkeypress(self.cursor_down, 'Left')
            turtle.onkeypress(self.cursor_down, 'a')
        else:
            pass
        # Apply special function to return or space
        turtle.onkeypress(self.press_enter_or_space, 'Return')
        turtle.onkeypress(self.press_enter_or_space, 'space')

    def display_controls(self):
        '''Displays control screen. Nothing can be changed.'''
        self.current_screen = 'controls'
        self.pen.hideturtle()
        self.screen.bgpic('controls.gif')

    def display_main(self):
        '''Displays the main menu.'''
        self.current_screen = 'main'
        self.screen.bgpic('main_menu.gif')
        self.pen.showturtle()

    def display_grid_options(self):
        '''Displays grid size options, after selecting to start.'''
        self.pen.cursor_pos = 2
        self.current_screen = 'grid_size'
        self.screen.bgpic('grid_size.gif')

    def press_enter_or_space(self):
        '''Depending on the current screen, controls how the enter and space keys function'''
        if self.current_screen == 'main':
            if self.pen.cursor_pos == 3:
                self.display_grid_options()
            elif self.pen.cursor_pos == 2:
                self.display_controls()
            elif self.pen.cursor_pos == 1:
                if os.name == 'posix':
                    os.system('killall afplay')
                turtle.bye()
            else:
                pass

        elif self.current_screen == 'grid_size':
            if self.pen.cursor_pos == 1:
                width, height = (640, 480)
            elif self.pen.cursor_pos == 2:
                width, height = (800, 600)
            elif self.pen.cursor_pos == 3:
                width, height = (1024, 768)
            else:
                pass
            self.screen.clear()
            self.pen.clear()
            if os.name == 'posix':
                os.system('killall afplay')
            self.game_on = True
            # Start game
            self.start_game(width, height)
            # Game finishes and returns to menu
            self.current_screen = 'main'
            menu.start_menu()
        elif self.current_screen == 'controls':
            self.display_main()
        else:
            pass

    def start_game(self, width, height):
        '''Starts the game with grid size choice.'''
        gameObj = game.Game(width, height)
        gameObj.start_game()

    def start_menu(self):
        '''Main menu loop. Creates cursor, displays main menu, and plays bgm.'''
        self.create_screen()
        self.pen = turtle.Turtle()
        self.pen.shapesize(stretch_wid=3, stretch_len=3, outline=None)
        self.pen.cursor_pos = 3
        self.pen.pencolor('#40BBE3')
        self.pen.penup()
        self.game_on = False
        # Stop music when returning from game and restart main menu music
        if os.name == 'posix':
            os.system('killall afplay')
            os.system('afplay main_menu.m4a&')
        # Change cursor position based on keybindings
        while True:
            turtle.update()
            self.set_cursor()
            self.keyboard_bindings()

if __name__ == '__main__':
    if sys.version_info[0] < 3:
        raise SystemExit('Python 3 required!')
    menu = MainMenu()
    menu.start_menu()
