#-------------------------------------------------------------------------------
# Name:        Blackjack.py
# Purpose:
#
# Author:      m.browne/c.jackson
#
# Created:     10/11/2014
# Copyright:   (c) m.browne 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from graphics import *
from deck import *
from random import *
from buttons import *
import fileinput

def main():
    # Create game window and build buttons and text graphics
    w,deck,pent,greeting,prompt,resultMess,playertot,dealertot,dealbut,hitbut,staybut,dblebut,quitbut,chbetbut,dispbet,dispbank,insresult = gameInit()
    name,bank = getName()
    greeting.setText("Welcome {}, to\nBlackjack at J & M Casino".format(name))
    bet = getBet(w,dealbut)
    dbchk = False # initialize variable to keep status of double down or not so bet can be corrected
    dispbet.setText("The bet is ${} ".format(bet))
    dispbank.setText("Your bank is ${:,.02f}".format(bank))
    chbetbut.activate(w)
    quitbut.activate(w)
    prompt.setText("Click Deal to start game!")
    pt = Point(0,0)
    while (not quitbut.clicked(pt)): # check for quit
        pt = w.getMouse()
        if chbetbut.clicked(pt): # check for change bet
                dbchk,bet = clearGame(playertot,dealertot,insresult,resultMess,dbchk,bet,w)
                bet = getBet(w,dealbut)
                dispbet.setText("The bet is ${} ".format(bet))
        elif bank < 5:
            prompt.setText("You don't have enough money to play, please exit to reload bank")
            dealbut.deactivate(w)
            chbetbut.deactivate(w)
        elif bank < bet:
            prompt.setText("You have insufficient funds, please change bet")
            dealbut.deactivate(w)
        else:
            if (dealbut.clicked(pt)): # check for new hand
                dbchk,bet = clearGame(playertot,dealertot,insresult,resultMess,dbchk,bet,w)
                prompt.setText("")
                bank -= bet
                dispbank.setText("Your bank is ${:,.02f}".format(bank))
                if len(deck.cards) < pent:
                    prompt.setText("The deck has been shuffled!")
                    deck = Deck(0)
                    deck = Deck(52)
                    deck.shuffle()
                    pent = randint(15,25) # randomize the shuffle point (deck penetration before shuffle)
                dealbut.deactivate(w)
                chbetbut.deactivate(w)
                quitbut.deactivate(w)
                # end if
                # Deal two card to each player and adds card and graphic object to hand list
                player1hand, dealhand = dealcards(deck,w)
                player1Points, dealerPoints = getVals(player1hand,dealhand)
                # if dealer up card is an Ace, check for insurance
                if dealhand[2].getName()[:1] == "a":
                    bet,bank = insurance(w,prompt,dealhand,bank,bet,dispbank,insresult)

                playbutt(hitbut,staybut,dblebut,dealbut,chbetbut,quitbut,w)
                # checks to see if player hand is blackjack
                if ((int(player1hand[0].getValue()) + int(player1hand[2].getValue())) == 21
                and ((int(dealhand[0].getValue()) + int(dealhand[2].getValue())) < 21)):
                    dealhand[1] = drawcards(dealhand[0].getFront(),200,300,w) # draws face up card for dealer on game window
                    prompt.setText("Blackjack, pays 1.5 time bet!")
                    resultMess.setText("You Win!")
                    bank += (bet + (bet*1.5))
                # checks to see if dealer hand is blackjack
                elif ((int(dealhand[0].getValue()) + int(dealhand[2].getValue())) == 21
                and (int(player1hand[0].getValue()) + int(player1hand[2].getValue())) < 21):
                    dealhand[1] = drawcards(dealhand[0].getFront(),200,300,w) # draws face up card for dealer on game window
                    prompt.setText("Dealer has Blackjack!")
                    resultMess.setText("You Lose!")
                elif ((int(dealhand[0].getValue()) + int(dealhand[2].getValue())) == 21
                and (int(player1hand[0].getValue()) + int(player1hand[2].getValue())) == 21):
                    dealhand[1] = drawcards(dealhand[0].getFront(),200,300,w) # draws face up card for dealer on game window
                    resultMess.setText("It's a Push!")
                    bank += bet
                else: # neither player was dealt 21
                    playertot.setText("Your card count is {}".format(player1Points)) # displays players count on screen
                    # plays players hand to completition
                    play1,bet,bank,dbchk = playerhand(deck,prompt,player1hand,player1Points,hitbut,staybut,dblebut,playertot,bet,bank,dbchk,w)
                    # plays dealers hand to completition
                    deal1 = dealerhand(deck, dealhand,dealerPoints, dealertot,w)
                    if (play1 > 21):  # cheack for player bust
                        resultMess.setText("You Lose!")
                    elif (deal1 <= 21): # check for dealer bust
                        if (play1 <= 21 and play1 > deal1): # check for player win
                            resultMess.setText("You Win!")
                            bank += (bet*2)
                        elif (play1 == deal1): # check for push
                            resultMess.setText("It's a Push!")
                            bank += bet
                        else: # dealer win
                            resultMess.setText("You Lose!")
                        # end if
                    else: # player win
                        resultMess.setText("You Win!")
                        bank += (bet*2)
                    # end if
                dispbank.setText("Your bank is ${:,.02f}".format(bank))
                choicebutt(hitbut,staybut,dblebut,dealbut,chbetbut,quitbut,w)
                # end if
            # end if
    # end while
    findcnt = 0 # initialize count of name matches found in file to 0
    # read line of file, if name matches first word in line, replace line with (name bank)
    for line in fileinput.input("text files/scores.txt", inplace = 1):
        if line.split(",")[0] == name: # name match has been found
            # this line replaces line and writes to file
            print (line.replace(line.split(",")[1], str(bank)), end = "\n")
            findcnt += 1
        else: # if no match found, rewrite existing line to file
            print(line, end ="")
    if findcnt == 0: # if no matches found, add name and bank to file as new line
        out = open("text files/scores.txt", "a")
        out.write("{},{}\n".format(name,bank))
        out.close()


    w.close()




