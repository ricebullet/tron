#!/usr/bin/env python3

import turtle, random, time, os, main

# Welcome to TRON! The object of the game is to stay alive the longest by not crashing into the walls
# or the opponent's trails. Game resets when either player crashes.
# Options: Grid size

class Game(object):
    '''Creates screen, draws border, creates all sprites, maps keys, draws score, and
    game loop runs.'''
    def __init__(self,width=None,height=None):
        self.width = width
        self.height = height
        self.create_screen()
        self.pen = turtle.Turtle()
        self.score_pen = turtle.Turtle()
        self.draw_border()
        self.player_creation()
        self.particle_creation()
        self.keyboard_bindings()
        self.state = 'game_on'
        self.draw_score()
        self.game_loop()

    def screen_size(self):
        '''Only used if script runs directly.'''
        choices = ['small', 'medium', 'large']
        size = ''
        while size not in choices:
            size = input('Grid size: (Small, Medium, Large) ').lower().strip()
            if size == 'small':
                return (640, 480)
            elif size == 'medium':
                return (800, 600)
            elif size == 'large':
                return (1024, 768)
            else:
                print('{} is not a valid size.'.format(size))

    def create_screen(self):
        '''If run directly, based on user choice from self.screen_size, screen is created
        Otherwise, screen is automatically created with arguments from main menu script.'''
        if not self.width or not self.height:
            self.width, self.height = self.screen_size()
        self.screen = turtle.Screen()
        self.screen.bgcolor('black')
        self.screen.setup(self.width, self.height, startx=None, starty=None)
        self.screen.title('TRON')
        self.screen.tracer(0)

    def draw_border(self):
        '''Border is drawn from the width and height, starting in upper
        right hand corner. Each side is 50 pixels from the screen.
         The border coordinates will be used for border detection as well.'''
        self.x_boundary = (self.width / 2) - 50
        self.y_boundary = (self.height / 2) - 50
        self.pen.color('blue')
        self.pen.penup()
        self.pen.setposition(self.x_boundary, self.y_boundary)
        self.pen.pendown()
        self.pen.pensize(3)
        self.pen.speed(0)
        self.pen.setheading(180) # Start drawing west
        # Square is drawn
        for side in range(4):
            # Vertical
            if side % 2:
                self.pen.forward(self.height - 100)
                self.pen.left(90)
            # Horizontal
            else:
                self.pen.forward(self.width - 100)
                self.pen.left(90)
        self.pen.penup()
        self.pen.hideturtle()

    def boundary_check(self, player):
        '''Checks if light cycle is out of bounds using border coord'''
        if ((player.xcor() < (-self.x_boundary + 3)) or (player.xcor() > (self.x_boundary - 3)) or
            (player.ycor() < (-self.y_boundary + 3)) or (player.ycor() > (self.y_boundary - 3))):
                player.lives -= 1
                for particle in particles:
                    particle.change_color(player)
                    particle.explode(player.xcor(), player.ycor())
                player.status = 'crashed'

    def position_range_adder(self, player_positions):
        '''If speed is > 1, the positions aren't recorded in between the speed. Therefore,
        this function is needed to fill in the gaps and append the missing positions'''
        prev_x_pos, prev_y_pos = player_positions[-2] # tuple unpacking
        next_x_pos, next_y_pos = player_positions[-1]
        positions_range = []
        # X coord are changing and the difference between them is greater than 1
        if abs(prev_x_pos - next_x_pos) > 1:
            start = min(prev_x_pos, next_x_pos) + 1
            end = max(prev_x_pos, next_x_pos)
            for x_position in range(start, end):
                coord = (x_position, prev_y_pos)
                positions_range.append(coord)
        # Y coord are changing and the difference between them is greater than 1
        if abs(prev_y_pos - next_y_pos) > 1:
            start = min(prev_y_pos, next_y_pos) + 1
            end = max(prev_y_pos, next_y_pos)
            for y_position in range(start, end):
                coord = (prev_x_pos, y_position)
                positions_range.append(coord)
        if positions_range:
            for position in positions_range:
                if position not in player_positions:
                    player_positions.append(position)
        # print('Range: ', positions_range)

    def player_creation(self):
        '''Two players are always created and are global variables. P1 is blue.
        P2 is Yellow'''
        global P1
        global P2
        # Create player 1
        P1 = Player('P1', -100, 100)
        P1.speed(0)
        P1.color('#40BBE3')

        # Create player 2
        P2 = Player('P2', 100, -100)
        P2.speed(0)
        P2.color('#E3E329')

    def particle_creation(self):
        '''Creates particles. Particles is a global value.'''
        global particles
        particles = []
        # Number of particles
        for i in range(15):
            particles.append(Particle('circle', 'white', 0, 0))

    def particles_explode(self, xcor, ycor):
        '''Makes all particles explode at player crash position'''
        for particle in particles:
            particle.explode(xcor, ycor)

    def keyboard_bindings(self):
        '''Maps keys to player movement.'''
        turtle.listen()
        # Set P1 keyboard bindings
        turtle.onkeypress(P1.turn_left, 'a')
        turtle.onkeypress(P1.turn_right, 'd')
        turtle.onkeypress(P1.accelerate, 'w')
        turtle.onkeypress(P1.decelerate, 's')

        # Set P2 keyboard bindings
        turtle.onkeypress(P2.turn_left, 'Left')
        turtle.onkeypress(P2.turn_right, 'Right')
        turtle.onkeypress(P2.accelerate, 'Up')
        turtle.onkeypress(P2.decelerate, 'Down')

    def draw_score(self):
        '''Using a turtle, this draws the score on the screen once, then clears once
        the score changes. Start position is upper left corner.'''
        self.score_pen.clear()
        self.score_pen.setposition((self.width / -2) + 75, (self.height / 2) - 40)
        self.score_pen.pendown()
        self.score_pen.color('white')
        p1lives = 'P1 Lives: %s' % P1.lives
        p2lives = 'P2 Lives: %s' % P2.lives
        self.score_pen.write(p1lives, font=("Arial", 18, "bold"))
        self.score_pen.penup()
        self.score_pen.hideturtle()
        self.score_pen.setposition((self.width / -2) + 190, (self.height / 2) - 40)
        self.score_pen.pendown()
        self.score_pen.write(p2lives, font=("Arial", 18, "bold"))
        self.score_pen.penup()
        self.score_pen.hideturtle()

    def display_winner(self, player, other):
        '''Once game loop finishes, this is run to display the winner.'''
        self.score_pen.setposition(0, 0)
        self.score_pen.pendown()
        if player.lives > 0:
            winner = player.name
            self.score_pen.write(winner + ' wins!', align='center', font=("Arial", 36, "bold"))
        else:
            winner = other.name
            self.score_pen.write(winner + ' wins!', align='center', font=("Arial", 36, "bold"))

    def game_loop(self):
        '''All players are set into motion, boundary checks, and collision checks
        run continuously until a player runs out of lives.'''
        # Start bgm
        global game_on
        game_on = True
        if os.name == 'posix':
            os.system('afplay son_of_flynn.wav&')
        while P1.lives > 0 and P2.lives > 0:
            # Updates screen only when loop is complete
            turtle.update()
            # Set default player speed
            P1.forward(P1.fd_speed)
            P2.forward(P2.fd_speed)

            # Particle movement
            for particle in particles:
                particle.move()

            # P1 Boundary check
            self.boundary_check(P1)
            # P2 Boundary check
            self.boundary_check(P2)

            # Coercing coordinates and appending to list
            P1.convert_coord_to_int()
            P1.positions.append(P1.coord)
            if len(P1.positions) > 2:
                self.position_range_adder(P1.positions)
            P1.is_collision(P2)

            P2.convert_coord_to_int()
            P2.positions.append(P2.coord)
            if len(P2.positions) > 2:
                self.position_range_adder(P2.positions)
            P2.is_collision(P1)


            # print('Last 5 positions: ', P2.positions[-5:])

            if P1.status == 'crashed' or P2.status == 'crashed':
                P1.player_crashed(P2)
                if os.name == 'posix':
                    os.system('afplay explosion.wav&')
                self.draw_score()
        # Game ends
        self.display_winner(P1, P2)
        self.state = 'game_over'
        game_on = False
        # turtle.exitonclick()
        time.sleep(3)
        self.screen.clear()
        if os.name == 'posix':
            os.system('killall afplay')


