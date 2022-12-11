
#Libraries
#import FITNESS2
import numpy as np
import pandas as pd
import math
import random


file_name='a280-n279.txt'

#global vars
#constanst of current problem
global dict_constants

#nodes dataframe containing index and coors /used to decode solution
global nodes_df
#items df containing index, profit weight and assigned node /used to decode solution
global items_df

global population


global number_of_nodes
global number_of_items
global max_nodes
global fitnesess
global detailed_fitnesess
global number_fitness_eval


pop_size=200
tournament_size=4
mutation_rate=10
SEED=4



def read_data(file_name):
    global dict_constants, nodes_df, items_df, number_of_nodes, number_of_items, max_nodes

    dict_constants={}

    #read txt file on absolute path
    with open(f"/home/sebastian/Documents/EXETER/Nature_inspired_computation/pyprojects/Coursework2/gecco19-thief-master/src/main/resources/{file_name}") as raw:
        data = raw.read()
        nodes_pos=data.split('ITEMS SECTION')[0]
        items_vals = data.split('ITEMS SECTION')[1]

        #CONSTANTS
        for global_features in nodes_pos.split('\n')[2:8]:
            temp = global_features.split('\t')
            var_name = temp[0].replace((':'),' ').strip()
            var_val = temp[1]
            dict_constants[var_name] = float(var_val)

        #NODES POSTIONS
        all_nodes_list = []
        for vals in nodes_pos.split('\n')[10:-1]:
            temp = vals.split('\t')
            temp = [float(t) for t in temp]
            all_nodes_list.append(temp)

        nodes_df = pd.DataFrame(all_nodes_list, columns=['node_index', 'x_coor', 'y_coor'])
        nodes_df['node_index'] = nodes_df['node_index'].astype('int')


        #ITEMS
        all_items_list = []
        for vals in items_vals.split('\n')[1:-1]:
            temp = vals.split('\t')
            temp = [float(t) for t in temp]
            all_items_list.append(temp)

        items_df = pd.DataFrame(all_items_list, columns=['item_index','profit','weight','assigned_node'])
        items_df['item_index']= items_df['item_index'].astype('int')
        items_df['assigned_node'] = items_df['assigned_node'].astype('int')

    #close file
    raw.close()

    number_of_nodes=int(dict_constants['DIMENSION'])
    number_of_items = int(dict_constants['NUMBER OF ITEMS'])
    max_nodes = int(dict_constants['DIMENSION'])

def get_weakest(fitnesses):
    #return index of worst fitnes
    return np.argmax(fitnesses)

def generate_random_initial_population_knappsack(pop_size,dimension):
    global number_fitness_eval #set global var

    #start at zero evals
    number_fitness_eval=0

    #population list
    population = []

    #use numpy random int between 0-1 to create solutions with size of number of bags [0,1,0,0,1.....] to 100
    for i in range(0, pop_size):
        actual_sol = np.random.randint(2, size=int(dimension))
        population.append(actual_sol)

    return population

def generate_random_initial_population_TSP(pop_size,number_nodes, max_nodes):

    population = []
    #use numpy random solutions with size of number of nodes [1,2,3,280.....] to number of nodes
    for i in range(0, pop_size):
        actual_sol = np.random.choice(range(2,int(number_nodes)+1), int(max_nodes-1), replace=False)
        actual_sol=np.insert(actual_sol, 0, 1)
        population.append(actual_sol)

    return population

def create_init_pop():
    global population, dict_constants, number_of_nodes, number_of_items
    final_pop=[]
    initial_KN=generate_random_initial_population_knappsack(pop_size,number_of_items)
    initial_TSP=generate_random_initial_population_TSP(pop_size,number_of_nodes,max_nodes)

    for i in range(len(initial_KN)):
        final_pop.append((initial_KN[i],initial_TSP[i]))

    population=final_pop

def e_distance(point_1, point_2):
    distance = math.sqrt((point_2[1] - point_1[1]) ** 2 + (point_2[2] - point_1[2]) ** 2)
    return distance