# ==============================================================================
def getVals(player1hand, dealhand):
     # Deal two card to each player and adds card and graphic object to hand list

            player1Points = 0 # initializes players count
            for i in range(0,len(player1hand),2): # loops through cards and adds values to player1Points
                player1Points += int(player1hand[i].getValue())
            # end for
            dealerPoints = 0 # initialize dealer points and add in values of each card
            for i in range(0,len(dealhand),2):
                dealerPoints += int(dealhand[i].getValue())
                #check dealer hand for double aces
            if dealerPoints > 21:
                   dealerPoints = checkAce(dealhand, dealerPoints)
             #check player hand for double aces
            if player1Points > 21:
                player1Points = checkAce(player1hand, player1Points)
            return(player1Points,dealerPoints)


# ==============================================================================
def gameInit():
    w = GraphWin("Blackjack", 800,800) # builds window
    w.setBackground(color_rgb(24, 123, 24))
    greeting = Text(Point(400,60), "Welcome to\nBlackjack at J & M Casino") # draws greeting text
    greeting.setStyle("bold")
    greeting.setSize(24)
    greeting.draw(w)

    Image(Point(400,180), "images/BJ table art Ins.gif").draw(w) #rules of the game

    prompt = Text(Point(400,775), "") # displays user instructions
    prompt.setStyle("bold")
    prompt.setFill("White")
    prompt.setSize(22)
    prompt.draw(w)


    resultMess = Text(Point(305,420),"") # display win/loss status
    resultMess.setStyle("bold")
    resultMess.setSize(36)
    resultMess.setFill("white")
    resultMess.draw(w)

    playertot = Text(Point(265,625), "") # display players count
    playertot.setStyle("bold")
    playertot.setSize(14)
    playertot.draw(w)

    dealertot = Text(Point(270,675), "") # display dealer count
    dealertot.setStyle("bold")
    dealertot.setSize(14)
    dealertot.draw(w)

    dispbet = Text(Point(615,400), "") # displays user instructions
    dispbet.setStyle("bold")
    dispbet.setSize(18)
    dispbet.draw(w)

    dispbank = Text(Point(575,430), "") # displays user instructions
    dispbank.setStyle("bold")
    dispbank.setSize(18)
    dispbank.draw(w)

    insresult = Text(Point(575,460), "") # displays user instructions
    insresult.setStyle("bold")
    insresult.setSize(18)
    insresult.draw(w)

    # builds deal, hit, stay, double down, and quit buttons
    chbetbut= Button(w,Point(550,715),95,35,"Change Bet")

    dealbut= Button(w,Point(450,715),75,35,"Deal")

    hitbut= Button(w,Point(197,715),75,35,"Hit")
    staybut = Button(w,Point(287,715),75,35,"Stay")
    dblebut = Button(w,Point(107,715),75,35,"Double\nDown")
    quitbut = Button(w,Point(700,715),50,35,"Quit")
    quitbut.rect.setFill("black")
    # draws graphival representation of deck on screen
    showdeck = [] # Draws static deck on screen
    for i in range(4):
        showdeck.append(Image(Point(i*-3 + 125,425), "cards/b1fv.gif"))
        showdeck[i].draw(w)
    deck = Deck(52) # initialize game deck
    deck.shuffle()
    pent = randint(15,25) # randomize the shuffle point (deck penetration before shuffle)

    return(w,deck,pent,greeting,prompt,resultMess,playertot,dealertot,dealbut,hitbut,staybut,dblebut,quitbut,chbetbut,dispbet,dispbank,insresult)


