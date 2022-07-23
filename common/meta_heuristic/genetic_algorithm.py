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

Call the function initPopulation passing the database location, the filename, population size, DNA lenght and the DNA start and DNA end, this will return an object of the class Population.

Note: if you already have a database, call the function loadPopulation() passing the database location and the filename, then the program will automatically search for the other parameters and return a Population object.

To add a score for the individuals, call the function addIndividualScore() passing as a parameter a list with the score of each individual and a list with the maximum score that this individual could get in that round, the function then will update the round number.

When all the individuals have updated their score, then call the function calculatePopulationMeanFitness() to get the updated value of the fitess of the population and to update the index of the best individual of the population.

if you want to create a new generation, call the function newGeneration()

to save the DNA of the population call the function savePopulationDNA()

Note: after initializing the population, updating the DNA lenght or the population size, wait until a new score was added for the individuals before calling the function to calculate population fitness or to generate a new population.

Note: don't call change DNA size or population lenght before savePopulationDNA at least one time.
"""
# - [X] Carregar algoritmos genéticos a partir de arquivos
# - [X] Salvar outras informações em arquivo de mesmo nome a parte (melhor indivíduo, número da geração, número de rounds)
# - [X] Mudar o tamanho da população e do DNA
# - [X] Criar código para organizar os arquivos na hora de salvar
# - [ ] Atualizar os testes necessários

import random
import csv
import pandas as pd
from datetime import datetime

# print(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))

# Default values
POPULATION_SIZE = 100
DNA_LENGTH = 20
DNA_START = 0
DNA_END = 1000
FLOAT_NUMBERS = False


# Generic classes for individuals and populations
class Individual:

    def __init__(self, sequence: list = []):
        self._sequence = sequence
        self._score = 0
        self._ideal_score = 0
        self._fitness = 0.00

    def newDNASequence(self, dna_length: int, dna_start: int, dna_end: int):
        "Generate a new random DNA sequence"
        if len(self._sequence) == 0:
            dna = [random.uniform(dna_start, dna_end) for num in range(dna_length)]
            self._sequence = dna
        else:
            dna_size = 0
            new_dna = []
            while dna_size < dna_length:
                if dna_size <= len(self._sequence):
                    new_dna.append(self._sequence[dna_size])
                else:
                    new_dna.append(random.uniform(dna_start, dna_end))
                dna_size += 1
            self._sequence = new_dna

    def setScore(self, score: int, ideal_score: int):
        self._score += score
        self._ideal_score += ideal_score

    def calculateFitness(self) -> float:
        self._fitness = (self._score / self._ideal_score) ** 2
        return self._fitness

    def mutation(self):
        new_sequence = []
        i = 0
        while i < len(self._sequence):
            new_sequence.append(self._sequence[i] + random.uniform(-2, 2))
            i += 1
        self._sequence = new_sequence

    def getSequenceOfDNA(self) -> list:
        return self._sequence

    def getFitness(self) -> float:
        return self._fitness


class Population:

    def __init__(self, database_location, filename, population_size, dna_length, dna_start, dna_end):
        self.database_location = database_location
        self.filename = filename
        self.population_size = population_size
        self.dna_length = dna_length
        self.dna_start = dna_start
        self.dna_end = dna_end
        self.creation = datetime.strftime(datetime.now(), '%Y%m%d%H%M')
        self.generation_number = 1
        self.rounds = 0
        self.sum_population_fitness = 0
        self.mutation_rate = 0.01
        self.meanFitness = 0.00
        self.parents1 = []
        self.parents2 = []
        self.individuals = []
        self.best_individual_index = -1
    
    def initIndividuals(self):
        """This function creates a new individual and save it in the population collection"""
        if self.dna_start != -1 and self.dna_end != -1:
            individuals = []
            for i in range(self.population_size):
                individual = Individual()
                individual.newDNASequence(self.dna_length, self.dna_start, self.dna_end)
                individuals.append(individual)
            self.individuals = individuals
    
    def addIndividualScore(self, score_individuals: list, score_ideal: list):
        """This function receives a list with the scores obtained by each individual and the total score that this individual should achieve to get a perfect score, then the number of rounds are updated"""
        i = 0
        while i < self.population_size:
            self.individuals[i].setScore(score_individuals[i], score_ideal[i])
            i += 1
        self.rounds += 1

    def calculatePopulationMeanFitness(self):
        self.sum_population_fitness = 0
        best_individual_fitness = 0
        for i in range(self.population_size):
            individual_fitness = self.individuals[i].calculateFitness()
            self.sum_population_fitness += individual_fitness
            if individual_fitness > best_individual_fitness:
                best_individual_fitness = individual_fitness
                self.best_individual_index = i
        self.meanFitness = round(self.sum_population_fitness / self.population_size, 2)
        return self.meanFitness
    
    def pickOne(self):
        """generate a random number between the maximum fitness and then subtract it with the fitness of the individuals, then returns the index when the score is bellow 0"""
        j = 0
        generated_number = random.uniform(0, self.sum_population_fitness)
        choosen_index = 0
        while j < len(self.individuals):
            generated_number -= self.individuals[j].getFitness()
            choosen_index = j
            if generated_number <= 0:
                break
            j += 1
        return choosen_index
    
    def poolSelection(self):
        """Choose parents with the probabillity of their fitness value"""
        i = 0
        while i < len(self.individuals):
            self.parents1.append(self.individuals[self.pickOne()])
            self.parents2.append(self.individuals[self.pickOne()])
            i += 1

    def crossover(self):
        """Take two parents and generate two new individuals with mixed DNA and append to the new populatin until it reaches the same size of the population size"""
        new_population = []
        i = 0
        while i < self.population_size // 2:
            parent1_DNA = self.parents1[i].getSequenceOfDNA()
            parent1_DNA = [parent1_DNA[0:len(parent1_DNA)//2], parent1_DNA[len(parent1_DNA)//2:]]
            parent2_DNA = self.parents2[i].getSequenceOfDNA()
            parent2_DNA = [parent2_DNA[0:len(parent2_DNA)//2], parent2_DNA[len(parent2_DNA)//2:]]

            individual1 = parent1_DNA[0] + parent2_DNA[1]
            individual2 = parent2_DNA[0] + parent1_DNA[1]

            new_individual1 = Individual(individual1)
            new_individual2 = Individual(individual2)
            new_population.append(new_individual1)
            new_population.append(new_individual2)
            i += 1
        self.individuals = new_population
    
    def getBestIndividual(self):
        return self.best_individual_index

    def applyMutationRate(self):
        for individual in self.individuals:
            mutate_prob = random.uniform(0, 1)
            if self.mutation_rate >= mutate_prob:
                individual.mutation()
    
    def newGeneration(self):
        self.calculatePopulationMeanFitness()
        self.poolSelection()
        self.crossover()
        self.applyMutationRate()
        self.generation_number += 1
    
    def getPopulationParameters(self):
        """New function to update the values for dna_start, dna_end, round number, generation number and best individual"""
        with open(f"{self.database_location}\\{self.creation}_{self.filename}.txt", 'r') as file:
            file_content = file.readlines()
            information = [line.replace('\n', '').split(': ')[1] for line in file_content]
            self.dna_start = information[0]
            self.dna_end = information[1]
            self.generation_number = information[2]
            self.rounds = information[3]
            self.best_individual_index = information[4]

    def refreshParameters(self):
        "check the population size and the dna length of the saved population and ajust if necessary"
        df = pd.read_csv(f"{self.database_location}/{self.filename}.csv")

        if self.dna_length == -1 and self.population_size == -1:
            self.population_size = df.shape[0]
            self.dna_length = df.shape[1]
            individuals = []
            for dna_index in range(df.shape[0]):
                individual_dna = list(df.iloc[dna_index].values)
                individuals.append(Individual(individual_dna))
            self.individuals = individuals
            self.getPopulationParameters()
        else:
            self.getPopulationParameters()
            if self.population_size != df.shape[0]:
                pop_size = 0
                individuals = []
                while pop_size < self.population_size:
                    if pop_size > len(self.individuals):
                        new_individual = Individual()
                        new_individual.newDNASequence(self.dna_length, self.dna_start, self.dna_end)
                        individuals.append(new_individual)
                    else:
                        individuals.append(self.individuals[pop_size])
                    pop_size += 1
                self.individuals = individuals
            elif self.dna_length != df.shape[1]:
                for individual in self.individuals:
                    individual.newDNASequence(self.dna_length, self.dna_start, self.dna_end)

    def changePopulationSize(self, new_size: int):
        self.population_size = new_size
        self.refreshParameters()

    def changeDNALength(self, new_dna_length: int):
        self.dna_length = new_dna_length
        self.refreshParameters()

    def savePopulationDNA(self):
        "Write in a csv file the population information"
        with open(f"{self.database_location}\\{self.creation}_{self.filename}.csv", 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            for individual in self.individuals:
                writer.writerow(individual.getSequenceOfDNA())

        with open(f"{self.database_location}\\{self.creation}_{self.filename}.txt", 'w') as file:
            file.write(
                f"DNA start: {self.dna_start}\nDNA end: {self.dna_end}\nGeneration number: {self.generation_number}\nRound number: {self.rounds}\nBest individual: {self.best_individual_index}"
            )


# Main functions to create and load populations
def initPopulation(database_location: str, filename: str, population_size: int = POPULATION_SIZE, dna_length: int = DNA_LENGTH, dna_end: float = DNA_END, dna_start: float = DNA_START) -> Population:
    """
    This function will start a new population wich is just a matrix of numbers, where each column represents a 'base pair' of the 'DNA' and the rows represent
    the individuals, the number of columns will be determined by the parameter 'dna_lenght' and the number of rows will be determined by 'population_size', the
    database_location is where the matrix will be stored. The dna_start and dna_end will be the range of numbers that can be generated, so if dna_start is = -5
    and dna_end = 5, the numbers will be generated only between -5 and 5.
    """

    new_population = Population(database_location, filename, population_size, dna_length, dna_start, dna_end)
    new_population.initIndividuals()

    return new_population


def loadPopulation(database_location: str, filename: str) -> Population:
    loadedPopulation = Population(database_location, filename, -1, -1, -1, -1)
    loadedPopulation.refreshParameters()

    return loadedPopulation