from random import randint

colors = [(255,255,255), (255,127,36),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),
 	(192,192,192),(128,128,128),(128,0,0),(128,128,0),(0,128,0),(128,0,128),(0,128,128),(0,0,128)]

minIntervalSeconds = 300     # 5 minutes
maxIntervalSeconds = 3600    # 1 hour

class Person:
	def __init__(self,sim,name):
		self.id = sim.personId                    # Person's ID Number
		self.sim = sim                            # Pointer to simulator object
		self.name = name                          # Tell me your name
		self.active = True                        # Is person active?
		self.visible = True                       # Is person visible?
		self.time = 0                             # Total tick count elapsed
		self.eventTime = 0                        # Total tick count between events
		self.size = randint(10,20)                # Random size for our person
		self.events = []                          # All of the events that are queued for this person

		# These are the actions
		self.waiting = False                      # Currently waiting for elevator
		self.traveling = False                    # Currently traveling to floor kn elevator
		self.walking = False                      # Currently walking
		self.onFloor = False                      # Not currently on their work floor

		# Person is created on the Ground floor (0)
		self.currentFloor = 0
		self.destinationFloor = None
		self.speed = randint(5,50)
		self.color = randomColor()

		# Initialize off screen to right, and direction = -1 (moving to left)
		self.position = (sim.width + randint(100,500),sim.height - sim.ground)
		self.direction = -1
		self.destination = None    # This will be set later - (x,y) coordinates

		# Everyone gets created with a CALL_ELEVATOR event queued
		self.queueCallElevatorEvent()

		self.printDetails()

	def tick(self,dt):

		# Do we need separate timers? Leave as is for now
		self.time += dt
		self.eventTime += dt

	def act(self,dt):
		self.tick(dt)

		# TODO: self.waiting is set when it's at destination - should
		#       probably process event at this point?

		if self.sim.arrived:
			if self.waiting:
				print "Will exit floor and enter elevator here"

			elif self.traveling:
				print "Will exit elevator and enter floor here"

		elif not self.atDestination() and not self.destination == None:
			# Don't process event if we're still walking
			#print "walking"
			self.walk(dt)

		elif not self.events == []:
			print "Got an event to do"
			print self.events
			self.processEvent(self.events[0])

		# No queued events, so if we have a destination just walk
		#elif not self.destination == None:
		#	self.walk()
		else:
			#print "At destination, have nothing to do" + str(self.events)
			pass

	##### Queued Event logic #####
	def addQueuedEvent(self,event):
		print "Adding queued event for " + self.name + " " + str(event)

		evt = self.events
		evt.append(event)

		self.events = evt

	def processEvent(self,event):
		print "Processing event for " + self.name

		eventType = event[0]
		elevator = event[1]
		floor = event[2]
		if len(event) > 3:
			delay = event[3]
		else:
			delay = 0

		# We've met the delay threshold, so do the event
		if self.eventTime > delay:
			print "Event expired, handling event for " + self.name

			# Set events to remainder
			self.events = self.events[1:]

			# Reset event timer
			self.eventTime = 0

			# Now actually handle the event
			if eventType == "CALL_ELEVATOR":
				self.callElevator()
			elif eventType == "ENTER_ELEVATOR":
				self.enterElevator(elevator,floor)
			elif eventType == "EXIT_ELEVATOR":
				self.exitElevator(elevator,floor)
			elif eventType == "ENTER_FLOOR":
				self.enterFloor(elevator,floor)
			elif eventType == "EXIT_FLOOR":
				self.exitFloor(elevator,floor)

	##### Actions go here #####
	def walk(self,dt):
		if not self.atDestination():
			p = self.position
			x = p[0]
			y = p[1]

			xNew = x + (self.direction * (self.speed/self.sim.speed)/100)
			if (x == xNew):
				xNew = x + (self.direction * 1)

			self.position = (xNew,y)
			#if self.position[0] > 0:
			#	pass

		# Arrived at destination
		else:
			self.waiting = True

	def performAction(self):

		'''
		Need to wait until on the floor in order to do this - people are created with an initial
		CALL_ELEVATOR event queued so that will handle their initial entry to building
		'''
		if self.onFloor:
			# Assign a new destination floor
			self.assignFloor()

			# TODO Add random event here - maybe leave building if after quitting time
			# Fow now, just call elevator
			#self.addQueuedEvent(["CALL_ELEVATOR","",self.currentFloor,0])
			self.queueCallElevatorEvent()

	def atDestination(self):
		return self.position == self.destination

	def setDestination(self,destination):
		self.destination = destination

	def getDestination(self):
		return self.destination

	def enterBuilding(self):
		print self.name + " has entered building - start="+ str(self.currentFloor) + ", end=" + str(self.destinationFloor)

	def exitBuilding(self):
		print self.name + " has left building"

	# This probably isn't needed
	def walkToElevator(self,elevatorNum,floor):
		print "Walking to Elevator  " + str(elevatorNum)

	def queueCallElevatorEvent(self):
		print "Queueing call elevator event"
		self.addQueuedEvent(["CALL_ELEVATOR","",self.currentFloor,0])

	def callElevator(self):
		print "Calling elevator on floor " + str(self.currentFloor)
		self.sim.building.callElevator(self.currentFloor)

	def enterElevator(self,elevatorNum,floor):
		print self.name + " has entered elevator " + str(elevatorNum)
		self.visible = False

	def exitElevator(self,elevatorNum,floor):
		print + self.name + " has left elevator " + str(elevatorNum)
		self.visible = True
		self.onFloor = True
		self.currentFloor = self.destFloor
		self.destFloor = None

	def assignFloor(self):

		startFloor = self.currentFloor
		destFloor = startFloor

		while (destFloor == startFloor):
			destFloor = randomFloor(self.sim)

		self.destFloor = destFloor
		print "New floor assigned " + str(self.name) + " " + str(self.destFloor)

	# These two might not be needed after all
	def enterFloor(self,elevator,floor):
		self.visible = False

	def leaveFloor(self,elevator,floor):
		self.visible = True

	def printDetails(self):
		print "Name=" + self.name + " Id=" + str(self.id) + " Speed=" + str(self.speed) + " Position=" + str(self.position) + " Direction=" + str(self.direction) + " Destination=" + str(self.destination)

def randomFloor(sim):
	return randint(0,sim.building.numFloors)

def randomColor():
	return colors[randint(0,len(colors)-1)]

def checkElapsed(self,event):

	return False
