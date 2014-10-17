import pygame,random

BLACK	= (   0,   0,   0)
WHITE	= ( 255, 255, 255)
GREEN	= (  30, 255, 30)
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
				#print self.x, self.y, self.direction
				print "Game Over"
			else:
				grid[self.y][self.x] = self.player_number 	# later change this to a player number

			self.pixels = 0
			self.direction = self.new_direction

	def show(self):
		x = self.x * GRID_SIZE	# convert x and y coordinates to pixels
		y = self.y * GRID_SIZE
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
		if self.pixels != 1:
			return self.new_direction

		# if next square is blocked, turn
		if self.direction == "up":
			if grid[self.y-1][self.x] != 0:
				return self.turn()
		if self.direction == "down":
			if grid[self.y+1][self.x] != 0:
				return self.turn()
		if self.direction == "left":
			if grid[self.y][self.x-1] != 0:
				return self.turn()
		if self.direction == "right":
			if grid[self.y][self.x+1] != 0:
				return self.turn()

		# turn randomly
		if random.randint(1,10) == 1:
			return self.turn()

		return self.new_direction

	def turn(self):
		if self.direction == "up" or self.direction == "down":
			return random.choice(["left", "right"])
		elif self.direction == "left" or self.direction == "right":
			return random.choice(["up", "down"])


def draw_grid(grid):
	for row in range(30):
		for col in range(40):
			if grid[row][col] == 9:
				pygame.draw.rect(screen, DKGREY, [col*GRID_SIZE, row*GRID_SIZE, GRID_SIZE, GRID_SIZE], 0)
			for i in range(len(colors)):
				if grid[row][col] == i+1:
					pygame.draw.rect(screen, colors[i], [col*GRID_SIZE, row*GRID_SIZE, GRID_SIZE, GRID_SIZE], 0)
				

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
number_of_players = 3   # int(raw_input("How many snakes? "))
snakes = []
colors = [YELLOW,GREEN,BLUE,RED]
starting_points = [[10,11],[10,21],[30,11],[30,21]]
random.shuffle(starting_points)
print starting_points
for i in range(number_of_players):
	snakes.append(ComputerSnake(colors[i+1],starting_points[i+1],i+2))

my_snake = Snake(colors[0],starting_points[0],1)


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

direction = "up"	# first direction

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
				if direction == "up" or direction == "down":
					direction = "left"
			if event.key == pygame.K_RIGHT:
				if direction == "up" or direction == "down":
					direction = "right"
			if event.key == pygame.K_UP:
				if direction == "left" or direction == "right":
					direction = "up"
			if event.key == pygame.K_DOWN:
				if direction == "left" or direction == "right":
					direction = "down"

	if not my_snake.stopped:
		my_snake.move(grid,direction)

	for i in range(number_of_players):
		if not snakes[i].stopped:
			computer_direction = snakes[i].which_direction(grid)
			snakes[i].move(grid,computer_direction)

	# --- Game logic should go here
	
	# --- Drawing code should go here

	screen.fill(LTGREY)
	draw_grid(grid)

	for i in range(number_of_players):
		snakes[i].show()

	my_snake.show()

	pygame.display.flip()

	clock.tick(60)
	 
pygame.quit()