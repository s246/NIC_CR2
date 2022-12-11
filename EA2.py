
#Libraries
#import FITNESS2
import numpy as np
import pandas as pd
import math
import itertools


file_name='a280-n279.txt'

#global vars
global dict_constants #constanst of current problem
global nodes_df
global items_df
global initial_pop


global number_of_nodes
global number_of_items
global max_nodes
global fitnesess
global detailed_fitnesess


pop_size=200




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

def create_final_pop():
    global initial_pop, dict_constants, number_of_nodes, number_of_items
    final_pop=[]
    initial_KN=generate_random_initial_population_knappsack(pop_size,number_of_items)
    initial_TSP=generate_random_initial_population_TSP(pop_size,number_of_nodes,max_nodes)

    for i in range(len(initial_KN)):
        final_pop.append((initial_KN[i],initial_TSP[i]))

    initial_pop=final_pop

    def e_distance(point_1, point_2):
        distance = math.sqrt((point_2[1] - point_1[1]) ** 2 + (point_2[2] - point_1[2]) ** 2)
        return distance

    def travelling_thief(check):
        TSP = check[1]
        # it is assumed TSP begins at node 1
        # if not, please contact the person who provided the TSP!
        # TSP = [1,x,y,...,a,b]
        # len(TSP) = len(nodes_df)
        knapsack = check[0]

        bag_locations = [[]]

        for i in range(int(dict_constants['DIMENSION'])):
            bag_locations.append([])
        # look through all bags
        for i in range(len(items_df)):
            # assign to position in array which node they are at
            bag_locations[items_df['assigned_node'][i]].append(i)
        # this will give a 2D array with an empty 1 index (node 1 has no items)
        # also an empty 0 index (node 0 does not exist)

        bag_weight = 0
        total_value = 0
        time = 0
        # for len(TSP solution)
        for i in range(len(TSP)):
            # if current node is not last in TSP solution
            if i < (len(TSP) - 1):
                # find distance from node just visited to new node
                j = TSP[i] - 1
                point1 = [TSP[i], nodes_df['x_coor'][j], nodes_df['y_coor'][j]]
                k = TSP[(i + 1)] - 1
                point2 = [TSP[k], nodes_df['x_coor'][k], nodes_df['y_coor'][k]]
                # speed = 1-(weight of bag/max bag weight)
                speed = 1 - (bag_weight / dict_constants['CAPACITY OF KNAPSACK'])
                # if speed < min speed
                if speed < dict_constants['MIN SPEED']:
                    # speed = min speed
                    speed = dict_constants['MIN SPEED']
                # time = distance*(1/speed)
                time += e_distance(point1, point2) * (1 / speed)

                # for len(items at new node)
                items_at_location = bag_locations[TSP[i + 1]]
                for j in range(len(items_at_location)):
                    # check if item taken
                    if knapsack[items_at_location[j]] == 1:
                        # if item taken
                        # add item weight to weight of bag
                        bag_weight += items_df['weight'][items_at_location[j]]
                        # add item value to total value
                        total_value += items_df['profit'][items_at_location[j]]

            # else
            else:
                # find distance from node just visited to new node
                j = TSP[i] - 1
                point1 = [TSP[i], nodes_df['x_coor'][j], nodes_df['y_coor'][j]]
                k = TSP[0] - 1
                point2 = [TSP[k], nodes_df['x_coor'][k], nodes_df['y_coor'][k]]
                # speed = 1-(weight of bag/max bag weight)
                speed = 1 - (bag_weight / dict_constants['CAPACITY OF KNAPSACK'])
                # if speed < min speed
                if speed < dict_constants['MIN SPEED']:
                    # speed = min speed
                    speed = dict_constants['MIN SPEED']
                # time = distance*(1/speed)
                time += e_distance(point1, point2) * (1 / speed)

        # return time, total value
        return time, total_value

    # fitness function(TSP, Knapsack)
    def fitness_function(to_check):
        # time, value = Travelling Thief(TSP,Knapsack)
        total_time, profit = travelling_thief(to_check)
        # f = time - value
        f = total_time - profit
        # return f
        return f

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
            #speed = 1-(weight of bag/max bag weight)
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

    #return time, total value
    return time, total_value

#fitness function(TSP, Knapsack)
def fitness_function(to_check):
    #time, value = Travelling Thief(TSP,Knapsack)
    total_time, profit = travelling_thief(to_check)

    #print('TIME',round(total_time,2))
    #print('Value',profit)
    #f = time - value
    f = total_time - profit

    #print('FINAL FIT', f)
    #return f
    return f, total_time,profit


def evaluate_fitness_initial_pop():
    global initial_pop, fitnesess, detailed_fitnesess
    fitnesess=[]
    detailed_fitnesess=[]
    #FITNESS2.fitness_calculation(initial_pop[0], nodes_df, items_df, dict_constants)
    for p in initial_pop:
        f, total_time, profit=fitness_function(p)
        fitnesess.append(f)
        detailed_fitnesess.append((total_time,profit))


read_data(file_name)
create_final_pop()

evaluate_fitness_initial_pop()




