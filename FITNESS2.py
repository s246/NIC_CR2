
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd


def eul_dis(node1, node2):  # Calculation of Euclidean distance
    # print(node1['x_coor'].iloc[0])
    # print(node1)
    dis = (((node1['x_coor'].iloc[0] - node2['x_coor'].iloc[0]) ** 2) + (
                (node1['y_coor'].iloc[0] - node2['y_coor'].iloc[0]) ** 2)) ** 0.5
    # print(dis,'dis')
    return (dis)


def cul_dis(node, n_df):  # Calculate the length of each path
    dis_df = pd.DataFrame(np.zeros(len(node['node_index'])))
    # print(dis_df)
    # print(n_df.iloc[7])
    j = 0
    for i in range(len(node['node_index'])):
        # print(node['node_index'][i])
        if i != len((node['node_index'])) - 1:
            # print(i)
            node1 = n_df.loc[n_df['node_index'] == node['node_index'][i]]
            node2 = n_df.loc[n_df['node_index'] == node['node_index'][i + 1]]
            dis_df[0].iloc[j] = eul_dis(node1, node2)
            # print(dis_df)
            j += 1
        else:
            node1 = n_df.loc[n_df['node_index'] == node['node_index'][i]]
            node2 = n_df.loc[n_df['node_index'] == node['node_index'][0]]
            dis_df[0].iloc[j] = eul_dis(node1, node2)
            j += 1
    # print(dis_df)
    return (dis_df)


def cul_weight_speed_profit(node, new_i_df, min_sp, max_sp,
                            capacity):  # Calculate the weight, profit and speed after passing each point
    wei_df = pd.DataFrame(np.zeros(len(node['node_index'])))
    pro_df = pd.DataFrame(np.zeros(len(node['node_index'])))
    node['weight'] = wei_df
    node['profit'] = pro_df

    for i in range(len(new_i_df)):
        node_index = node[node['node_index'] == new_i_df['assigned_node'].iloc[i]].index[0]

        node['weight'][node_index] += new_i_df['weight'].iloc[i]
        node['profit'][node_index] += new_i_df['profit'].iloc[i]

    node['cumsum_w'] = node['weight'].cumsum(axis=0)
    node['cumsum_p'] = node['profit'].cumsum(axis=0)
    node['speed'] = node['cumsum_w'].map(lambda x: max_sp - (x / capacity * (max_sp - min_sp)))
    node.loc[node['speed'] < min_sp, 'speed'] = min_sp
    # print(node)
    return (node)


def cul_time(node, n_df, item, i_df, min_sp, max_sp, capacity):  # Calculate the time traveled on each road
    # print(node)
    # print(n_df)
    # print(item)
    # print(i_df)
    #print(min_sp, max_sp, capacity)
    di_df = cul_dis(node, n_df)
    node['distance'] = di_df
    i_df['item'] = item
    new_i_df = i_df.copy()
    new_i_df = new_i_df[new_i_df['item'] != 0]
    #print(new_i_df)
    node = cul_weight_speed_profit(node, new_i_df, min_sp, max_sp, capacity)
    node['time'] = node.apply(lambda x: x['distance'] / x['speed'], axis=1)
    #print(node)
    return (node)


def cul_fitness(node):  # Calculate the fitness.

    # Normalize time and profit to reduce errors caused by data size gaps.
    time_max = node['time'].max()
    time_min = node['time'].min()
    node['normal_time'] = node['time'].map(lambda x: (x - time_min) / (time_max - time_min))
    pro_max = node['profit'].max()
    pro_min = node['profit'].min()
    node['normal_profit'] = node['profit'].map(lambda x: (x - pro_min) / (pro_max - pro_min))

    # Fitness at each point is the result of profit minus time.
    node['fitness'] = node.apply(lambda x: x['normal_profit'] - x['normal_time'], axis=1)
    #print(node)

    # Total fitness is the sum of all individual fitness.
    total_fitness = node['fitness'].sum()
    #print(total_fitness, 'total_fitness')
    return total_fitness



def fitness_calculation(a, nodes_df, items_df, dict_constants):
    # random_item, random_node = generate_random(items_df, nodes_df)

    b = {"node_index": a[1]}
    random_node = pd.DataFrame(b)
    random_node.columns = ['node_index']
    random_item = a[0]

    new_node = cul_time(random_node, nodes_df, random_item, items_df, dict_constants['MIN SPEED'],
                        dict_constants['MAX SPEED'], dict_constants['CAPACITY OF KNAPSACK'])
    total_fitness = cul_fitness(new_node)

    return total_fitness



def main():
    return None

if __name__ == '__main__':
    main()