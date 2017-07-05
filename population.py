
import random
import math
import Parser
import copy
import settings

class Gene(object):

    def __init__(self,key,x,y, distances=None):
        self.key = key
        self.x = x
        self.y = y
        self.gx = x
        self.gy = y
        settings.genes.append(self)

        self.distances = {self.key: 0.0}
        if distances:
            self.distances = distances

    def calc_distances(self):
        """
            počíta vzdialenosti do všetkých ostatných miest
        """

        for gene in settings.genes:
            tmp = self.euclidian_distance(self.x, self.y, gene.x, gene.y)
            self.distances[gene.key] = tmp


    def euclidian_distance(self, x1, y1, x2, y2):
        """ 
            počítanie euklidovskej vzdialenosti
        """
        deltax = abs(x1 - x2)
        deltay = abs(y1 - y2)
        return int(math.sqrt((deltax*deltax + deltay*deltay)))

    def manhattan_distance(self, x1, y1, x2, y2):
        """ 
            počítanie manhatanskej vzdialenosti
        """
        deltax = abs(x1 - x2)
        deltay = abs(y1 - y2)
        return int(deltax+deltay)

class Chromosome(object):

    def __init__(self):
        self.route = sorted(settings.genes, key=lambda *args: random.random())
        self.calc_length()
        self.calc_fittness()

    def calc_fittness(self):
        self.fittness = 1/self.length *10000

    def calc_length(self):
        self.length = 0.0

        for gene in self.route:
            neighbour = self.route[self.route.index(gene) - len(self.route) + 1]
            neighbour_distance = gene.distances[neighbour.key]
            self.length += neighbour_distance


    def genes_validation(self):
        for gene in settings.genes:
            if self.doubles_count(self.route, lambda g: g.key == gene.key) >1:
                return False
        return True

    def doubles_count(self, chromosome, fnc):
        return sum(1 for gene in chromosome if fnc(gene))


class Population(object):
    def __init__(self, size, init):
        self.size = size
        self.chromosomes = []

        if init:
            for i in range(0, size):
                new_chromosome = Chromosome()
                self.chromosomes.append(new_chromosome)
            self.get_fittest()

    def get_fittest(self):
        sl = sorted(self.chromosomes, key= lambda chromosome: chromosome.fittness, reverse=True)
        self.fittest = sl[0]
        return self.fittest