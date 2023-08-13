import pygame
import math
from CONST import *
import numpy as np
import random
from vehicle import Vehicle

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

total_poision = 20

def draw(screen, vehicles, foods, poisions):
	screen.fill(BACKGROUND)

	if len(poisions) < total_poision:
		x = random.randrange(WIDTH)
		y = random.randrange(HEIGHT)
		poisions.append(CreateVector(x, y))

	if random.randrange(100) < 20:
		x = random.randrange(WIDTH)
		y = random.randrange(HEIGHT)
		foods.append(CreateVector(x, y))

	for food in foods:
		pygame.draw.circle(screen, GREEN, (food.x, food.y), 4)

	for poision in poisions:
		pygame.draw.circle(screen, RED, (poision.x, poision.y), 4)

	for vehicle in vehicles:
		vehicle.boundaries()
		vehicle.behaviors(foods, poisions)
		vehicle.update()
		vehicle.draw(screen)
		
		if random.uniform(0, 100) < .1:
			vehicles.append(vehicle.clone())
		
		if vehicle.dead():
			vehicles.remove(vehicle)


	pygame.display.update()

def main():
	vehicles = []

	for i in range(5):
		vehicles.append(Vehicle(random.randrange(WIDTH), random.randrange(HEIGHT)))
	
	foods = []
	for i in range(40):
		x = random.randrange(WIDTH)
		y = random.randrange(HEIGHT)
		foods.append(CreateVector(x, y))

	poisions = []
	for i in range(total_poision):
		x = random.randrange(WIDTH)
		y = random.randrange(HEIGHT)
		poisions.append(CreateVector(x, y))

	run = True
	while run:
		clock.tick(60)
		draw(screen, vehicles, foods, poisions)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pass


	pygame.quit()

main()