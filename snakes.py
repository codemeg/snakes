import pygame,random

BLACK	= (   0,   0,   0)
WHITE	= ( 255, 255, 255)
GREEN	= (  30, 255,  30)
RED	    = ( 255,   0,   0)
BLUE    = (   0,   0, 255)
YELLOW  = ( 255, 255,   0)
DKGREY  = (  50,  50,  50)
LTGREY  = ( 220, 220, 220)

GRID_SIZE = 20
DEFAULT_SPEED = 1

class Snake():
	def __init__(self,color,start_x_y, player_number):
		self.width = GRID_SIZE
		self.color = color
		self.stopped = False
		self.x = start_x_y[0]
		self.y = start_x_y[1]
		self.direction = "up"
		self.new_direction = "up"
		self.default_speed = DEFAULT_SPEED
		self.pixels = 0
		self.player_number = player_number
	def move(self, grid, direction):
		self.new_direction = direction

		self.pixels += 1
		if self.pixels == GRID_SIZE:
			old_x = self.x
			old_y = self.y
			#self.direction = self.new_direction

			if self.direction == "up":
				self.y -= self.default_speed
			if self.direction == "down":
				self.y += self.default_speed
			if self.direction == "left":
				self.x -= self.default_speed
			if self.direction == "right":
				self.x += self.default_speed

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
				draw_game_over()
				self.stop()
				self.x = old_x
				self.y = old_y
				print self.x, self.y, self.direction
				print "Game Over"
			else:
				grid[self.y][self.x] = self.player_number

			self.pixels = 0
			self.direction = self.new_direction

	def show(self):
		x = self.x * GRID_SIZE	# convert x and y coordinates to pixels
		y = self.y * GRID_SIZE
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
	def stop(self):
		self.stopped = True
		self.direction = "none"

class ComputerSnake(Snake):
	def __init__(self,color,start_x_y, player_number):
		Snake.__init__(self,color,start_x_y, player_number)

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
			if grid[row][col] == 9:
				pygame.draw.rect(screen, DKGREY, [col*GRID_SIZE, row*GRID_SIZE, GRID_SIZE, GRID_SIZE], 0)
			for i in range(len(colors)):
				if grid[row][col] == i+1:
					pygame.draw.rect(screen, colors[i], [col*GRID_SIZE, row*GRID_SIZE, GRID_SIZE, GRID_SIZE], 0)

def draw_grid():
	for row in range(30):
		pygame.draw.line(screen, BLACK, [0,row*GRID_SIZE],[width*GRID_SIZE,row*GRID_SIZE],1)
	for col in range(40):
		pygame.draw.line(screen, BLACK, [col*GRID_SIZE,0],[col*GRID_SIZE, height*GRID_SIZE],1)
				

def draw_game_over(): # doesn't work yet
	font = pygame.font.Font(None, 40)
	text = font.render("GAME OVER",True,RED)
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
total_players = human_players + computer_players
humans = []
snakes = []
colors = [YELLOW,GREEN,BLUE,RED]
starting_points = [[10,11],[10,21],[30,11],[30,21]]
random.shuffle(starting_points)

for i in range(human_players):
	humans.append(Snake(colors[i], starting_points[i], i+1))

for i in range(computer_players):
	snakes.append(ComputerSnake(colors[human_players+i],starting_points[human_players+i], human_players+i+1))

#my_snake = Snake(colors[0],starting_points[0],1)


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

width = 40
height = 30
size = (width*GRID_SIZE, height*GRID_SIZE)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Snakes")
done = False
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

direction = ["up","up"]	# initial direction

# -------- Main Program Loop -----------
while not done:
	# --- Main event loop
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

	for i in range(human_players):
		if not humans[i].stopped:
			humans[i].move(grid,direction[i])

	for i in range(computer_players):
		if not snakes[i].stopped:
			computer_direction = snakes[i].which_direction(grid)
			snakes[i].move(grid,computer_direction)

	# --- Game logic should go here
	
	# --- Drawing code should go here

	screen.fill(LTGREY)
	draw_arena(grid)
	draw_grid()

	for i in range(computer_players):
		snakes[i].show()
	for i in range(human_players):
		humans[i].show()

	pygame.display.flip()

	clock.tick(60)
	 
pygame.quit()