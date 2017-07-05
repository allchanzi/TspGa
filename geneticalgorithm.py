import Parser
import random
import population as pop
import settings
import copy


class GeneticAlgorithm(object):


    def initialize_genens(self, filename):
        p = Parser.Parser(filename)
        coords = p.get_coords()
        for i in range(0, len(coords) - 1):
            a = pop.Gene(str(i), coords[i][0], coords[i][1])
        for gene in settings.genes:
            gene.calc_distances()
    #Selections
    def tournament_selection(self, population):
        tournament_population = pop.Population(size=settings.tournament_size, init = False)
        tournament_selection = pop.Population(size=population.size, init= False)

        for i in range(0, len(population.chromosomes)*1):
            for j in range(0, settings.tournament_size-1):
                tournament_population.chromosomes.append(random.choice(population.chromosomes))
            tournament_selection.chromosomes.append(tournament_population.get_fittest())


        return tournament_selection

    def roulette_selection(self, population):
        roulette_population = pop.Population(size=population.size, init= False)


        absolut_sum = sum(i.fittness for i in population.chromosomes)
        probabilities = []
        prob_sum=0
        for i in range(0, len(population.chromosomes)*1):
            probability = prob_sum + population.chromosomes[i].fittness / absolut_sum
            prob_sum +=  population.chromosomes[i].fittness / absolut_sum
            probabilities.append(probability)


        for j in range(0, len(population.chromosomes)*1):
            spin = random.uniform(0,prob_sum)
            for i in range(0, len(population.chromosomes)):
                if i == 0 and spin <= probabilities[i]:
                    roulette_population.chromosomes.append(population.chromosomes[i])
                elif i == len(population.chromosomes)-1 and spin> probabilities[i-1]:
                    roulette_population.chromosomes.append(population.chromosomes[i])
                elif spin <= probabilities[i] and spin > probabilities[i-1]:
                    roulette_population.chromosomes.append(population.chromosomes[i])



        return roulette_population

    #Crossovers

    def oox(self,population):
        """
            Ordered-One Crossover náhodne sa zvolia dve pozície chromosomu 
            border_1, border_2
            
        """
        parents = population.chromosomes

        childrens = []

        for i in range(0, int(len(population.chromosomes)/2)):
            pair = random.sample(parents, 2)
            for j in pair:
                parents.remove(j)

            parent1 = pair[0]
            parent2 = pair[1]
            child1 = pop.Chromosome()
            child2 = pop.Chromosome()

            for g in range(0,len(child1.route)):
                child1.route[g] = None
                child2.route[g] = None

            border_1 = random.randint(0, len(parent1.route) - 1)
            border_2 = random.randint(border_1 + 1, len(parent1.route))

            child1.route[border_1:border_2+1] = parent1.route[border_1:border_2+1]
            child2.route[border_1:border_2+1] = parent2.route[border_1:border_2+1]

            parent1_after_extraction = parent1.route[border_2:] + parent1.route[:border_2]
            parent2_after_extraction = parent2.route[border_2:] + parent2.route[:border_2]



            for i in range(border_2, len(child1.route)):
                for j in range(0, len(parent2_after_extraction)):
                    if not parent2_after_extraction[j] in child1.route:
                        child1.route[i] = parent2_after_extraction[j]
            for i in range(0, border_1):
                for j in range(0, len(parent2_after_extraction)):
                    if not parent2_after_extraction[j] in child1.route:
                        child1.route[i] = parent2_after_extraction[j]

            for i in range(border_2, len(child2.route)):
                for j in range(0, len(parent1_after_extraction)):
                    if not parent1_after_extraction[j] in child2.route:
                        child2.route[i] = parent1_after_extraction[j]
            for i in range(0, border_1):
                for j in range(0, len(parent1_after_extraction)):
                    if not parent1_after_extraction[j] in child2.route:
                        child2.route[i] = parent1_after_extraction[j]

            child1.calc_length()
            child2.calc_length()
            child1.calc_fittness()
            child1.calc_fittness()
            childrens.append(child1)
            childrens.append(child2)

        return childrens

    def pmx(self, population):
        parents = population.chromosomes

        childrens = []

        for i in range(0, int(len(population.chromosomes)/2)):
            pair = random.sample(parents, 2)
            for j in pair:
                parents.remove(j)

            parent1 = pair[0]
            parent2 = pair[1]
            child1 = pop.Chromosome()
            child2 = pop.Chromosome()

            for g in range(0,len(child1.route)):
                child1.route[g] = None
                child2.route[g] = None

            size = len(parent1.route)
            borders = random.sample(range(size), 2)
            border_1,border_2 = min(borders), max(borders)
            child1.route = copy.copy(parent1.route)
            child1.route[border_1:border_2+1] = parent1.route[border_1:border_2+1]
            child2.route[border_1:border_2+1] = parent2.route[border_1:border_2+1]
            child2.route = copy.copy(parent2.route)
            for parent, child in zip([parent1.route, parent2.route], [child1.route, child2.route]):

                for j in range(border_1, border_2 +1):
                    if parent[j] not in child[border_1:border_2 +1]:
                        spot = j
                        while border_1 <= spot <= border_2:
                            spot = parent.index(child[spot])
                        child[spot] = parent[j]

            child1.calc_length()
            child2.calc_length()
            child1.calc_fittness()
            child1.calc_fittness()
            childrens.append(child1)
            childrens.append(child2)



        return childrens

    #Mutations


    def swap_mutation(self, chromosome, mutation_probability = 0.3):
        if random.random() < mutation_probability:
            gene_pos1 = random.randint(0, len(chromosome.route)-1)
            gene_pos2 = random.randint(0, len(chromosome.route)-1)

            if gene_pos1 == gene_pos2:
                return chromosome

            gene1 = chromosome.route[gene_pos1]
            gene2 = chromosome.route[gene_pos2]

            chromosome.route[gene_pos2] = gene1
            chromosome.route[gene_pos1] = gene2

        chromosome.calc_length()
        chromosome.calc_fittness()
        return chromosome

    def inverse_mutation(self, chromosome, mutation_probability = 0.3):
        if random.random() < mutation_probability:
            gene_pos1 = random.randint(0, len(chromosome.route)-1)
            gene_pos2 = random.randint(0, len(chromosome.route)-1)

            tmp = chromosome.route[gene_pos1:gene_pos2+1]
            tmp.reverse()
            chromosome.route[gene_pos1:gene_pos2+1] = tmp

        return chromosome

    def partitial_shuffle_mutation(self, chromosome, mutation_probability = 0.3):
        if random.random() < mutation_probability:
            gene_pos1 = random.randint(0, len(chromosome.route)-1)
            gene_pos2 = random.randint(0, len(chromosome.route)-1)

            tmp = chromosome.route[gene_pos1:gene_pos2 + 1]
            random.shuffle(tmp)
            chromosome.route[gene_pos1:gene_pos2 + 1] = tmp

        return chromosome





    def evolve(self, initial_population, elitism=False):
        new_population = pop.Population(size=initial_population.size, init=True)

        elite = 0

        if elitism:
            new_population.chromosomes[0] = initial_population.fittest
            elite = 1


        if settings.selection == 'tournament':
            new_population = self.tournament_selection(initial_population)
        elif settings.selection == 'roulette':
            new_population = self.roulette_selection(initial_population)

        if settings.crossover == 'oox':
            new_population.chromosomes = self.oox(new_population)
        elif settings.crossover == 'pmx':
            new_population.chromosomes = self.pmx(new_population)
        if settings.mutation == 'swap':
            for chromosome in new_population.chromosomes:
                if random.random() < 0.3:
                    self.swap_mutation(chromosome)
        elif settings.mutation == 'psm':
            for chromosome in new_population.chromosomes:
                if random.random() < 0.3:
                    self.partitial_shuffle_mutation(chromosome)
        elif settings.mutation == 'inverse':
            for chromosome in new_population.chromosomes:
                if random.random() < 0.3:
                    self.inverse_mutation(chromosome)
        return new_population