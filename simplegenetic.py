"""
Genetic Alogorithm 
problem is a list on n numbers with sum 
 sum = target 
eg : N=5 sum=200
solutions
lst = [40,40,40,40,40]
lst = [50,50,50,25,25]
lst = [200,0,0,0,0]
"""

from random import randint, random
from operator import add
from functools import reduce

#Individuals in our population

def individual(length, min, max):
    'Create a member of the population.'
    return [ randint(min,max) for x in range(length) ]

#The collection of all individuals is referred to as our population.
def population(count, length, min, max):
     """  
       Create a number of individuals (i.e. a population).
       count: the number of individuals in the population
       length: the number of values per individual
       min: the min possible value in an individual's list of values
       max: the max possible value in an individual's list of values
 
    """
     return [ individual(length,min,max) for x in range(count)]

"""
We need to calcualte fitness of each individual.
Fitness function will do this trick
"""
def fitness(individual, target):
   """
     Determine the fitness of an individual. Lower is better.
     individual: the individual to evaluate
      target: the sum of numbers that individuals are aiming for
   """
   sum = reduce(add, individual, 0)
   return abs(target-sum)

#population's average fitness.
def grade(pop, target):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x, target) for x in pop), 0)
    return summed / (len(pop) * 1.0)

"""
EVOLUTION
selecting parents -> low fitness
add some individuals
mutate parents
determine child length and breed
"""
def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [ (fitness(x, target), x) for x in pop] #[(71, [34, 32, 72, 58, 75]), (50, [62, 10, 52, 33, 93])... 
    graded = [ x[1] for x in sorted(graded)] # sort based on fitness (asending) lowest value is best
    print("sorted:")
    print(graded)
    retain_length = int(len(graded)*retain) #Nummber of individuals to retain 
    parents = graded[:retain_length]
    print("Retain length :"+str(retain_length))
    
    
    #randomly add other individuals to promote genetic diversity 
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            print("position to mutate")
            print(pos_to_mutate)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length #number of children=len of pop -len of parents
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) / 2
            child = male[:int(half)] + female[int(half):]
            children.append(child)
            
    parents.extend(children)
    print (parents)
    return parents
    

target = 200
p_count = 100
indiv_length = 5
indiv_min = 0
indiv_max = 100
p = population(p_count, indiv_length, indiv_min, indiv_max)
fitness_history = [grade(p, target),]
for i in range(100):
    p=evolve(p,target)
    fitness_history.append(grade(p, target))
    

for datum in fitness_history:
    print (datum)
print("Final Population :")
print(p)
