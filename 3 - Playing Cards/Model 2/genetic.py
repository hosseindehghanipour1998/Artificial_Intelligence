import random
import math

class GeneticAlgorithm:

    # population size
    POP = 30

    # geneotype
    LEN = 10

    # mutation rate, change it have a play
    MUT = 0.1

    # recomination rate
    REC = 0.5

    # how many tournaments should be played
    END = 2000

    # the sum pile, end result for the SUM pile
    # card1 + card2 + card3 + card4 + card5, MUST = 36 for a good GA
    SUMTARG = 36

    # the product pile, end result for the PRODUCT pile
    # card1 * card2 * card3 * card4 * card5, MUST = 360 for a good GA
    PRODTARG = 360

    # the genes array, 30 members, 10 cards each
    gene = []
    for i in range(0, 31):
        gene.append([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    # used to create randomness (Simulates selection process in nature)
    # randomly selects genes
    rnd = random.random()

    def run(self):
        # initialise the population (randomly)
        self.init_pop()
        # start a tournament
        for tournamentNo in range(0, self.END):
            # pull 2 population members at random
            random.seed()
            a = math.trunc(round(self.POP * random.random(), 0))
            random.seed()
            b = math.trunc(round(self.POP * random.random(), 0))
            # have a fight, see who has best genes
            if self.evaluate(a) < self.evaluate(b):
                winner = a
                loser = b
            else:
                winner = b;
                loser = a;
            # Possibly do some gene jiggling, on all genes of loser
            # again depends on randomness (simulating the natural selection
            # process of evolutionary selection)
            for i in range(0, self.LEN):
                # maybe do some recombination
                if random.random() < self.REC:
                    self.gene[loser][i] = self.gene[winner][i]
                #maybe do some muttion
                if random.random() < self.MUT:
                    self.gene[loser][i] = 1 - self.gene[loser][i]
                # then test to see if the new population member is a winner
                if self.evaluate(loser) == 0.0:
                    self.display(tournamentNo, loser)


    # Display the results. Only called for good GA which has solved
    # the problem domain
    # @param tournaments : the current tournament loop number
    # @param n : the nth member of the population.
    def display(self, tournaments, n):
        print("\r\n==============================\r\n")
        print("After {} tournaments, Solution sum pile (should be 36) cards are : ".format(tournaments))
        countsum = 0
        countprod = 1
        for i in range(0, self.LEN):
            if self.gene[n][i] == 0:
                print(i + 1)
                countsum += i+1
        print("\r\nWhich sum to: {}\r\n".format(countsum))
        print("\r\n==============================\r\n")
        print("\r\nAnd Product pile (should be 360)  cards are : ")
        for i in range(0, self.LEN):
            if self.gene[n][i] == 1:
                print(i + 1)

                countprod = countprod*(i+1)
        print("\r\nWhich product is: {}\r\n".format(countprod))
        print("\r\n==============================\r\n")

    # evaluate the the nth member of the population
    # @param n : the nth member of the population
    # @return : the score for this member of the population.
    # If score is 0.0, then we have a good GA which has solved
    # the problem domain
    def evaluate(self, n):
        # initialise field values
        ssum = 0
        prod = 1
        # loop though all genes for this population member
        for i in range(0, self.LEN):
            # if the gene value is 0, then put it in the sum (pile 0), and calculate sum
            if self.gene[n][i] == 0:
                ssum += (1 + i)
            # if the gene value is 1, then put it in the product (pile 1), and calculate sum
            else:
                prod *= 1 + i
        # work out how food this population member is, based on an overall error
        # for the problem domain
        # NOTE : The fitness function will change for every problem domain.
        scaled_sum_error = (ssum - self.SUMTARG) / self.SUMTARG
        scaled_prod_error = (prod - self.PRODTARG) / self.PRODTARG
        combined_error = math.fabs(scaled_sum_error) + math.fabs(scaled_prod_error)

        return combined_error

    # initialise population
    def init_pop(self):
        # for entire population
        for i in range(0, self.POP):
            #for all genes
            for j in range(0, self.LEN):
                #randomly create gene values
                self.rnd = random.random()
                if self.rnd < 0.5:
                    self.gene[i][j] = 0
                else:
                    self.gene[i][j] = 1