import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# creating screen
XMODE = 1200
YMODE = 800

screen = pygame.display.set_mode((XMODE, YMODE))

# caption and icon
pygame.display.set_caption("Welcome to Space\
alien Game by:- styles")


# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
	score = font.render("Points: " + str(score_val),
						True, (255,255,255))
	screen.blit(score, (x , y ))

def game_over():
	game_over_text = game_over_font.render("GAME OVER",
										True, (255,255,255))
	screen.blit(game_over_text, (190, 250))


# spaceship
spaceshipImage = pygame.image.load('images/spaceship.png')
spaceship_X = 300
spaceship_Y = 550
spaceship_Xchange = 0
spaceshipImage = pygame.transform.scale(spaceshipImage, ((200,200)))

# alien
alienImage = []
alien_X = []
alien_Y = []
alien_Xchange = []
alien_Ychange = []
no_of_alien = 6

for num in range(no_of_alien):
	alienImage.append(pygame.image.load('images/alien.png'))
	alien_X.append(random.randint(64, 737))
	alien_Y.append(random.randint(30, 180))
	alien_Xchange.append(1.2)
	alien_Ychange.append(50)

# Bullet
# rest means bullet is not moving
# fire means bullet is moving
bulletImage = pygame.image.load('images/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "rest"

# Bullets Collision Function
def collide(x1, x2, y1, y2):
	distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
	if distance <= 50:
		return True
	else:
		return False

def spaceship(x, y):
	screen.blit(spaceshipImage, (x - 16, y + 10))

def alien(x, y, i):
	screen.blit(alienImage[i], (x, y))

def bullet(x, y):
	global bullet_state
	screen.blit(bulletImage, (x, y))
	bullet_state = "fire"

# game loop
running = True
while running:

	# RGB
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# Controling the spaceship movement
		# from the arrow keys
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				spaceship_Xchange = -1.7
			if event.key == pygame.K_RIGHT:
				spaceship_Xchange = 1.7
			if event.key == pygame.K_SPACE:
				
				# Fixing the change of direction of bullet
				if bullet_state is "rest":
					bullet_X = spaceship_X
					bullet(bullet_X, bullet_Y)
		if event.type == pygame.KEYUP:
			spaceship_Xchange = 0

	# adding the change in the spaceship position
	spaceship_X += spaceship_Xchange
	for i in range(no_of_alien):
		alien_X[i] += alien_Xchange[i]

	# bullet movement
	if bullet_Y <= 0:
		bullet_Y = 600
		bullet_state = "rest"
	if bullet_state is "fire":
		bullet(bullet_X, bullet_Y)
		bullet_Y -= bullet_Ychange

	# movement of the alien
	for i in range(no_of_alien):
		
		if alien_Y[i] >= 450:
			if abs(spaceship_X-alien_X[i]) < 80:
				for j in range(no_of_alien):
					alien_Y[j] = 2000
				game_over()
				break

		if alien_X[i] >= 735 or alien_X[i] <= 0:
			alien_Xchange[i] *= -1
			alien_Y[i] += alien_Ychange[i]
		# Collision
		collision = collide(bullet_X, alien_X[i], bullet_Y, alien_Y[i])
		if collision:
			score_val += 1
			bullet_Y = 600
			bullet_state = "rest"
			alien_X[i] = random.randint(64, 736)
			alien_Y[i] = random.randint(30, 200)
			alien_Xchange[i] *= -1

		alien(alien_X[i], alien_Y[i], i)


	# restricting the spaceship so that
	# it doesn't go out of screen
	if spaceship_X <= 16:
		spaceship_X = 16;
	elif spaceship_X >= 750:
		spaceship_X = 750


	spaceship(spaceship_X, spaceship_Y)
	show_score(scoreX, scoreY)
	pygame.display.update()
