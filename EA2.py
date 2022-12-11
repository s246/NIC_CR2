
#Libraries
import re
import numpy as np
import pandas as pd
import random


file_name='a280-n279.txt'

#global vars
global dict_constants #constanst of current problem
global nodes_df
global items_df
global initial_pop


global number_of_nodes
global number_of_items
global max_nodes


pop_size=20




def read_data(file_name):
    global dict_constants, nodes_df, items_df, number_of_nodes, number_of_items, max_nodes

    dict_constants={}

    #read txt file on absolute path
    with open(f"./{file_name}") as raw:
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


read_data(file_name)
create_final_pop()
