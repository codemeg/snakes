import pygame,random

BLACK	= (   0,   0,   0)
WHITE	= ( 255, 255, 255)
GREEN	= (  30, 255,  30)
RED	    = ( 255,   0,   0)
BLUE    = (   0,   0, 255)
YELLOW  = ( 255, 255,   0)
DKGREY  = (  50,  50,  50)
LTGREY  = ( 220, 220, 220)
MAGENTA = ( 164,  39, 227)

GRID_SIZE = 20
SPEED = 1

class Game():
	def __init__(self, boulders = True, treats=True, wrapping=False, diagonal=False, tail_mode=False):
		self.boulders = boulders
		self.treats = treats
		self.wrapping = wrapping
		self.diagonal = diagonal
		self.tail_mode = tail_mode
	def place_boulders(self,grid):
		if self.boulders == False:
			return
		else:
			for row in range(30):
				for col in range(40):
					if random.randint(1,100) == 1:	# 1 in 100 chance
						if grid[row][col] == 0:		# if that space is empty
							grid[row][col] = 9 	# then put a boulder
		return grid
	def place_treats(self,grid):
		if self.treats == False:
			return
		else:
			for row in range(30):
				for col in range(40):
					if random.randint(1,100) == 1:	# 1 in 100 chance
						if grid[row][col] == 0:		# if that space is empty
							grid[row][col] = 5 	# then put a 'treat'
		return grid


class Treat():	# later
	def __init__(self):
		pass


class Snake():
	def __init__(self,color,start_x_y, player_number, human):
		self.width = GRID_SIZE
		self.color = color
		self.stopped = False
		self.x = start_x_y[0]  # starting x coordinate
		self.y = start_x_y[1]  # starting y coordinate
		self.direction = "up"
		self.new_direction = "up"
		self.speed = SPEED
		self.pixels = 0
		self.player_number = player_number  # players are numbered from 1-4
		self.human = human   # if human, True, if computer, False
	def stop(self):
		self.stopped = True
		#self.direction = "none"

	def show(self):
		x = self.x * GRID_SIZE	# convert x and y coordinates to pixels
		y = self.y * GRID_SIZE

		# red box around snake heads to visualize
		pygame.draw.rect(screen, RED, [x,y,self.width,self.width], 1)

		if self.direction == "up":
			y = y - self.pixels
		if self.direction == "down":
			y = y + self.pixels
		if self.direction == "left":
			x = x - self.pixels
		if self.direction == "right":
			x = x + self.pixels
		pygame.draw.rect(screen, self.color, [x,y,self.width,self.width], 0)
		if self.direction == "up":
			pygame.draw.ellipse(screen, BLACK, [x+5,y+5,1,1])
			pygame.draw.ellipse(screen, BLACK, [x+14,y+5,1,1])
		if self.direction == "down":
			pygame.draw.ellipse(screen, BLACK, [x+5,y+14,1,1])
			pygame.draw.ellipse(screen, BLACK, [x+14,y+14,1,1])
		if self.direction == "left":
			pygame.draw.ellipse(screen, BLACK, [x+5,y+5,1,1])
			pygame.draw.ellipse(screen, BLACK, [x+5,y+14,1,1])
		if self.direction == "right":
			pygame.draw.ellipse(screen, BLACK, [x+14,y+5,1,1])
			pygame.draw.ellipse(screen, BLACK, [x+14,y+14,1,1])

	# HUMAN MOVING
	def move(self, grid, direction):
		self.new_direction = direction

		self.pixels += 1
		if self.pixels == GRID_SIZE:
			old_x = self.x
			old_y = self.y
			#self.direction = self.new_direction

			if self.direction == "up":
				self.y -= self.speed
			if self.direction == "down":
				self.y += self.speed
			if self.direction == "left":
				self.x -= self.speed
			if self.direction == "right":
				self.x += self.speed

			# wrap around screen
			if self.x > width - 1:
				self.x = 0
			if self.x < 0:
				self.x = width - 1
			if self.y > height - 1:
				self.y = 0
			if self.y < 0:
				self.y = height - 1

			if grid[self.y][self.x] != 0:
				draw_text("game is over")
				self.stop()
				self.x = old_x
				self.y = old_y
				print self.x, self.y, self.direction
				print "Game Over"
			else:
				grid[self.y][self.x] = self.player_number

			self.pixels = 0
			self.direction = self.new_direction

	
	# COMPUTER SNAKE STUFF

	def which_direction(self,grid):
		"""How the computer decides which direction to go"""

		if self.pixels != 19:
			return self.direction
		if random.randint(1,10) == 1:
			print "I turned randomly"
			return self.turn_randomly(grid)

		# if next square is blocked, turn
		
		if self.direction == "up":
			if grid[self.y-2][self.x] != 0:
				return self.turn_randomly(grid)
		if self.direction == "down":
			if grid[self.y+2][self.x] != 0:
				return self.turn_randomly(grid)
		if self.direction == "left":
			if grid[self.y][self.x-2] != 0:
				return self.turn_randomly(grid)
		if self.direction == "right":
			if grid[self.y][self.x+2] != 0:
				return self.turn_randomly(grid)
		
		# if none of the above, keep going the same direction
		return self.direction

	def turn_randomly(self,grid):
		"""Changes direction randomly but tries not to immediately crash"""
		if self.direction == "up" or self.direction == "down":
			if self.space_blocked(grid,"left"):
				return "right"
			elif self.space_blocked(grid,"right"):
				return "left"
			else:
				return random.choice(["left", "right"])
		elif self.direction == "left" or self.direction == "right":
			if self.space_blocked(grid,"up"):
				return "down"
			elif self.space_blocked(grid,"down"):
				return "up"
			else:
				return random.choice(["up", "down"])

	def space_blocked(self,grid,direction):
		"""Given a direction, would the next space be blocked"""
		if direction == "up":
			if grid[self.y-1][self.x] != 0:
				return True
		if direction == "down":
			if grid[self.y+1][self.x] != 0:
				return True
		if direction == "left":
			if grid[self.y][self.x-1] != 0:
				return True
		if direction == "right":
			if grid[self.y][self.x+1] != 0:
				return True
		return False


