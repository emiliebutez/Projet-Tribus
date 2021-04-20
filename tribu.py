import random

class Tribe:
    name = ""

    def __init__(self):
        self.name = "nom_tribut"

    def hunt(self, sesChoix):
        return 0

class BetrayTribe(Tribe):

    def __init__(self):
        self.name = "betrayTribe"

    def hunt(self, sesChoix):
        return 1

class CoopTribe(Tribe):

    def __init__(self):
        self.name = "coopTribe"

    def hunt(self, sesChoix):
        return 0

class RndTribe(Tribe):

    def __init__(self):
        self.name = "rndTribe"

    def hunt(self, sesChoix):
        return random.randint(0,2)

class MyTribe(Tribe):

    def __init__(self):
        self.name = "tribu_nal"

        # va servir à faire une liste de mes choix à chaque tour
        self.meschoix = [] 

        # va servir à compter le nombre de tour 
        self.tourActuel = 0 
        
        # suite de nombre non séquentiel pour trahir
        self.coupRandom = [30,38,43,55,66,76,78,85,93,98,99]



    def initialiserPartie(self, sesChoix) : 
        """cette fonction sert à initialiser en début de chaque
        match la liste meschoix,le nombre de tour et la liste de 
        nombre qui représente le tour auquel nous allons trahir"""

        if self.tourActuel == len(sesChoix) :
            self.tourActuel = 0
            self.meschoix = []
            self.coupRandom = [30,38,43,55,66,76,78,85,93,98,99]


    def hunt(self, sesChoix):#à compléter
        """Cette fonction définit notre choix du tour actuel 
        par rapport à des conditions. 

        Si le tour actuel est égal au tour ou nous voulons 
        placer un trahir, nous trahissons.
        
        Sinon si le tour actuel est inférieur à 5 nous jouons random
        sauf si dans les deux derniers tours l'adversaire à jouer
        la coopération dans ce cas là nous le suivons.

        Sinon si le tour est inférieur à 15 nous jouons la 
        coopération. Mais si l'adversaire nous trahit 
        trois fois de suite alors nous renonçons.

        Sinon nous choisissons la coopération. Par 
        contre si nos points des 5 derniers tours 
        sont inférieurs ou égal à 10 nous choisissons de 
        renoncer jusqu'à temps que nos points soit 
        de nouveau supérieur à 10 ou que l'adversaire 
        coopère deux tours de suite.
         """
        self.initialiserPartie(sesChoix)
        
        monChoix = 0
        
        if len(self.coupRandom) > 0 and self.tourActuel == self.coupRandom[0] : 
            self.coupRandom = self.coupRandom[1:]
            monChoix = 1
        
        elif self.tourActuel < 5: 
            monChoix = random.randint(0,2)

            if self.advCoopDeuxTours(sesChoix):
                monChoix = 0

        elif self.tourActuel < 15: 
            monChoix = 0

            if self.advTrahiTroisTours(sesChoix):
                monChoix = 2

        else : 
            monChoix = 0
            if self.mesPoints(sesChoix) <= 10:
                monChoix = 2
                if self.advCoopDeuxTours(sesChoix):
                    monChoix = 0

        self.meschoix.append(monChoix)
        self.tourActuel += 1
        return monChoix

            

    def advCoopDeuxTours(self, sesChoix):
            """Cette fonction sert à vérifier si l'adversaire 
            coopère deux tours de suite."""
            return sesChoix[self.tourActuel -1] \
                == sesChoix[self.tourActuel -2] \
                == 0


    def advTrahiTroisTours(self, sesChoix):
        """Cette fonction sert à vérifier si l'adversaire 
        trahit trois tours de suite."""
        return sesChoix[self.tourActuel -1] \
            == sesChoix[self.tourActuel -2] \
            == sesChoix[self.tourActuel -3] \
            == 1


    def mesPoints(self, sesChoix):
        """Cette fonction sert à compter le nombre de points
         engrangé lors des cinq derniers tours."""
        r1 = 0
        r2 = 0
        for i in range(self.tourActuel-5, self.tourActuel):
            choice1 = sesChoix[i]
            choice2 = self.meschoix[i]

            #ajout recompense
            if choice1 == 2:
                if choice2 == 2:
                    r1+=2
                    r2+=2
                elif choice2 == 0:
                    r1 += 2
                    r2 += 1
                elif choice2 == 1:
                    r1 += 2
                    r2 += 1
            elif choice1 == 0:
                if choice2 == 2:
                    r1+=1
                    r2+=2
                elif choice2 == 0:
                    r1 += 4
                    r2 += 4
                elif choice2 == 1:
                    r1 += 1
                    r2 += 6
            elif choice1 == 1:
                if choice2 == 2:
                    r1+=1
                    r2+=2
                elif choice2 == 0:
                    r1 += 6
                    r2 += 1
                elif choice2 == 1:
                    r1 += 1
                    r2 += 1
        
        return r2



def match(t1, t2, nbRounds):
    r1 = 0#récompenses tribu1
    r2 = 0#récompense tribu2

    #historique
    t1_choices = list()
    t2_choices = list()

    for i in range(nbRounds):
        t1_choices.append(-1)
        t2_choices.append(-1)

    #match
    for round in range(0, nbRounds):
        #faire les choix
        choice1 = t1.hunt(t2_choices)
        choice2 = t2.hunt(t1_choices)

        #maj historique
        t1_choices[round] = choice1
        t2_choices[round] = choice2

        #ajout recompense
        if choice1 == 2:
            if choice2 == 2:
                r1+=2
                r2+=2
            elif choice2 == 0:
                r1 += 2
                r2 += 1
            elif choice2 == 1:
                r1 += 2
                r2 += 1
        elif choice1 == 0:
            if choice2 == 2:
                r1+=1
                r2+=2
            elif choice2 == 0:
                r1 += 4
                r2 += 4
            elif choice2 == 1:
                r1 += 1
                r2 += 6
        elif choice1 == 1:
            if choice2 == 2:
                r1+=1
                r2+=2
            elif choice2 == 0:
                r1 += 6
                r2 += 1
            elif choice2 == 1:
                r1 += 1
                r2 += 1

    return (r1, r2)

def tournoi(tribes):
    nbRounds = 100
    points = list()
    wins = list()
    for i in range(0, len(tribes)):
        points.append(0)
        wins.append(0)

    for i in range(0, len(tribes)):
        tribe1 = tribes[i]
        for j in range(i, len(tribes)):
            tribe2 = tribes[j]
            if i < j:
                (score1, score2) = match(tribe1, tribe2, nbRounds)
                print(tribe1.name + " vs "+ tribe2.name)
                print(str(score1)+" - "+str(score2))
                points[i] += score1
                points[j] += score2
                if score1 > score2:
                    wins[i]+=1
                elif score1 < score2:
                    wins[j]+=1

    print("Final result")
    for i in range(0, len(tribes)):
        print(tribes[i].name+" "+str(points[i])+" "+str(wins[i]))


tribes = list()
tribes.append(CoopTribe())
tribes.append(BetrayTribe())
tribes.append(RndTribe())
tribes.append(MyTribe())

tournoi(tribes)
