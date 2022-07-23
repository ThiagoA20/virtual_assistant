from genetic_algorithm import *
import os
from pathlib import Path
import unittest
import logging


class TestIndividual(unittest.TestCase):

    def setUp(self):
        self.individual = Individual()

    def test_generate_individual(self):
        self.individual.newDNASequence(20, -100, 100)
        dna_sequence = self.individual.getSequenceOfDNA()
        self.assertEqual(len(dna_sequence), 20)
    
    def test_set_score_and_calculate_fitness(self):
        score1 = 30
        ideal_score1 = 100
        score2 = 50
        ideal_score2 = 100
        total_score = score1 + score2
        total_ideal_score = ideal_score1 + ideal_score2
        self.individual.setScore(score1, ideal_score1)
        self.individual.setScore(score2, ideal_score2)
        self.individual.calculateFitness()
        generated_fitness = self.individual.getFitness()
        self.assertEqual((total_score / total_ideal_score) ** 2, generated_fitness)


class TestPopulation(unittest.TestCase):

    def setUp(self):
        POPULATION_SIZE = 500
        DNA_LENGTH = 24
        DNA_START = -100
        DNA_END = 100

        self.DIRECTORY = 'D:\\trading_bot\\meta_heuristic'
        self.FILENAME = 'test_population'

        self.population = Population(
            self.DIRECTORY, self.FILENAME,
            POPULATION_SIZE,
            DNA_LENGTH,
            DNA_START,
            DNA_END
        )
        self.population.initIndividuals()
        INDIVIDUAL_SCORES = [random.uniform(0, 99) for x in range(500)]
        IDEAL_SCORE = [100 for x in range(500)]
        self.population.addIndividualScore(INDIVIDUAL_SCORES, IDEAL_SCORE)
        self.population.calculatePopulationMeanFitness()
        self.population.poolSelection()

        # logging.debug(f'Population size: {self.population.population_size}')
        # logging.debug(f'Population sum fitness: {self.population.sum_population_fitness}')
        # logging.debug(f"Mean fitness: {self.population.meanFitness}")

    def test_init_individuals(self):
        self.assertEqual(len(self.population.individuals), 500)
    
    def test_add_individuals_score_and_calculate_population_fitness(self):
        self.assertNotEqual(self.population.meanFitness, 0.0)

    def test_pool_selection(self):
        self.assertEqual((len(self.population.parents1) + len(self.population.parents2)), (self.population.population_size * 2))

    def test_crossover(self):
        self.population.crossover()
        self.assertEqual(len(self.population.individuals), 500)

    def test_apply_mutation_rate(self):
        self.population.applyMutationRate()
    
    def test_get_Best_Individual(self):
        best_individual_index = self.population.getBestIndividual()
        self.assertEqual(type(best_individual_index), int)
        self.assertNotEqual(best_individual_index, -1)

    def test_save_population_dna(self):
        self.population.savePopulationDNA()
        self.assertTrue(Path(f'{self.DIRECTORY}\\{self.FILENAME}.csv').exists())
        os.remove(f'{self.DIRECTORY}\\{self.FILENAME}.csv')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()