def travelling_thief(check):
    TSP = check[1]
    #it is assumed TSP begins at node 1
    #if not, please contact the person who provided the TSP!
    #TSP = [1,x,y,...,a,b]
    #len(TSP) = len(nodes_df)
    knapsack = check[0]

    bag_locations = [[]]

    for i in range (int(dict_constants['DIMENSION'])):
        bag_locations.append([])
    #look through all bags
    for i in range (len(items_df)):
    #assign to position in array which node they are at
        bag_locations[items_df['assigned_node'][i]].append(i)
    #this will give a 2D array with an empty 1 index (node 1 has no items)
    #also an empty 0 index (node 0 does not exist)

    bag_weight = 0
    total_value = 0
    time = 0
    #for len(TSP solution)
    for i in range(len(TSP)):
        #if current node is not last in TSP solution
        if i < (len(TSP)-1):
            #find distance from node just visited to new node
            j = TSP[i]-1
            point1 = [TSP[i],nodes_df['x_coor'][j],nodes_df['y_coor'][j]]
            k = TSP[(i+1)]-1
            point2 = [TSP[k],nodes_df['x_coor'][k],nodes_df['y_coor'][k]]
            #COMMENT sssssspeed = 1-(weight of bag/max bag weight)
            speed = 1 - (bag_weight/dict_constants['CAPACITY OF KNAPSACK'])
            #if speed < min speed
            if speed < dict_constants['MIN SPEED']:
                #speed = min speed
                speed = dict_constants['MIN SPEED']
            #time = distance*(1/speed)
            time += e_distance(point1,point2)*(1/speed)

            #for len(items at new node)
            items_at_location = bag_locations[TSP[i+1]]
            for j in range(len(items_at_location)):
                #check if item taken
                if knapsack[items_at_location[j]] == 1:
                    #if item taken
                    #add item weight to weight of bag
                    bag_weight += items_df['weight'][items_at_location[j]]
                    #add item value to total value
                    total_value += items_df['profit'][items_at_location[j]]

        #else
        else:
            #find distance from node just visited to new node
            j = TSP[i]-1
            point1 = [TSP[i],nodes_df['x_coor'][j],nodes_df['y_coor'][j]]
            k = TSP[0]-1
            point2 = [TSP[k],nodes_df['x_coor'][k],nodes_df['y_coor'][k]]
            #speed = 1-(weight of bag/max bag weight)
            speed = 1 - (bag_weight/dict_constants['CAPACITY OF KNAPSACK'])
            #if speed < min speed
            if speed < dict_constants['MIN SPEED']:
                #speed = min speed
                speed = dict_constants['MIN SPEED']
            #time = distance*(1/speed)
            time += e_distance(point1,point2)*(1/speed)

    #CHECK VALIDITY
    if bag_weight > dict_constants['CAPACITY OF KNAPSACK']:
        return math.inf, 0

    return time, total_value

#fitness function(TSP, Knapsack)
def fitness_function(to_check):
    global number_fitness_eval
    #time, value = Travelling Thief(TSP,Knapsack)
    total_time, profit = travelling_thief(to_check)

    #print('TIME',round(total_time,2))
    #print('Value',profit)
    #f = time - value
    f = total_time - profit

    #print('FINAL FIT', f)
    #return f
    number_fitness_eval=number_fitness_eval+1
    return f, total_time,profit

def evaluate_fitness_initial_pop():
    global population, fitnesess, detailed_fitnesess
    fitnesess=[]
    detailed_fitnesess=[]
    #FITNESS2.fitness_calculation(population[0], nodes_df, items_df, dict_constants)
    for p in population:
        f, total_time, profit=fitness_function(p)
        fitnesess.append(f)
        detailed_fitnesess.append((total_time,profit))

def perform_tournament_selection(tournament_size, population, fitnesses):
    # how many candidates per tournament
    times=tournament_size

    #candidates and their fitneses
    candidates=[]
    condidates_fitnesess=[]

    while times>0:
        #random choice to select index of a candidate from population
        random_sol_index=np.random.choice(len(population), 1)[0]
        #get candidate
        candidates.append(population[random_sol_index])
        #get candidate fitness
        condidates_fitnesess.append(fitnesses[random_sol_index])
        times=times-1

    #winner is candidate with higher fitness
    winner=max(condidates_fitnesess)
    #get candidate with winner fitnes
    winner_index = condidates_fitnesess.index(winner)

    #return candidate (actual pointer to population not a copy)
    return candidates[winner_index]


