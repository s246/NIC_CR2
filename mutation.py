import random

def mutation(child1, child2, rate):
    a1,a2 = child1,child2
    bag_dis_1, city_route_1, bag_dis_2, city_route_2 = a1[0], a1[1], a2[0], a2[1]
    mutation_rate_1 = int((rate/100)*len(bag_dis_1))
    mutation_rate_2 = int((rate/100)*len(city_route_1))

    for i in range(mutation_rate_1):
        mutation_point_bag_1 = random.randint(0, len(bag_dis_1)-1) # bag selection mutation
        bag_dis_1[mutation_point_bag_1] = random.randint(0,1)

        mutation_point_bag_2 = random.randint(0, len(bag_dis_2)-1) # bag selection mutation
        bag_dis_2[mutation_point_bag_2] = random.randint(0,1)

    
    for j in range(mutation_rate_2): 
        rand_1 = random.sample(range(1, len(city_route_1)-1), 2)  # random values to generate the indexes of the route to be swapped
        city_route_1[rand_1[0]], city_route_1[rand_1[1]] = city_route_1[rand_1[1]], city_route_1[rand_1[0]]

        rand_2 = random.sample(range(1, len(city_route_2)-1), 2)  # random values to generate the indexes of the route to be swapped
        city_route_2[rand_2[0]], city_route_2[rand_2[1]] = city_route_2[rand_2[1]], city_route_2[rand_2[0]]
    
    return bag_dis_1, city_route_1, bag_dis_2, city_route_2