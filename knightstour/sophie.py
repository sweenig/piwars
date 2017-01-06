"""
This code generates the path required for a knight's tour 
around a chessboard with user-specified dimensions
Written by Sophie Li, 2016
http://blog.justsophie.com/algorithm-for-knights-tour-in-python/
"""
import sys
from time import sleep
from sense_emu import SenseHat
sense = SenseHat()
sense.clear()
w = (255,255,255)
b = (0,0,0)
k = (0,0,255) #color for the knight
p = (192,192,255) #color for previous path spaces
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
		self.w = width
		self.h = height
		self.board = []
		self.generate_board()
	def generate_board(self):
		"""
		Creates a nested list to represent the game board
		"""
		for i in range(self.h):
			self.board.append([0]*self.w)
	def print_board(self):
		print "  "
		print "------"
		for elem in self.board:
			print elem
		print "------"
		print "  "
	def generate_legal_moves(self, cur_pos):
		"""
		Generates a list of legal moves for the knight to take next
		"""
		possible_pos = []
		move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
						(2, 1), (2, -1), (-2, 1), (-2, -1)]

		for move in move_offsets:
			new_x = cur_pos[0] + move[0]
			new_y = cur_pos[1] + move[1]

			if (new_x >= self.h):
				continue
			elif (new_x < 0):
				continue
			elif (new_y >= self.w):
				continue
			elif (new_y < 0):
				continue
			else:
				possible_pos.append((new_x, new_y))

		return possible_pos
	def sort_lonely_neighbors(self, to_visit):
		"""
		It is more efficient to visit the lonely neighbors first, 
		since these are at the edges of the chessboard and cannot 
		be reached easily if done later in the traversal
		"""
		neighbor_list = self.generate_legal_moves(to_visit)
		empty_neighbours = []

		for neighbor in neighbor_list:
			np_value = self.board[neighbor[0]][neighbor[1]]
			if np_value == 0:
				empty_neighbours.append(neighbor)

		scores = []
		for empty in empty_neighbours:
			score = [empty, 0]
			moves = self.generate_legal_moves(empty)
			for m in moves:
				if self.board[m[0]][m[1]] == 0:
					score[1] += 1
			scores.append(score)

		scores_sort = sorted(scores, key = lambda s: s[1])
		sorted_neighbours = [s[0] for s in scores_sort]
		return sorted_neighbours
	def tour(self, n, path, to_visit):
		"""
		Recursive definition of knights tour. Inputs are as follows:
		n = current depth of search tree
		path = current path taken
		to_visit = node to visit
		"""
		self.board[to_visit[0]][to_visit[1]] = n
		path.append(to_visit) #append the newest vertex to the current point
		#print "Visiting: ", to_visit
		if n == self.w * self.h: #if every grid is filled
			#self.print_board()
			#print path
			#print "Done solving!"
			prev_x,prev_y = path[0][0],path[0][1]
			for space in path:
				sense.set_pixel(prev_x,prev_y,p)
				sense.set_pixel(space[0],space[1],k)
				prev_x,prev_y = space[0],space[1]
				sleep(0.25)
			sys.exit(1)
		else:
			sorted_neighbours = self.sort_lonely_neighbors(to_visit)
			for neighbor in sorted_neighbours:
				self.tour(n+1, path, neighbor)
			#If we exit this loop, all neighbours failed so we reset
			self.board[to_visit[0]][to_visit[1]] = 0
			try:
				path.pop()
				print "Going back to: ", path[-1]
			except IndexError:
				print "No path found"
				sys.exit(1)

kt = KnightsTour(8, 8)
startpos = tuple(int(x.strip()) for x in raw_input('Enter the starting position in the format X,Y: ').split(','))
#kt.tour(1, [], (0,0))
kt.tour(1,[],startpos)
