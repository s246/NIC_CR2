import numpy as np
import pandas as pd
import random as rd
from random import randint
import matplotlib.pyplot as plt
import os


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

    plt.scatter(df_pareto[0], df_pareto[1], s = 5, label = generattion)
    plt.title(resultfilename_fitness.split('/')[1])
    plt.xlabel('Time')
    plt.ylabel('Negative of profit')
    plt.legend()
