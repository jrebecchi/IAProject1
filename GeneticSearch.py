# -*- coding: utf-8 -*-
import random 
from Path import Path
import math
class GeneticSearch:
    
    MAX_NUMBER_OF_SIBLINGS = 110
    MIN_NUMBER_OF_SIBLINGS = 30
    MAX_NUMBER_WITHOUT_IMPROVEMENT = 30
    MAX_NUMBER_OF_MUTATION = 1
    
    def __init__(self, cityMap, seed = None):
       self.seed = seed
       self.cityMap = cityMap
       if seed != None:
           random.seed(seed)

    
    def search(self):
        noImprovement = 0
        population = self._generatePolulation(self.MAX_NUMBER_OF_SIBLINGS)
        actualBestElement = self._bestElement(population)
        while noImprovement < self.MAX_NUMBER_WITHOUT_IMPROVEMENT:
            loopNumber = int((self.MAX_NUMBER_OF_SIBLINGS - self.MIN_NUMBER_OF_SIBLINGS)/2)
            for i in range(0, loopNumber):
                parent1 = self._selectParent(population)
                parent2 = self._selectParent(population)
                (kid1, kid2) = self._makeLove(parent1, parent2)
                for j in range(0, self.MAX_NUMBER_OF_MUTATION):
                    self._mutate(kid1)
                    self._mutate(kid2)
                population.append(Path(kid1,self.cityMap))
                population.append(Path(kid2,self.cityMap))
            population = self._keepBestElements(population, self.MIN_NUMBER_OF_SIBLINGS)
            newBestElement = population[0]
            if (newBestElement.pathcost >= actualBestElement.pathcost):
                noImprovement +=1
            else:
                noImprovement =0
                actualBestElement = newBestElement
        result = actualBestElement.path
        return result
    
    @classmethod
    def _makeLove(self, father, mother):
        halfNumberOfCities = int(len(father)/2)
        startOfSelection = random.randint(0,halfNumberOfCities)
        child1 = list()
        child2 = list()
        nextIndiceToFillForChild1=0
        nextIndiceToFillForChild2=0
        for i in range(0, len(father)):
            if i >= startOfSelection and i < startOfSelection+halfNumberOfCities :
                child1.insert(i, father[i])
                child2.insert(i, mother[i])
                nextIndiceToFillForChild1=i+1
                nextIndiceToFillForChild2=i+1
            if i >= startOfSelection+halfNumberOfCities:
                if mother[i] not in child1:
                    child1.insert(i, mother[i])
                    nextIndiceToFillForChild1=i+1
                if father[i] not in child2:
                    child2.insert(i, father[i])
                    nextIndiceToFillForChild2=i+1
        for i in range(0, len(father)):
            if nextIndiceToFillForChild1 == len(father):
                nextIndiceToFillForChild1 = 0
            if nextIndiceToFillForChild2 == len(father):
                nextIndiceToFillForChild2 = 0
            if mother[i] not in child1:
                child1.insert(nextIndiceToFillForChild1, mother[i])
                nextIndiceToFillForChild1 +=1
            if father[i] not in child2:
                child2.insert(nextIndiceToFillForChild2, father[i])
                nextIndiceToFillForChild2 +=1
        
        return (child1, child2)
    
    def _mutate(self, child):
        swapPosition1 = random.randint(0,len(child)-1)
        swapPosition2 = random.randint(0,len(child)-1)
        temp = child[swapPosition1]
        child[swapPosition1] = child[swapPosition2]
        child[swapPosition2] = temp
        
    def _generateRandomSolution(self):
        solution = list(self.cityMap.getCityList())
        random.shuffle(solution)
        return solution
    
    def _generatePolulation(self, numberOfElement):
        population = list()
        for i in range(0, numberOfElement):
            path=self._generateRandomSolution()
            population.append(Path(path,self.cityMap))
        return population
    
    def _selectParent(self, population):
        indice1 = random.randint(0,len(population)-1)
        indice2 = random.randint(0,len(population)-1)
        if (population[indice1].pathcost >= population[indice1].pathcost):
            return population[indice2].path
        else:
            return population[indice1].path
    
    def _bestElement(self, population):
        element = 0
        for i in range(1, len(population)):
            if(population[i].pathcost < population[element].pathcost):
                element = i
        return population[element]
    
    def _keepBestElements(self, population, numberToKeep):
        costClassification = dict()
        for i in range(0,len(population)):
            costClassification[population[i].pathcost]  = population[i] 
        sortedListOfBestElements = [value for (key, value) in sorted(costClassification.items())]
        n = int(math.ceil(numberToKeep/2))
        "Keeps top n elements, where n is selected number/2"
        filteredSortedListOfBestElements = sortedListOfBestElements[:n] 
        "Calculates how many will be left"
        amountLeft = len(population) - n
        "Gets in a separate list the not chosen elements"
        notSelectedElementList = sortedListOfBestElements[:-amountLeft]
        "Shuffles the list"
        random.shuffle(notSelectedElementList)
        "Selects the first n random elements"
        randomSelectedElementList = notSelectedElementList[:n]
        
        return filteredSortedListOfBestElements + randomSelectedElementList  
            
