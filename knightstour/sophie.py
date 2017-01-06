"""
This code generates the path required for a knight's tour 
around a chessboard with user-specified dimensions
Written by Sophie Li, 2016, modified for use with SenseHat by Stuart Weenig
http://blog.justsophie.com/algorithm-for-knights-tour-in-python/
"""

import sys
from time import sleep
if raw_input('Use real sense hat? (Y/N)').lower() == 'y':
	from sense_hat import SenseHat
else:
	from sense_emu import SenseHat

sense = SenseHat()
sense.clear()
w = (255,255,255)
b = (0,0,0)
k = (0,0,255) #color for the knight
p = (0,255,0) #color for previous path spaces
if raw_input('Draw checkerboard? (Y/N)').lower() == 'y':
	blankboard = [[w,b,w,b,w,b,w,b],
                [b,w,b,w,b,w,b,w],
                [w,b,w,b,w,b,w,b],
                [b,w,b,w,b,w,b,w],
                [w,b,w,b,w,b,w,b],
                [b,w,b,w,b,w,b,w],
                [w,b,w,b,w,b,w,b],
                [b,w,b,w,b,w,b,w]]
	sense.set_pixels(sum(blankboard,[]))

class KnightsTour:

	def __init__(self, width, height):
		self.w = width #store the width in the object
		self.h = height #store the height in the object
		self.board = [] #make a 0 dimension board
		for i in range(self.h): #for each column...
			self.board.append([0]*self.w) #add a row of 0's

	def generate_legal_moves(self, cur_pos): #Generates a list of legal moves for the knight to take next
		possible_pos = [] #assume no moves are legal
		move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),(2, 1), (2, -1), (-2, 1), (-2, -1)] #relative positions of possible moves
		for move in move_offsets: #for each possible move
			new_x = cur_pos[0] + move[0] #set new position
			new_y = cur_pos[1] + move[1] #set new position
			if (new_x >= self.h or new_x < 0 or new_y >= self.w or new_y < 0): #if the new position is off the board
				continue #don't do anything (this should be turned into a single if statement, instead of an if..else
			else: #if the new position is on the board, append it
				possible_pos.append((new_x, new_y)) #append the validated position to the possible_position list
		return possible_pos #return the possible position list

	def sort_lonely_neighbors(self, to_visit):
		"""
		It is more efficient to visit the lonely neighbors first, 
		since these are at the edges of the chessboard and cannot 
		be reached easily if done later in the traversal
		"""
		neighbor_list = self.generate_legal_moves(to_visit) #get all the moves from the current position that are on the board
		empty_neighbours = [] #make a place to list all the empty neighbors
		for neighbor in neighbor_list: #for each legal move
			np_value = self.board[neighbor[0]][neighbor[1]] #get the value of the first legal move
			if np_value == 0: #if it's zero, it hasn't been visited, so it's an empty neighbor
				empty_neighbours.append(neighbor) #if it hasn't been visited, add it to the empty neighbors list
		scores = [] #make a place to store the scores
		for empty in empty_neighbours: #for all legal moves that haven't been visited
			score = [empty, 0] #give the move a starting score of 0
			moves = self.generate_legal_moves(empty) #figure out the moves from each of to_visit's neighbors
			for m in moves: #for all legal moves
				if self.board[m[0]][m[1]] == 0: #if the move is 0, it's empty, give it a higher score
					score[1] += 1 #increment the neighbor for each of the neighbor's empty neighbors
			scores.append(score) #put the score for this move into the list
		scores_sort = sorted(scores, key = lambda s: s[1]) #sort by the score
		sorted_neighbours = [s[0] for s in scores_sort] #put the moves in order into the sorted neighbors list
		return sorted_neighbours #return the list

	def tour(self, n, path, to_visit): #n = current depth of search tree, path = current path taken, to_visit = node to visit
		self.board[to_visit[0]][to_visit[1]] = n #put the current count in the new position
		path.append(to_visit) #append the newest vertex to the current point
		if n == self.w * self.h: #if every grid is filled
			prev_x,prev_y = path[0][0],path[0][1] #save the starting position as the new position
			for space in path: #mark the path
				sense.set_pixel(prev_x,prev_y,p) #mark the previous position with a lighter color
				sense.set_pixel(space[0],space[1],k) #mark the current position of the knight
				prev_x,prev_y = space[0],space[1] #save the current position as the previous position
				sense.set_pixel(startpos[0],startpos[1],(255,0,0)) #mark the starting position
				sleep(0.25) #give the user a chance to see where things are (animation speed)
			sys.exit(1) #exit the script because it was successful (if we return, the assumption is that it was unsuccessful)
		else: #not every space is filled
			sorted_neighbours = self.sort_lonely_neighbors(to_visit) #figure out the best order to try legal moves against
			for neighbor in sorted_neighbours: #for every legal move
				self.tour(n+1, path, neighbor) #recursion point
			#If we exit this loop, all neighbours failed so we reset
			self.board[to_visit[0]][to_visit[1]] = 0 #mark that new spot with a 0 to indicate it can't be done from this path
			try:
				path.pop() #take the most recent attempt off the path
			except IndexError: #if there's nothing on the path to take off...
				print('No available paths.')
				sys.exit(1) #exit unsuccessfully

kt = KnightsTour(8, 8) #instantiate the board
startpos = tuple(int(x.strip()) for x in raw_input('Enter the starting position in the format X,Y: ').split(',')) #prompt for starting position
kt.tour(1,[],startpos) #start looking for a path from the prompted location