# ==============================================================================
def playbutt(hitbut,staybut,dblebut,dealbut,chbetbut,quitbut,w):
    """ activates button needed to play hand, hit, stay, and double down: deactivates the rest """
    if quitbut.active: quitbut.deactivate(w)
    if dealbut.active: dealbut.deactivate(w)
    if chbetbut.active: chbetbut.deactivate(w)
    hitbut.activate(w)
    staybut.activate(w)
    dblebut.activate(w)

# ==============================================================================
def choicebutt(hitbut,staybut,dblebut,dealbut,chbetbut,quitbut,w):
    """ activates choice buttons, deal, change bet, quit: deactivates the rest """
    quitbut.activate(w)
    dealbut.activate(w)
    chbetbut.activate(w)
    hitbut.deactivate(w)
    staybut.deactivate(w)
    dblebut.deactivate(w)


# ==============================================================================
def getName():
    """ gets name input from player, check saved games for match and sets bank to
    saved bank if found, if not found bank defaults to $1,000.  bank values loaded from
    file that are less than $100 will be loaded in as $1,000 """

    namwin= GraphWin("Login Screen", 676, 450)
    namwin.setBackground(color_rgb(24, 123, 24))

    Image(Point(338,225), "images/Hello_my_name_is_sticker.gif").draw(namwin)

    # name entry label and text box
    name = Entry(Point(338, 310), 40)
    namelab = Text(Point(338, 230), "Please click the entry box\n to enter your name\n(commas will be removed): ")
    namelab.setStyle("bold")
    namelab.setSize(22)
    name.setText("")
    name.draw(namwin)
    namelab.draw(namwin)
    # build set name button
    setname = Button(namwin, Point(338,360),75,30, "Set Name")
    setname.activate(namwin)
    p = Point(0,0)
    pname = name.getText() # grabs name from entry box if name is entered
##    pname = pname.replace(",", "")
##    pname = pname.strip()
    while (pname == ""):
        p = namwin.getMouse()
        if setname.clicked(p):
            if name.getText() != "":
                pname = name.getText().replace(",", "").strip()
    bank = 0 # initialize bank
    f = open("text files/scores.txt", "r")
    for line in f:
        if line.split(",")[0] == pname: # checks for name in saved games
            bank = float(line.split(",")[1]) # sets bank to saved value from file
    if bank < 100:
        bank = 1000
    f.close()
    namwin.close()
    return pname, bank