def draw_arena(grid):
	for row in range(30):
		for col in range(40):
			if grid[row][col] == 9:		# border
				pygame.draw.rect(screen, DKGREY, [col*GRID_SIZE, row*GRID_SIZE, GRID_SIZE, GRID_SIZE], 0)
			if grid[row][col] == 5:		# treat
				pygame.draw.ellipse(screen, MAGENTA, [col*GRID_SIZE, row*GRID_SIZE, GRID_SIZE, GRID_SIZE], 5)
			for i in range(len(colors)):
				if grid[row][col] == i+1:
					pygame.draw.rect(screen, colors[i], [col*GRID_SIZE, row*GRID_SIZE, GRID_SIZE, GRID_SIZE], 0)

def draw_grid():
	"""Draws an ugly grid so you can see the board better"""
	for row in range(30):
		pygame.draw.line(screen, BLACK, [0,row*GRID_SIZE],[width*GRID_SIZE,row*GRID_SIZE],1)
	for col in range(40):
		pygame.draw.line(screen, BLACK, [col*GRID_SIZE,0],[col*GRID_SIZE, height*GRID_SIZE],1)
				

def draw_text(text):
	font = pygame.font.Font(None, 40)
	text = font.render(text,True,RED)
	screen.blit(text, [300,200])

def print_grid(grid):
	"""Prints grid for debugging"""
	for i in range(30):
		for j in range(40):
			print grid[i][j],
		print ""


# making snakes
human_players = 2
computer_players = 2   # int(raw_input("How many snakes? "))
players = []
humans = []
snakes = []
colors = [YELLOW,GREEN,BLUE,RED]
starting_points = [[10,11],[10,21],[30,11],[30,21]]
random.shuffle(starting_points)

for i in range(human_players):
	players.append(True)
for i in range(computer_players):
	players.append(False)

for i in range(len(players)):
	snakes.append(Snake(colors[i], starting_points[i], i+1, players[i]))

pygame.init()

# making empty grid
grid = []
print grid
for row in range(30):
	grid.append([0]*40)

# adding border
for row in range(30):
	grid[row][0] = 9
	grid[row][39] = 9
for col in range(40):
	grid[0][col] = 9
	grid[29][col] = 9

# setup
width = 40
height = 30
size = (width*GRID_SIZE, height*GRID_SIZE)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Snakes")
done = False
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

direction = ["up","up"]	# initial direction
snakes_stopped = 0
humans_stopped = 0

g = Game()
print g.treats
grid = g.place_boulders(grid)
grid = g.place_treats(grid)
print_grid(grid)

# -------- Main Program Loop -----------
while not done:
	# Events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
			if event.key == pygame.K_LEFT:
				if direction[0] == "up" or direction[0] == "down":
					direction[0] = "left"
			if event.key == pygame.K_RIGHT:
				if direction[0] == "up" or direction[0] == "down":
					direction[0] = "right"
			if event.key == pygame.K_UP:
				if direction[0] == "left" or direction[0] == "right":
					direction[0] = "up"
			if event.key == pygame.K_DOWN:
				if direction[0] == "left" or direction[0] == "right":
					direction[0] = "down"
			if event.key == pygame.K_a:
				if direction[1] == "up" or direction[1] == "down":
					direction[1] = "left"
			if event.key == pygame.K_d:
				if direction[1] == "up" or direction[1] == "down":
					direction[1] = "right"
			if event.key == pygame.K_w:
				if direction[1] == "left" or direction[1] == "right":
					direction[1] = "up"
			if event.key == pygame.K_s:
				if direction[1] == "left" or direction[1] == "right":
					direction[1] = "down"

	# Game Logic
	for i in range(len(players)):
		if not snakes[i].stopped:
			if snakes[i].human == True:
				snakes[i].move(grid,direction[i])
			else:
				computer_direction = snakes[i].which_direction(grid)
				snakes[i].move(grid, computer_direction)
		else:
			snakes_stopped += 1

	# Drawing
	screen.fill(LTGREY)
	draw_arena(grid)
	draw_grid()

	for i in range(len(players)):
		snakes[i].show()
		if snakes[i].stopped:
			draw_text("Player %s crashed!" % (snakes[i].player_number))

	if snakes_stopped == players:
		draw_text("GAME OVER")

	pygame.display.flip()


	for i in range(len(players)):  # this doesn't work
		if snakes[i].human and snakes[i].stopped and humans_stopped < human_players:
			humans_stopped += 1
	if snakes[0].stopped and snakes[1].stopped: # need a better way to do this
		print "all the humans are dead"
		clock.tick(120)
		snakes[2].speed = 2
		snakes[3].speed = 2
	else:
		clock.tick(60)
	 
pygame.quit()


# to add:
# random scattered treats/tricks to do stuff like:
# 	speed you up
# 	slow you down
# 	temporary invincibility
# 	make you invisible for a sec?!

# game mode where you wrap around the board
# game mode where you can go diagonal

# improve computer ai

# game mode to eat each others tails

# fix movement (1 square off)


# Combined human & computer snakes into one class. Made scaffold for future game modes, added boulders & treats placed on the grid. Computer snakes speed up now when human snakes are dead (buggy)
