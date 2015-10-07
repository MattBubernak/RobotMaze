# Program Name: RobotProgram.py
# Author: Matt Bubernak
# Date: 10/6/2015
# Description: Provided an input file containing a grid, defined by the following 
#              character set: [.,R,O,T] , the program will tell you if there is a 
#              connection between R and T through the grid, that doesn't go through
#              an O. Will output 'Yes' or 'No'.
# Example 'Yes' Input File: 
# 					  ...
#                     RO.
#                     ..T
# Example 'No' Input File: 
# 					  ...
#                     ROO
#                     .OT
# Usage: ./RobotProgram.py [input.txt]

import os.path
import sys

# Used to as an element of a grid, acts as a tuple of a character and boolean 
# for whether it has been visited. 
class GridElem:
	def __init__(self,val):
		self.value = val
		self.visited = False

# Used to store the input file, translated to a 2D array. 
class Grid: 
	def __init__(self,inputText):
		# We can store a 2D array as a dictionary.
		self.gridArr = {} 
		# We will find this when we load a grid.
		self.robotX = -1   
		self.robotY = -1 
		# Used for incramenting
		i = 0
		j = 0

		# Loop through every line. 
		for line in inputText: 
			j = 0
			# Split line into characters, and add them to the gridArr
			for char in list(line):
				self.gridArr[i,j] = (GridElem(char.lower()))
				if (char.lower() == 'r'):
					self.robotX = j
					self.robotY = i
				j+=1

			# Apply appropriate operations to i/j before the next line is read. 
			i += 1

	def validLocation(self,x,y):
		if (y,x) in self.gridArr:
			return True
		return False

	def visitLocation(self,x,y):
		self.gridArr[y,x].visited = True

	def get(self,x,y):
		return self.gridArr[y,x]

class Solver: 
	def __init__(self):
		pass

	def solveRecurse(self,grid,x,y):
		if (grid.validLocation(x,y) == False):
			return False

		# If we have already been here, or it's not valid, or it's an obstacle
		elif ((grid.get(x,y).value == 'o') or (grid.get(x,y).visited == True)):
			return False

		# If it's the target, return true. 
		elif (grid.get(x,y).value == 't'):
			return True

		# Else try all adjacent locations. 
		else:
			grid.visitLocation(x,y)
			solveUp = self.solveRecurse(grid,x,y+1)
			solveDown = self.solveRecurse(grid,x,y-1)
			solveLeft = self.solveRecurse(grid,x-1,y)
			solveRight = self.solveRecurse(grid,x+1,y)
			return (solveUp or solveDown or solveLeft or solveRight)

	def solveGrid(self,grid):
		return self.solveRecurse(grid,grid.robotX,grid.robotY) 

def main(): 
	# The 'solver' that we will load with a grid, and asked to solve it. 
	solver = Solver() 

	# Verify the user provided correct format of input. 
	if (len(sys.argv) < 2 or len(sys.argv) > 2):
		print("Usage: ./RobotProgram.py [input.txt]")
		return
	# If the correct input format was provided
	else: 
		inputPath = sys.argv[1]
		# If the file exists pass the input to the solver.
		if (os.path.exists(inputPath)):
			fileObj = open(inputPath,'r')
			lines = fileObj.readlines()
			result = solver.solveGrid(Grid(lines))
			if (result == True): 
				print("yes")
			else: 
				print("no")

		# Else, inform user of invalid input and return
		else: 
			print("File: " + inputPath + " doesn't exist.")

		return

main()