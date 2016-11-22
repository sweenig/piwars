from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.clear()

max_speed = 40 #total magnitude range of speed (double the max speed in one direction)
r = (255,0,0) #color of the walls
g = (0,255,0) #color of the target
b = (0,0,0) #color of the floor
orient_margin = 5 #the distance from absolute zero orientation beyond which movement will occur
maze = 	[[b,b,b,b,b,b,b,b],
				 [b,b,r,b,b,b,b,b],
				 [r,r,r,b,r,b,b,b],
				 [b,b,r,b,r,r,r,r],
				 [b,b,b,b,b,b,b,b],
				 [b,b,r,r,r,r,b,b],
				 [b,b,b,r,g,b,b,b],
				 [b,b,b,r,b,b,b,b]] #initial map of the maze

class Marble():
	def __init__(self, x, y, red, green, blue):
		#global marbles
		self.x = x #define initial location
		self.y = y #define initial location
		self.color = (red,green,blue) #define the color of the marble
		self.active = 1
		#print('Marble placed at (%s,%s)' % (self.y, self.x))
		if maze[self.y][self.x] == r or maze[self.y][self.x] == g: #check if the marble was initialized on a wall or the exit
			print('Marble placed on a wall or the exit, removing that marble.')
			self.active = 0
	def move(self,pitch,roll):
		new_x = self.x #set new x location to existing x location
		new_y = self.y #set new y location to existing y location
		if pitch > orient_margin and self.x != 7: #if tilted right and not on the right edge
			new_x += 1 #move to the right
		elif pitch < 0 - orient_margin and self.x != 0: #if tilted left and not on the left edge
			new_x -= 1 #move to the left
		if roll > orient_margin and self.y != 7: #if tilted up and not on the upper edge
			new_y += 1 #move up
		elif roll < 0 - orient_margin and self.y != 0: #if tilted down and not on the lower edge
			new_y -= 1 #move down
		if maze[new_y][new_x] != r: #as long as the marble's x and y are not on a wall
			self.x = new_x #set marble's x location
			self.y = new_y #set marble's y location
		elif maze[new_y][self.x] != r: #as long as the marble's y is not on a wall
			self.y = new_y #set marble's y location
		elif maze[self.y][new_x] != r: #as long as the marble's x is not on a wall
			self.x = new_x #set marble's x location

marbles = [] #build the marbles list
marbles.append(Marble(1,1,255,255,255)) #add a marble
marbles.append(Marble(2,6,0,0,255))
#marbles.append(Marble(0,0,255,255,0))
#marbles.append(Marble(4,6,64,64,64))

for marble in range(len(marbles)-1,-1,-1): #examine marbles in reverse order
	if marbles[marble].active == 0: #if the marble is inactive
		marbles.pop(marble) #remove the marble

while len(marbles) > 0:
	for marble in marbles:
		pitch = sense.get_orientation()['pitch'] #get pitch
		#convert roll from 0 through 360 to -180 through 180
		if pitch > 180:
			pitch = -1 * (360-pitch)
		#convert roll from 0 through 360 to -180 through 180
		roll = sense.get_orientation()['roll'] #get roll
		if roll > 180:
			roll = -1 * (360-roll)
		speed = max(1,((pitch*pitch) + (roll*roll)) / 255 / 255 * max_speed) #adjust speed based on magnitude of distance from zero orientation
		maze[marble.y][marble.x] = b #color the previous location the same as the floor
		marble.move(pitch,roll) #move the marble
		if maze[marble.y][marble.x] == g: #if the marble is over the end point
			marbles.pop(marbles.index(marble)) #remove it from the list
		else:
			maze[marble.y][marble.x] = marble.color #put the marble's new position into the maze
	sense.set_pixels(sum(maze,[])) #draw the maze, marbles and all
	sleep(1/speed)
sense.show_message('You Win!')

