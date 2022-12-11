import numpy as np

def crossover_knapsack(parents, skip_crossover = False):
    crossover_point = np.random.randint(0, high = len(parents[0]), dtype = int)
    offsprings = parents.copy()
    # print('crossover_point knapsack', crossover_point)
    
    # Case for no crossover
    if skip_crossover == True:
        return offsprings
    
    offsprings[0, crossover_point:] = parents[1, crossover_point:]
    offsprings[1, crossover_point:] = parents[0, crossover_point:]
    
    return offsprings.tolist()

def crossover_tsp(parents, skip_crossover = False):
    crossover_point = np.random.randint(1, high = len(parents[0]), dtype = int)
    # print('crossover_point tsp', crossover_point)

    offsprings = []
    offspring_1 = []
    offspring_2 = []

    for i in range(crossover_point):
        offspring_1.append(parents[0][i])
        offspring_2.append(parents[1][i])
    
    for i in range(len(parents[0])):
        if parents[1][i] not in offspring_1:
            offspring_1.append(parents[1][i])

        if parents[0][i] not in offspring_2:
            offspring_2.append(parents[0][i])
    
    offsprings.append(offspring_1)
    offsprings.append(offspring_2)

    return offsprings

def crossover(parents):
    offsprings = parents.copy()

    # crossover knapsack
    parents_knapsack = []
    parents_knapsack.append(parents[0][0])
    parents_knapsack.append(parents[1][0])
    parents_knapsack_arr = np.array(parents_knapsack)
    offsprings_knapsack = crossover_knapsack(parents_knapsack_arr)

    # crossover TSP
    parents_tsp = []
    parents_tsp.append(parents[0][1])
    parents_tsp.append(parents[1][1])
    offsprings_tsp = crossover_tsp(parents_tsp)

    # offspring 1
    offsprings[0] = (offsprings_knapsack[0], offsprings_tsp[0])
    # offspring 2
    offsprings[1] = (offsprings_knapsack[1], offsprings_tsp[1])

    return offsprings



def main():
    #generating test values
    parents = []
    parent1 = ([1,0,0,1,1,0,1,1], [1,2,3,4,5])
    parent2 = ([1,1,1,1,0,0,0,0], [1,5,4,3,2])
    parents.append(parent1)
    parents.append(parent2)
    print('parents')
    print(parents)

    offsprings = crossover(parents)
    print('offsprings')
    print(offsprings)


if __name__ == "__main__":
    main()