import pygame
import math
from CONST import *
import numpy as np
import random

class Vehicle(object):
	def __init__(self, x, y, dna = None):
		self.acc = CreateVector(0, 0)
		self.vel = CreateVector(0, 0)
		self.pos = CreateVector(x, y)
		self.r = 6
		self.maxspeed = 5
		self.maxforce = .5
		if dna == None:
			self.dna = []
			self.dna.append(random.uniform(-2, 2))
			self.dna.append(random.uniform(-2,2))
			self.dna.append(random.uniform(10,100))
			self.dna.append(random.uniform(10,100))
		else:
			self.dna = dna

		self.hp = 1

	def clone(self):
		return Vehicle(random.randrange(WIDTH), random.randrange(HEIGHT), self.dna)

	def update(self):
		self.hp -= .01
		self.vel.add(self.acc)
		self.vel.limit(self.maxspeed)
		self.pos.add(self.vel)
		self.acc.mul(0)

	def boundaries(self):
		d = 20
		desired = None

		if self.pos.x < d:
			desired = CreateVector(self.maxspeed, self.vel.y)
		elif self.pos.x > WIDTH - d:
			desired = CreateVector(-self.maxspeed, self.vel.y)
		elif self.pos.y < d:
			desired = CreateVector(self.vel.x, self.maxspeed)
		elif self.pos.y > HEIGHT - d:
			desired = CreateVector(self.pos.x, - self.maxspeed)


		if desired != None:
			desired.normalize()
			desired.mul(self.maxspeed)
			desired.sub(self.vel)
			desired.limit(self.maxforce)
			self.applyForce(desired)


	def applyForce(self, force):
		self.acc.add(force)

	def seek(self, target):
		temp = target.copy()
		temp.sub(self.pos)
		temp.setMag(self.maxspeed)

		temp.sub(self.vel)
		temp.limit(self.maxforce)

		return temp

	def dead(self):
		return self.hp < 0

	def behaviors(self, foods, poisions):
		foodSteer = self.eat(foods, .2, self.dna[2])
		poisionSteer = self.eat(poisions, -.5, self.dna[3])

		foodSteer.mul(self.dna[0])
		poisionSteer.mul(self.dna[1])

		self.applyForce(foodSteer)
		self.applyForce(poisionSteer)

	def eat(self, foods, nutri, perception):
		record = float('inf')
		closet = None
		for food in foods:
			d = food.dist(self.pos)
			if d < 4 + self.r:
				if nutri < 0:
					print('poision')
				foods.remove(food)
				self.hp += nutri
				if self.hp > 1.3:
					self.hp = 1.3
			else:
				if d < record and d < perception:
					record = d
					closet = food


		if closet != None:
			return self.seek(closet)

		return CreateVector(0, 0)

	def draw(self, screen):
		theta = self.vel.heading() + math.pi/2
		top_x = 30 * math.sin(theta) + self.pos.x
		top_y = 30 * math.cos(theta) + self.pos.y
		bottom_right_x = 8 * math.sin(theta-math.pi/2) + self.pos.x
		bottom_right_y = 8 * math.cos(theta-math.pi/2) + self.pos.y
		bottom_left_x = 8 * math.sin(theta+math.pi/2) + self.pos.x
		bottom_left_y = 8 * math.cos(theta+math.pi/2) + self.pos.y

		color = [0, 0, 0]
		if self.hp > .5:
			color[1] = int(self.hp*255)
			if color[1] > 255:
				color[1] = 255
		elif self.hp == .5:
			color[0] = 255
			color[1] = 255
		elif self.hp < .5:
			color[0] = 255
			color[1] = int(self.hp*255)
			if color[1] < 0:
				color[1] = 0
		pygame.draw.polygon(screen, color, ((bottom_left_x, bottom_left_y), (bottom_right_x, bottom_right_y), (top_x, top_y)))
		pygame.draw.circle(screen, GREEN, (self.pos.x, self.pos.y), self.dna[3], width = 2)
		pygame.draw.circle(screen, RED, (self.pos.x, self.pos.y), self.dna[3], width = 2)
