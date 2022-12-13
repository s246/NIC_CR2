from typing import DefaultDict


F_MAX = float('inf')

def findMinRoute(tsp):
	sum = 0
	counter = 0
	j = 0
	i = 0
	min = F_MAX
	visitedRouteList = DefaultDict(int)

	# Starting from the 0th indexed
	# city i.e., the first city
	visitedRouteList[0] = 1
	route = [0] * len(tsp)

	# Traverse the adjacency
	# matrix tsp[][]
	while i < len(tsp) and j < len(tsp[i]):

		# Corner of the Matrix
		if counter >= len(tsp[i]) - 1:
			break

		# If this path is unvisited then
		# and if the cost is less then
		# update the cost
		if j != i and (visitedRouteList[j] == 0):
			if tsp[i][j] < min:
				min = tsp[i][j]
				route[counter] = j + 1

		j += 1

		# Check all paths from the
		# ith indexed city
		if j == len(tsp[i]):
			sum += min
			min = F_MAX
			visitedRouteList[route[counter] - 1] = 1
			j = 0
			i = route[counter] - 1
			counter += 1
			
	# Update the ending city in array
	# from city which was last visited
	i = route[counter - 1] - 1

	min = tsp[i][0]
	route[counter] = 1
	sum += min

	route = route[:-1]
	route.insert(0, 1)

	# print(route)
	# print("Minimum Cost is :", sum)

	return sum, route


# Driver Code
if __name__ == "__main__":

	# Input Matrix
	tsp = [[-1, 10, 15, 20], [10, -1, 35, 25], [15, 35, -1, 30], [20, 25, 30, -1]]
	tsp2 = [[0.0, 266.03, 252.99, 269.32, 133.51],
			[266.03, 0.0, 56.14, 8.0, 168.58],
			[252.99, 56.14, 0.0, 64.12, 135.48],
			[269.32, 8.0, 64.12, 0.0, 174.64],
			[133.51, 168.58, 135.48, 174.64, 0.0]]
	# Function Call
	findMinRoute(tsp2)