import numpy as np
import pandas as pd
import random as rd
from random import randint
import matplotlib.pyplot as plt
import os
import math
import itertools



def save_to_file(file_name, detailed_fitnesess, population): 
    # Printing fitness for last gen
    file_name_without_ext = os.path.splitext('{}'.format(file_name))[0]
    resultfilename_fitness = 'Results/{}/fitness_evals.txt'.format(file_name_without_ext)
    os.makedirs(os.path.dirname(resultfilename_fitness), exist_ok=True)

    with open(resultfilename_fitness, 'w') as f:
        for fitness in detailed_fitnesess:
            f.writelines("{} {}\n".format(fitness[0], fitness[1]))

    # Printing population for last gen
    resultfilename_pop = 'Results/{}/pop.txt'.format(file_name_without_ext)
    os.makedirs(os.path.dirname(resultfilename_pop), exist_ok=True)

    with open(resultfilename_pop, 'w') as f:
        for pop in population:
            for p in pop[1]:
                f.writelines("{} ".format(p))
            f.writelines("\n")
            for p in pop[0]:
                f.writelines("{} ".format(p))
            f.writelines("\n\n")


def plot_time_vs_profit(file_name, generattion):
    file_name_without_ext = os.path.splitext('{}'.format(file_name))[0]
    resultfilename_fitness = 'Results/{}/fitness_evals.txt'.format(file_name_without_ext)

    df = pd.read_csv(resultfilename_fitness, sep=" ", header=None)
    pareto_list = []

    for i, row_i in df.iterrows():
        is_dominant = True
        for j, row_j in df.iterrows():
            if i != j:
                if df.loc[j][0] < df.loc[i][0] and df.loc[j][1] > df.loc[i][1]:
                    is_dominant = False
        
        if is_dominant == True:
            pareto_list.append(row_i)

    df_pareto = pd.DataFrame(pareto_list, columns=[0,1])
    df_pareto[1] = df_pareto[1]*(-1)

    plt.scatter(df_pareto[0], df_pareto[1], s = 5, label = "{} gen".format(generattion))
    plt.title(resultfilename_fitness.split('/')[1])
    plt.xlabel('Time')
    plt.ylabel('Negative of profit')
    plt.legend()

def calculate_distance(point_1,point_2):
    distance = math.sqrt((point_2[1] - point_1[1])**2 + (point_2[2] - point_1[2])**2)
    return distance 

def eucledian_distance(nodes_list):
    main_list = [] 
    b = list(itertools.permutations(nodes_list,2))
    for i in b:
        elements_list = []
        point1 = i[0]
        point2 = i[1]
        distance = calculate_distance(point1, point2)
        elements_list.extend((int(point1[0]),int(point2[0]),distance))
        main_list.append(elements_list)

    for i in range(1,int(nodes_list[-1][0])+1):
        lst_1 = []
        lst_1.extend((int(i),int(i),float(0)))
        main_list.append(lst_1)

    df = pd.DataFrame(main_list, columns=['Source','Destination','Distance'])
    df = df.sort_values(by=['Source','Destination']).reset_index(drop=True)

    distance_list = df['Distance'].tolist()
    x = np.array(distance_list)
    shape = (len(nodes_list),len(nodes_list)) 
    distance_matrix = x.reshape(shape)
    
    return distance_matrix

