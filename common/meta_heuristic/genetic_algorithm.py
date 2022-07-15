"""
--------------------------------------------------------------
- About
The genetic algorithms are used for problems where you have a very small probability of getting the correct answer for a specific question with brute force or you don't know a good optimization algorithm to solve the problem, these problems are named non polynomial (NP for short), where you can't have a quick answer (namely, in polynomial time).

Genetic algorithms are part of a group of algorithms named metaheuristic, that can provide a sufficiently good solution to an optimization problem.
--------------------------------------------------------------
- How it works
There are 3 main principles that it must to be followed: variation, heredity and selection.

To create variation, the setup function will generate a population with N random elements.

The selection is the fitness function wich will be calculated for each individual in the population, the fitness function will be specific for every problem. Then 2 individuals are choosen from the population with the probability attached to the fitness score.

The selected individuals will pass through a function to make the crossover, it means, generating a new individual with a mixed combination of the information of it's parents.

There is a probability that at the begining, not enought variation is created, and to solve this problem, after a new individual is generated, a mutation rate is aplied to it's information. This rate will be determined by the mean of the fitness of the population.

This process repeats until we have a new population with the same size of the previous population.
--------------------------------------------------------------
- How to use

"""
import random
import csv
import pandas as pd


# Default values
POPULATION_SIZE = 100
DNA_LENGTH = 20
DNA_START = 0
DNA_END = 0
FLOAT_NUMBERS = False


# Generic images for individuals and populations
class Individual:

    def __init__(self, sequence: list = []):
        self.sequence = sequence
        self.score = 0
        self.fitness = 0.00
    
    def newDNASequence(self, dna_length, dna_start, dna_end):
        "Generate a new random DNA sequence"
        dna = [random.uniform(dna_start, dna_end) for num in range(dna_length)]
        self.sequence = dna
    
    def calculateFitness(self) -> float:
        """rounds: 10, correct: 7, incorrect: 3, Fitness: 70%
        ---
        score: 
        """

    def mutation(self):
        pass

    def getSequenceOfDNA(self) -> list:
        return self.sequence


class Population:

    def __init__(self, database_location, filename, population_size, dna_length, dna_start, dna_end, float_numbers):
        self.database_location = database_location
        self.filename = filename
        self.population_size = population_size
        self.dna_length = dna_length
        self.dna_start = dna_start
        self.dna_end = dna_end
        self.float_numbers = float_numbers
        self.generation_number = 1
        self.rounds = 0
        self.meanFitness = 0.00
        self.individuals = []
    
    def initIndividuals(self):
        individuals = []
        for i in range(self.population_size):
            individual = Individual()
            individual.newDNASequence(self.dna_length, self.dna_start, self.dna_end)
            individuals.append(individual)
        self.individuals = individuals
    
    def calculatePopulationMeanFitness(self):
        fitness = 0
        for individual in self.individuals:
            fitness += individual.calculateFitness()
        fitness = round(fitness / self.population_size, 2)
        self.meanFitness = fitness
    
    def poolSelection(self):
        pass

    def crossover(self):
        pass

    def applyMutationRate(self):
        for individual in self.individuals:
            individual.mutation()

    # def refreshParameters(self, population_size: int = None, dna_length: int = None):
    #     "check the population size and the dna length of the saved population and ajust if necessary"
    #     df = pd.read_csv(f"{self.database_location}/{self.filename}.csv").shape
    #     self.population_size = df[0]
    #     self.dna_length = df[1]

    # def changePopulationSize(self, new_size: int):
    #     self.population_size = new_size

    # def changeDNALength(self, new_dna_length: int):
    #     self.dna_length = new_dna_length

    def savePopulationDNA(self):
        "Write in a csv file the population information"
        with open(f"{self.database_location}/{self.filename}.csx", 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            for individual in self.individuals:
                writer.writerow(individual.getSequenceOfDNA())


# Main functions to create and load populations
def initPopulation(database_location: str, filename: str, population_size: int = POPULATION_SIZE, dna_length: int = DNA_LENGTH, dna_end: float = DNA_END, dna_start: float = DNA_START, float_numbers: bool = FLOAT_NUMBERS) -> Population:
    """
    This function will start a new population wich is just a matrix of numbers, where each column represents a 'base pair' of the 'DNA' and the rows represent
    the individuals, the number of columns will be determined by the parameter 'dna_lenght' and the number of rows will be determined by 'population_size', the
    database_location is where the matrix will be stored. The dna_start and dna_end will be the range of numbers that can be generated, so if dna_start is = -5
    and dna_end = 5, the numbers will be generated only between -5 and 5. float_numbers by default is false, it means that only integer numbers will be generated, but
    it can be True as well.
    """

    new_population = Population(database_location, filename, population_size, dna_length, dna_start, dna_end, float_numbers)
    new_population.initIndividuals()

    return new_population


# def loadPopulation(database_location, filename, **kwargs) -> Population:
#     """
#     This function will receive the filename and location of the database of the population. Start a new population with default values, refresh the parameters to catch
#     the parameters from the actual database and then return the population. The size of the population ('population_size') and the dna ('dna_length') can be modified if
#     passed as named parameters.
#     """

#     loaded_population = Population(database_location, filename, POPULATION_SIZE, DNA_LENGTH, DNA_START, DNA_END, FLOAT_NUMBERS)
#     # in the case you want to load a database, but you want to change the parameters
#     # if kwargs['population_size'] or kwargs['dna_length']:
#     #     loaded_population.refreshParameters(population_size=kwargs['population_size'], dna_length=kwargs['dna_length'])
#     # else:
#     loaded_population.refreshParameters()

#     return loaded_population