# ==============================================================================
def getBet(gamewin,dealbut):
    """ opens window and allows user to change the bet, displays current bet on main game window
    bet can be integer of 5 - 100 inclusive (multiples of 5) """
    betwin= GraphWin("Bet Screen", 600, 400)
    betwin.setBackground(color_rgb(24, 123, 24))

    prompt = Text(Point(300,50),"Please adjust your bet with the butttons!")
    prompt.setSize(24)
    prompt.setFill("white")
    prompt.draw(betwin)

    prompt2 = Text(Point(300,350), "Press Set Button to save bet!")
    prompt2.setSize(24)
    prompt2.setFill("white")
    prompt2.draw(betwin)

    Image(Point(215,235), "images/chips1.gif").draw(betwin)


    # betting buttons
    plus = CButton(betwin,Point(400, 180), 30, "+")
    plus.label.setStyle("bold")
    plus.label.setSize(28)
    plus.circ.setFill("green")
    plus.activate(betwin)
    minus = CButton(betwin,Point(500, 180), 30, "-")
    minus.label.setStyle("bold")
    minus.label.setSize(28)
    minus.circ.setFill("red")
    minus.activate(betwin)
    setbet = Button(betwin, Point(450, 260), 75, 30, "Set Bet")
    setbet.activate(betwin)


    # initialize bet and draw on screen
    bet = 5
    dispbet = Text(Point(220,115), "The bet is ${} ".format(bet))
    dispbet.setSize(30)
    dispbet.draw(betwin)
    pt = Point(0,0)
    while (not setbet.clicked(pt)): # waits for set bet to be clicked and saves bet
        pt = betwin.getMouse()
        if (plus.clicked(pt) and bet < 100):
            bet += 5
            dispbet.setText("The bet is ${} ".format(bet))
        elif (minus.clicked(pt) and bet > 5):
            bet -= 5
            dispbet.setText("The bet is ${} ".format(bet))
    if dealbut.active == False: # checks to make sure deal button isn't drawn and draws if not drawn
        dealbut.activate(gamewin)
    betwin.close()
    return bet
# ==============================================================================
def dealcards(deck,w):
    """ Takes in deck and graphic window.  Draws to window 4 cards, cards 1&3 to player one and cards 2&4 to dealer, returns card objects
    draws card 2 face down (dealers first card) and returns list of card and graphical objects for each hand """
    c1v, c2v, c3v, c4v, = deck.deal(), deck.deal(), deck.deal(), deck.deal()

    c1 = drawcards(c1v.getFront(),200,550,w)
    c2 = drawcards(c2v.getBack(),200,300,w)
    c3 = drawcards(c3v.getFront(),275,550,w)
    c4 = drawcards(c4v.getFront(), 275,300,w)
    playercards = [c1v,c1,c3v,c3]
    dealercards = [c2v,c2,c4v,c4]

    return(playercards,dealercards)

# test code, forces deal of ace hearts and ace club to player
##    c2v, c4v, = deck.deal(), deck.deal()
##    c1v = next((i for i in deck.cards if i.getName() == "ah"))
##    c3v = next((i for i in deck.cards if i.getName()== "ac"))

# ==============================================================================

def drawcards(card, x,y,w):
    """ receives card object and graphic window draws cards to window
    x and y values are for the center point of the image. """

    c = Image(Point(x,y), card) # use string to complete card file name
    c.draw(w)

    return(c)
# ==============================================================================
def playerhand(deck,prompt,player,count,hit,stay,dble,playertot,bet,bank,dbchk,w):
    """ deck = the game deck, player = list of card and graphic objects,
    count = sum of card values in hand, hit and stay are button objects,
    playertot = graphical text object - displays player count on screen, w = GraphinWin.
    Plays hand for user, allows for clicking hit until clicking stay or bust, returns count """

    while (count < 21):
        click = w.getMouse()
        if dble.clicked(click):
            prompt.setText("")
            bank -= bet
            bet, dbchk = bet*2, True
            phit = deck.deal() # deals card object from deck
            # creates images and draws to window
            h = drawcards(phit.getFront(), player[-1].getAnchor().getX() + 75 ,550,w)
            # adds card and card image player hand
            player.append(phit)
            player.append(h)
            # adds cards value to count
            count += int(phit.getValue())
            # if count over 21 then auto-adjust ace value
            if count > 21:
                count = checkAce(player,count)
            playertot.setText("Your count is {}".format(count)) # prints player count to window
            break

        elif(hit.clicked(click)): # checks for hit button clicked
            dble.deactivate(w)
            phit = deck.deal() # deals card object from deck
            # creates images and draws to window
            h = drawcards(phit.getFront(), player[-1].getAnchor().getX() + 75 ,550,w)
            # adds card and card image player hand
            player.append(phit)
            player.append(h)
            # adds cards value to count
            count += int(phit.getValue())
            # if count over 21 then auto-adjust ace value
            if count > 21:
                count = checkAce(player,count)
            playertot.setText("Your count is {}".format(count)) # prints player count to window

        elif (stay.clicked(click)): # stay
            prompt.setText("")
            break
        # end if
    # end while
    return count,bet,bank,dbchk