class Player(turtle.Turtle):
    def __init__(self, name, start_x, start_y):
        super(Player, self).__init__()
        self.name = name
        self.fd_speed = 1
        self.pensize(2)
        self.start_x = start_x
        self.start_y = start_y
        self.setposition(start_x, start_y)
        self.positions = []
        self.coord = (self.start_x, self.start_y)
        self.lives = 5
        self.status = 'ready'

    def turn_left(self):
        '''90 Degree left turn.'''
        self.left(90)

    def turn_right(self):
        '''90 Degree right turn.'''
        self.right(90)

    def accelerate(self):
        '''Min. speed = 1, Max. speed = 2.'''
        if self.fd_speed < 2:
            self.fd_speed += 1
            self.forward(self.fd_speed) # Needs to be run only if speed changes

    def decelerate(self):
        '''Min. speed = 1, therefore player can never stop'''
        if self.fd_speed > 1:
            self.fd_speed -= 1
            self.forward(self.fd_speed) # Needs to be run only if speed changes

    def convert_coord_to_int(self):
        '''Convert coordinates to integers for more accurate collision detection'''
        x, y = self.pos()
        x = int(x)
        y = int(y)
        self.coord = (x, y)

    def is_collision(self, other):
        '''Collision check'''
        # Player collides into own trail (suicide)
        if self.coord in self.positions[:-10]: # Checks the last positions too quickly
            self.lives -= 1
            # Particle explosion
            for particle in particles:
                particle.change_color(self)
                particle.explode(self.xcor(), self.ycor())
            self.status = 'crashed'

        # Player collides into other player.
        # Covers speed increase, thus 2 positions are checked
        for position in self.positions[-2:]:
            if position in other.positions:
                self.lives -= 1
                # Particle explosion
                for particle in particles:
                    particle.change_color(self)
                    particle.explode(self.xcor(), self.ycor())
                self.status = 'crashed'

    def crash(self):
        '''Removes lightcycle from screen'''
        self.penup()
        self.clear()
        self.respawn()

    def respawn(self):
        '''Respawns light cycle to default location, resets speed to 1, and
        resets the positions'''
        self.status = 'ready'
        self.setposition(self.start_x, self.start_y)
        self.setheading(random.randrange(0, 360, 90))
        self.fd_speed = 1
        self.pendown()
        self.positions = []

    def player_crashed(self, other):
        '''If either player crashes'''

        # print('Last 10 P2 positions: ', P2.positions[-10:])
        self.crash()
        other.crash()


class Particle(turtle.Turtle):
    '''This class is only used to create particle effects when there is a crash.'''
    def __init__(self, spriteshape, color, start_x, start_y):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.shapesize(stretch_wid=.1, stretch_len=.3, outline=None)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd_speed = 10
        self.hideturtle()
        self.frame = 0

    def explode(self, start_x, start_y):
        self.frame = 1
        self.showturtle()
        self.setposition(start_x, start_y)
        self.setheading(random.randint(0, 360))

    def move(self):
        if self.frame > 0:
            self.forward(self.fd_speed)
            self.frame += 1
        if self.frame > 10:
            self.frame = 0
            self.hideturtle()
            self.setposition(0, 0)

    def change_color(self, player):
        pencolor, fillcolor = player.color()
        self.color(pencolor)

def start(width, height):
    gameplay = Game(width, height)


if __name__ == '__main__':
    gameplay = Game()
