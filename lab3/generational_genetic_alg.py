import numpy as np
import time
import matplotlib.pyplot as plt

"""
Implementing Generational Genetic Algorithm to optimize Booth Function :  f(x,y) = (x+2y−7)^2 + (2x+y−5)^2
"""


# Define the booth function to be optimized
def booth_function(x, y):
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2


# Define the function to initialize the population
def populate(range_min, range_max, pop_size):
    # randomly select (x,y) pairs from a uniformly distributed range of (range_min, range_max)
    population = np.random.uniform(range_min, range_max, size=(pop_size, 2))
    return population


# Define a function to evaluate the fitness of each individual in the population
def evaluate_fitness(population):
    fitness_values = []
    for individual in population:
        # We use negative of booth_function for every individual to calculate their fitness
        # Because we are trying to find the individual that minimizes the function best
        fitness_values.append(-booth_function(*individual))
    return np.array(fitness_values)


# Define a function to select the parents for the next generation
# Fitness Proportional Selection (Roulette Wheel) method is used
def select_parents(population, fitness_values, pop_size):
    fitness_values = np.exp(fitness_values - np.max(fitness_values))
    fitness_values = fitness_values / np.sum(fitness_values)  # deriving probability to be selected from fitness values
    selected_indices = np.random.choice(range(pop_size), size=pop_size, replace=True, p=fitness_values)
    return population[selected_indices]


# Define a function to apply the mutation operator to an individual
def mutate(individual, mutation_prob, mutation_strength):
    mutated_individual = individual.copy()
    for i in range(len(individual)):
        if np.random.rand() < mutation_prob:
            mutated_individual[i] += np.random.normal(0, mutation_strength)
    return mutated_individual


# Define a function to apply the crossover operator to a pair of parents
# alpha -> weight of parent affecting its children
def crossover(parent1, parent2):
    child = np.zeros(2)  # initialize children
    alpha = np.random.rand()  # get a random weight
    child[0] = alpha * parent1[0] + (1 - alpha) * parent2[0]
    child[1] = alpha * parent1[1] + (1 - alpha) * parent2[1]
    return child


def main():
    # Get the range of values from user from which the population will be initialized
    range_min = float(input("Enter the minimum value for the range (default: -10) : "))
    range_max = float(input("Enter the maximum value for the range (default: 10) : "))

    # Get the population size from user
    pop_size = int(input("Enter the population size: "))

    # Get the number of generations from user
    while True:
        num_generations = int(input("Enter the number of generations (must be a positive integer): "))
        if num_generations > 0:
            break
        print("Invalid input. Please enter a positive integer.")

    # Get the mutation probability from user and limit it to be between 0 and 1
    while True:
        mutation_prob = float(input("Enter the mutation probability (between 0 and 1): "))
        if 0 <= mutation_prob <= 1:
            break
        print("Invalid input. Please enter a value between 0 and 1.")

    # Get the mutation strength from user
    mutation_strength = float(input("Enter the mutation strength: "))

    # Create a list to store the best fitness value of each generation
    best_fitness_values = []

    # Get the population
    population = populate(range_min, range_max, pop_size)

    # Start the optimization process
    start_time = time.time()

    for i in range(num_generations):
        # Evaluate the fitness of the population
        fitness_values = evaluate_fitness(population)
        best_fitness_values.append(np.max(fitness_values))

        # Select the parents for the next generation
        parents = select_parents(population, fitness_values, pop_size)

        # Create the next generation
        next_generation = np.zeros((pop_size, 2))
        for j in range(pop_size):
            # Get parents from those selected before
            parent1 = parents[np.random.randint(pop_size)]
            parent2 = parents[np.random.randint(pop_size)]
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_prob, mutation_strength)
            next_generation[j] = child

        # Replace the current generation with the next generation
        population = next_generation

    # End of the optimization process
    end_time = time.time()

    # Print the best solution found
    best_individual = population[np.argmax(fitness_values)]
    best_fitness = np.max(fitness_values)
    print("Best solution found: x = {}, y = {}, f(x,y) = {}".format(best_individual[0], best_individual[1],
                                                                    -best_fitness))

    # Print the optimization time
    optimization_time = end_time - start_time
    print("Optimization time: {:.2f} seconds".format(optimization_time))

    # Plot the best fitness value of each generation
    plt.plot(range(num_generations), best_fitness_values)
    plt.title('Best Fitness Values Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best fitness value')
    plt.show()


# Run the program
main()