def mutation(child1, child2, rate):
    a1, a2 = child1, child2
    bag_dis_1, city_route_1, bag_dis_2, city_route_2 = a1[0].copy(), a1[1].copy(), a2[0].copy(), a2[1].copy()
    mutation_rate_1 = math.ceil((rate / 100) * len(bag_dis_1))
    mutation_rate_2 = math.ceil((rate / 100) * len(city_route_1))
    #print(mutation_rate_2)
    #print(mutation_rate_1)

    for i in range(mutation_rate_1):
        mutation_point_bag_1 = random.randint(0, len(bag_dis_1) - 1)  # bag selection mutation
        #print(mutation_point_bag_1)
        bag_dis_1[mutation_point_bag_1] = random.randint(0, 1)

        mutation_point_bag_2 = random.randint(0, len(bag_dis_2) - 1)  # bag selection mutation
        #print(mutation_point_bag_2)
        bag_dis_2[mutation_point_bag_2] = random.randint(0, 1)

    for j in range(mutation_rate_2):
        rand_1 = random.sample(range(1, len(city_route_1) - 1),
                               2)  # random values to generate the indexes of the route to be swapped
        city_route_1[rand_1[0]], city_route_1[rand_1[1]] = city_route_1[rand_1[1]], city_route_1[rand_1[0]]

        rand_2 = random.sample(range(1, len(city_route_2) - 1),
                               2)  # random values to generate the indexes of the route to be swapped
        city_route_2[rand_2[0]], city_route_2[rand_2[1]] = city_route_2[rand_2[1]], city_route_2[rand_2[0]]

    return (bag_dis_1, city_route_1), (bag_dis_2, city_route_2)


# hypervolume
def dominate(point1, point2):
    if point1[0] < point2[0] and point1[1] > point2[1]:
        return True
    elif point1[0] < point2[0] and point1[1] == point2[1]:
        return True
    elif point1[0] == point2[0] and point1[1] > point2[1]:
        return True
    else:
        return False


# takes the file_name, and an array of tuples containing Time and Value of all final solutions
def Hypervolume(file_name, TTP_results):
    if file_name == 'a280-n279.txt':
        ideal = [2613, 42036]
        nadir = [5444, 0]
    elif file_name == 'a280_n1395.txt':
        ideal = [2613, 489194]
        nadir = [6573, 0]
    elif file_name == 'a280_n2790.txt':
        ideal = [2613, 1375443]
        nadir = [6646, 0]
    elif file_name == 'fnl4461_n4460.txt':
        ideal = [185359, 645150]
        nadir = [442464, 0]
    elif file_name == 'fnl4461_n22300.txt':
        ideal = [185359, 7827881]
        nadir = [452454, 0]
    elif file_name == 'fnl4461_n44600.txt':
        ideal = [185359, 22136989]
        nadir = [459901, 0]
    elif file_name == 'pla33810_n33809.txt':
        ideal = [66048945, 4860715]
        nadir = [168432301, 0]
    elif file_name == 'pla33810_n169045.txt':
        ideal = [66048945, 59472432]
        nadir = [169415148, 0]
    elif file_name == 'pla33810_n338090.txt':
        ideal = [66048945, 168033267]
        nadir = [168699977, 0]

    area = ideal[1] * (nadir[0] - ideal[0])

    # get non-dominated set
    non_dominated_set = []
    for i in range(len(TTP_results)):
        dominated = False
        for j in range(len(TTP_results)):
            if dominated == False:
                dominated = dominate(TTP_results[j], TTP_results[i])
        if dominated == False:
            non_dominated_set.append(TTP_results[i])

    def sort_key(item):
        return item[0]

    non_dominated_set.sort(key=sort_key)

    set_area = 0
    for i in range(len(non_dominated_set)):
        if i == 0:
            # from value to nadir
            set_area += non_dominated_set[i][1] * (nadir[0] - non_dominated_set[i][0])
        else:
            # from value to [nadir x, previous y]
            set_area += (non_dominated_set[i][1] - non_dominated_set[i - 1][1]) * (nadir[0] - non_dominated_set[i][0])

    for i in range(len(non_dominated_set)):
        non_dominated_set[i][1] = non_dominated_set[i][1] * -1
    hv = set_area / area
    return hv, non_dominated_set, ideal, nadir


