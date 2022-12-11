from EA2 import read_data
from euclidean_distance import eucledian_distance
from TSP import findMinRoute
import numpy as np

file_name = ['a280-n279.txt', 'a280-n1395.txt', 'a280-n2790.txt', 
            'fnl4461-n22300.txt', 'fnl4461-n4460.txt', 'fnl4461-n44600.txt', 
            'pla33810-n169045.txt', 'pla33810-n33809.txt', 'pla33810-n338090.txt', 
            'test-example-n4.txt']

def main():
    dict_constants, nodes_df, items_df = read_data(file_name[0])
    nodes = nodes_df.values.astype(int).tolist()
    ed_df, ed_matrix =  eucledian_distance(nodes)
   
    nodes_for_test = np.random.randint(2, 280, 4, dtype = int)
    nodes_for_test = np.insert(nodes_for_test, 0, 1)

    print('random nodes', nodes_for_test)

    dist = []
    for i in nodes_for_test:
        dist_from_i = []
        for j in nodes_for_test:
            dist_from_i.append(round(ed_matrix[i-1][j-1], 2))
        dist.append(dist_from_i)
        print(dist_from_i)

    # print(dist)

    sum = findMinRoute(dist)


if __name__ == "__main__":
    main()