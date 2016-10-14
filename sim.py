'''
Elevator Simulator
'''

from elevator import Elevator
from building import Building
from person import Person

import sys
import pygame
from pygame.locals import *
from pygame import Color, Rect, Surface
from random import randint

# Define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,127,36)

# Define screen width and height
WINDOWWIDTH = 1100
WINDOWHEIGHT = 900

# Min and max time between events
SPAWN_THRESHOLD_MIN = 5000
SPAWN_THRESHOLD_MAX = 10000

class Sim():
	def __init__(self,width,height):
		self.numFloors = 10                         # How many floors
		self.numElevators = 4                       # How many elevators
		self.elevators = []                         # List of Elevators
		self.persons = []                           # List of People
		self.personId = 0                           # ID Counter for new people
		self.width = width                          # Screen width
		self.height = height                        # Screen height
		self.speed = 10                             # Simulation speed
		self.ground = 50                            # What position is ground
		self.timer = 0                              # Timer between events
		self.startHour = 9                          # Hour (0-23) that day starts
		self.clock = self.startHour * 3600000       # ms counter for clock (start + updated every tick) - 3600000ms/hr
		self.spawn_threshold = getSpawnEventTime()  # When will next event occur

		# Initialize Building - Just do one for now
		self.building = Building()

		e = 100
		# Initialize Elevators
		for i in range(0, self.numElevators):
			self.elevators.append(Elevator(i,self,e))
			e+=150

		# Load Names file and initialize People
		self.personNames = loadNames()
		for i in range(0,25):
			person = self.spawnPerson()


	def spawnPerson(self):
		name = self.personNames[randint(0,len(self.personNames))]
		person = Person(self,name)

		self.persons.append(person)
		self.personId += 1

		el = randint(0,self.numElevators-1)
		person.setDestination((self.elevators[el].getPosition()[0],self.height - self.ground))

		return person

	def personAction(self):
		print "Person action"
		# Find a random person
		p = randint(0,len(self.persons)-1)

		# Do an action
		self.persons[p].randomAction()

	def removePerson(self,id):

		persons_new = []
		for p in self.persons:
			if p.id != id:
				persons_new.append(p)

		self.persons = persons_new

	def simulate(self,dt):
		# TODO: Figure out if we want a multiplier on dt to make it go faster
		self.clock += dt

		for person in self.persons:
			if person.active:
				person.act(dt)

		self.timer += dt

		# Spawn random events - these are for the existing people
		# TODO: How many events? Fixed number? Or proportional to # of people in building? For now, just do 1

		if (self.timer >= self.spawn_threshold):
			self.randomEvent()
			self.timer = 0
			self.spawn_threshold = getSpawnEventTime()

	def randomEvent(self):
		num = randint(0,100)

		# System events only occur 5% of the time
		if num < 5:
			self.systemEvent()
		else:
			self.personEvent()

	def systemEvent(self):
		print "System event - make elevator go to floor. Eventually shut down elevator"

		for elevator in self.elevators:
			if elevator.activeStatus() == False:
				elevator.activate()
				return

		e = randint(0,self.numElevators-1)
		self.elevators[e].deactivate()

	def personEvent(self):
		num = randint(0,100)

		# New Spwn events only occur 25% of the time
		if num < 25:
			self.spawnPerson()
		else:
			self.personAction()

	def render(self,screen,background):
		renderUI(screen,self)
		renderBuilding(screen,self)
		renderElevators(screen,self)
		renderPeople(screen,self)

def renderUI(screen,sim):
	# Render time
	time = sim.fontSmall.render(formatTime(sim.clock),1,WHITE)
	screen.blit(time,(5,5))

	# Render log messages

def renderBuilding(screen,sim):
	#pygame.draw.rect(screen, Color(255, 255, 255), pygame.Rect(100,100,1,10))
	for floor in range(0,sim.numFloors):
		num = sim.fontSmall.render(str(floor + 1),1,ORANGE)
		screen.blit(num,(0, (sim.height - sim.ground - ((floor+1) * sim.building.floorDistance))))

def renderElevators(screen,sim):
    for elevator in sim.elevators:
		num = sim.font.render(str(elevator.getNumber() + 1),1,WHITE)
		#e = sim.font.render(str("EL"),1,WHITE)

		pos = elevator.getPosition()
		size = elevator.getSize()

		# render number - on ground floor
		screen.blit(num,(pos[0],(sim.height- sim.ground)))

		# render elevator itself - for now just the number
		#screen.blit(e,elevator.getPosition())
		if elevator.activeStatus() == True:
			color = WHITE
		else:
			color = RED

		pygame.draw.rect(screen, color, pygame.Rect(pos[0],pos[1],size[0],size[1]),2)

def renderPeople(screen,sim):
	for person in sim.persons:
		if person.visible:
			pygame.draw.circle(screen, person.getColor(),person.getPosition(),10)

# Functions outside of class
def loadNames():
	# returns value because it is needed by init

	personNames = []

	f = open("names.txt")
	file = f.read()
	f.close()

	tmpNames = file.split(",")
	tmpNames.sort()

	for n in tmpNames:
		name = n.split("\"")[1].capitalize()
		personNames.append(name)

	return personNames

def getSpawnEventTime():
	r = randint(SPAWN_THRESHOLD_MIN,SPAWN_THRESHOLD_MAX)

	return r

def formatTime(time):
	s = (time / 1000) % 60
	m = ((time / (1000*60)) % 60)
	h = ((time / (1000*60*60)) % 24)

	return str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)

def main():
	simulator = Sim(WINDOWWIDTH,WINDOWHEIGHT)

	# set up pygame
	pygame.init()

	# set up the window
	screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
	pygame.display.set_caption("Elevator Simulator")

	# Display some text
	background = pygame.Surface(screen.get_size())
	background = background.convert()

	simulator.font = pygame.font.Font(None,64)
	simulator.fontSmall = pygame.font.Font(None,32)
	fontLarge = pygame.font.Font(None,200)

	screen.blit(background, (0, 0))
	pygame.display.flip()

	clock = pygame.time.Clock()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

		dt = clock.tick(30)

		simulator.simulate(dt)

		screen.fill(BLACK)

		simulator.render(screen,background)

		pygame.display.update()


main()