#test code, prints card values for each card in players hand
##                temp = []
##                for i in range(0,len(player),2):
##                    temp.append(player[i].getValue())
##                print(temp)


# ==============================================================================

def dealerhand(deck,dealer,count,dealertot,w):
    """ deck = the game deck, dealer = list of card and graphic objects,
    count = sum of card values in hand, hit and stay are button objects,
    dealertot = graphical text object - displays player count on screen, w = GraphinWin.
    Plays hand for user, allows for clicking hit until clicking stay or bust, returns count """

    dealer[1] = drawcards(dealer[0].getFront(),200,300,w) # draws face up card for dealer on game window
    while (count < 17): # dealers stays on all 17's
        dhit = deck.deal() # deal a card
        h = drawcards(dhit.getFront(), dealer[-1].getAnchor().getX() + 75 ,300,w) # draws a card
        # adds card and card image dealer hand list
        dealer.append(dhit)
        dealer.append(h)
        count += int(dhit.getValue()) # adds cards value to count
         # if count over 21 then auto-adjust ace value
        if (count > 21):
            count = checkAce(dealer,count)
    # end while

    dealertot.setText("The dealer count is {}".format(count))
    return count

# ==============================================================================
def insurance(w,prompt,dealhand,bank,bet,dispbank,insresult):
    prompt.setText("Do you want insurance?")
    yesbut = CButton(w, Point(625,770), 25, "Yes")
    yesbut.activate(w)
    yesbut.label.setStyle("bold")
    yesbut.label.setSize(18)
    yesbut.circ.setFill("blue")
    nobut = CButton(w,Point(685,770),25,"No")
    nobut.activate(w)
    nobut.label.setStyle("bold")
    nobut.label.setSize(18)
    nobut.circ.setFill("blue")

    while True:
        ipt = w.getMouse()
        if yesbut.clicked(ipt):
            yesbut.deactivate(w)
            nobut.deactivate(w)
            bank -= (bet/2)
            prompt.setText("")
            if dealhand[0].getValue() == 10:
                insresult.setText("Insurand paid ${:.02f}".format(bet))
                bank += (bet + (bet/2))
            dispbank.setText("Your bank is ${:,.02f}".format(bank))
            break
        elif nobut.clicked(ipt):
            yesbut.deactivate(w)
            nobut.deactivate(w)
            prompt.setText("")
            break
    return bet,bank,


# ==============================================================================
def clearGame(playertot, dealertot, insresult, resultMess, dbchk, bet, w):
    """ Resets game board, erases text and cards """
    # Resets text to empty strings and undraws each card in player and dealer hands from the graphic window
    resultMess.setText("")
    playertot.setText("")
    dealertot.setText("")
    insresult.setText("")
    if dbchk == True: # dble down was used last hand, divide bet by two to set back to normal (takes place after payout)
        dbchk = False # set dble down status back to no
        bet= bet/2

    # draws a table colored rectangle over the range of cards, undraw had inconsistent results
    r1 = Rectangle(Point(100,600), Point(800,500))
    r1.setFill(color_rgb(24, 123, 24))
    r1.setOutline(color_rgb(24, 123, 24))
    r1.draw(w)
    r2 = Rectangle(Point(100,250), Point(800,350))
    r2.setFill(color_rgb(24, 123, 24))
    r2.setOutline(color_rgb(24, 123, 24))
    r2.draw(w)
    return dbchk,bet

# ==============================================================================

def checkAce(player,count):
    """ player = list with card objects and graphical objects of cards alternating
        count = sum of the value of cards in players hand
        ---when aces are in hand, converts first ace with value of 11 to
        a value of 1 as necessary to prevent busting
        i.e. if count > 21:
                count = checkAce(player,count) """
    vals = [] # Values for each card in hand
    for i in range(0,len(player),2): # separate card objects from graphical object
        vals.append(player[i].getValue())  # grab value of each card object in list
    # checks values for 11, returns 11 if present, 0 if not
    f = next((i for i in vals if i==11),0)
    if f == 11:
        # finds index in values of first ace and then adjusting to get player index of that ace
        g = (vals.index(11) + 1) * 2 - 2
        player[g].setValue(player[g].getValue() - 10) # change ace value from 11 to 1
        count -= 10 # adjust player count for display text
    return count


# ==============================================================================

if __name__ == '__main__':
    main()
