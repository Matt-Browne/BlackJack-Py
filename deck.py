#-------------------------------------------------------------------------------
# Name:        deck.py
# Purpose:
#
# Author:      Matt Browne and Jackson Clark
#
# Created:     16/11/2014

#-------------------------------------------------------------------------------
import random

class Card:
    """ define a playing card () """

    def __init__(self,i):
        """ initialize a card, setting its value to i """
        self.value = i
        self.front = ""
        self.back = ""
        self.name = ""

    def setValue(self,val):
        """ set the value of a card """
        self.value = val


    def getValue(self):
        """ get the value of a card """
        return self.value

    def setFront(self,val):
        """ set the path to the front image of a card """
        self.front = val

    def getFront(self):
        """ get the path to the front image of a card """
        return self.front

    def setBack(self,val):
        """ set the path to the back image of a card """
        self.back = val

    def getBack(self):
        """ get the path to the back image of a card """
        return self.back

    def setName(self,val):
        """ set the name of a card (str) """
        self.name = val

    def getName(self):
        """ get the name of a card (str) """
        return self.name

class Deck:
    """ create a deck of cards.  Requires random library """
    def __init__(self,size):
        self.cards = []
        for i in range(size):
            self.cards.append(Card(i))
        self.size = len(self.cards)
        self.assign()


        # set up variables for the range to cut at
        self.cut1 = [24,28] # upper and lower bounds
        self.drop = [1,5] #sets range of shuffle drop for random int


    def assign(self):
        f = open("text files/smallcard.txt", "r") # read txt file with card names on seperate lines
        cardnames = []
        # read each line (card names) in the file and add  to list
        for i in f:
            cardnames.append(i[:-1])
        f.close()
        # sets front, back, and name of cards based on card name from file
        for i in range(self.size):
            self.cards[i].setFront("cards/{}.gif".format(cardnames[i]))
            self.cards[i].setBack("cards/b1fv.gif")
            self.cards[i].setName(cardnames[i])
        # assigns a blackjack value to each card based on card name
        for i in self.cards:
            if (i.getName()[:1] == "a"): # aces are 11 , cahnged to 1 as necessary with function checkAce() in Blackjack.py
                i.setValue(11)
            # 10 or face cards
            elif (i.getName()[:1] == "1" or i.getName()[:1] == "j" or i.getName()[:1] == "q" or i.getName()[:1] == "k"):
                i.setValue(10)

            else:
                i.setValue(i.getName()[:1])


    def shuffle(self):
        """Passes in list lh (left part of deck), list rh (right part of deck), drop variable range as a list drop.
        shuffles lh and rh with varying drops from each side until no cards are left, returns shuffled deck """

        for i in range(10):
             # split deck into two nearly halves, shuffle by droping a random number of cards from each side until all cards are gone
            where = random.randint(self.cut1[0],self.cut1[1])
            rh = self.cards[0:where]
            lh = self.cards[where:len(self.cards)]

            deck = []
            while True:
                d = random.randint(self.drop[0],self.drop[1])
                deck += lh[0:d] #dropping d cards, adding to end of self.cards
                lh = lh[d:] #removes d cards from lh
                d = random.randint(self.drop[0],self.drop[1])
                deck = deck + rh[0:d] #dropping d cards, adding to end of deck
                rh = rh[d:] #removes d cards from rh
                self.cards = deck
                if (len(rh) == 0 and len(lh) == 0):
                    break # no cards left so break out of while loop
                #end if
            #end while
        # end for

        return(self)

    def deal(self):
        """ deal a card from the deck (return the card value), self.cards size is
            decremented by one """
        card = self.cards[-1]
        self.cards = self.cards[:-1]
        return(card)

    def cut(self):
        """ randomly cut deck and move to the the bottom. """
        a = random.randint(1,self.size)
        self.cards[:a],self.cards[a:] = self.cards[a:], self.cards[:a]
        return(self)


    def getCardValues(self):
        """ get card values as list """
        temp = []
        for i in range(self.size):
            temp.append(self.cards[i].getValue())
        return temp

    def cutdeck(self):
        """ take deck,randomly split array into two halves using variables passed in as list cut, returns lh and rh as lists """
        where = random.randint(self.cut1[0],self.cut1[1])
        rh = self.cards[0:where]
        lh = self.cards[where:len(self.cards)]
        return(self)