def main():
    global number_fitness_eval, SEED #use global var

    number_fitness_eval=0

    #SET SEED FOR REPLICATION PURPOSES
    np.random.seed(SEED)

    #read bag data from file #detailed comments on function
    read_data(file_name)

    #create initial population #detailed comments on function
    create_init_pop()

    #evaluate each solution fitness on initial pop, creating the fitness array #detailed comments on function
    evaluate_fitness_initial_pop()


    #print arguments
    print('STARTING EXPERIMENT:\n')
    print('Number of nodes', number_of_nodes)
    print('Number of items', number_of_items)
    print('Population Size', len(population))
    print('Tournament Size', tournament_size)
    print('Mutation rate %', mutation_rate)

    print('*****************************\n'
          '*****************************\n')


    #keep generation count
    generation=0

    #do while fitness evals <10000
    while number_fitness_eval<10000:

        #select parent a from tournament
        parent_a = perform_tournament_selection(tournament_size, population, fitnesess)

        #select parent b from tournament
        parent_b = perform_tournament_selection(tournament_size, population, fitnesess)

        #generate random locus to cross parents
        #locus = np.random.choice(len(parent_a), 1)[0]

        # #perform crossover on that locus
        # child_c, child_d = perform_crossover(parent_a, parent_b, locus)


        child_e, child_f = mutation(parent_a, parent_b, mutation_rate)
        # Evaluate child 1 fitness
        child_e_fitness, child_e_time,child_e_profit = fitness_function(child_e)

        #find index of actual weakest member of pop
        actual_weakest_index = get_weakest(fitnesess)
        #if child has better fitness replace in population AND on fitness array
        if child_e_fitness <= fitnesess[actual_weakest_index]:
            population[actual_weakest_index] = child_e
            fitnesess[actual_weakest_index] = child_e_fitness
            detailed_fitnesess[actual_weakest_index]=(child_e_time,child_e_profit)


        # Evaluate child 2 fitnes
        child_f_fitness, child_f_time,child_f_profit = fitness_function(child_f)
        # find index of actual weakest member of pop
        actual_weakest_index = get_weakest(fitnesess)
        # if child has better fitness replace in population AND on fitness array
        if child_f_fitness <= fitnesess[actual_weakest_index]:
            population[actual_weakest_index] = child_f
            fitnesess[actual_weakest_index] = child_f_fitness
            detailed_fitnesess[actual_weakest_index] = (child_f_time, child_f_profit)

        if(generation % 1000) == 0:
            #print iteration status
            print('Current Generation',generation)
            print('Current Evaluation', number_fitness_eval)
            print('Current Average Fitness ', np.average(fitnesess))
            print('Current Best Fitness ', np.min(fitnesess))

            print('Current Best time, value ', detailed_fitnesess[np.argmin(fitnesess)])
            print('*********************************')
            print()

        generation = generation + 1

    #FIND BEST SOL
    best_sol_index=np.argmin(fitnesess)

    best_solution=population[best_sol_index]
    best_fitness=fitnesess[best_sol_index]
    best_time_value=detailed_fitnesess[best_sol_index]


    print('Termination Criteria reached -> Fitness Eval #',number_fitness_eval)
    print()
    print(best_solution)
    print(best_fitness)
    print(best_time_value)


    print('HYPER VOLUME')
    Hypervolume(file_name,[[t[0],t[1]] for t in detailed_fitnesess])
    print('***********************')

    #return w,v,fitnesses[best_sol_index],np.average(fitnesses),list(s.keys())



if __name__ == '__main__':
    main()

