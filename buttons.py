# button.py
from graphics import *
from math import sqrt


class Button:

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, centerPoint, width, height, 'Quit') """

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('blue')
        self.rect.draw(win)
        self.label = Text(center, label)

        self.deactivate(win)

    def clicked(self, p):
        """Returns true if button active and p is inside"""
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        """Returns the label string of this button."""
        return self.label.getText()

    def activate(self,win):
        """Sets this button to 'active'."""
        self.rect.draw(win)
        self.label.draw(win)
        self.label.setFill("white")
        self.active = True

    def deactivate(self,win):
        """Sets this button to 'inactive'."""
        self.rect.undraw()
        self.label.undraw()
        self.active = False

# ==============================================================================

class CButton:

    """A button is a labeled circle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, radius, label):
        """ Creates a Circle button, eg:
        qb = CButton(myWin, centerPoint, radius, 'Quit') """

        self.circ = Circle(center, radius)
        self.circ.setFill('lightgray')
        self.circ.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate(win)

    def clicked(self, p):
        """Returns true if button active and p is inside"""
        # measures distance of click from center poin of circle button, if less than radius, click is on button
        distance = sqrt((p.getX() - self.circ.getCenter().getX())**2 + (p.getY() - self.circ.getCenter().getY())**2)

        return (self.active and
                distance <= self.circ.getRadius())

    def getLabel(self):
        """Returns the label string of this button."""
        return self.label.getText()

    def activate(self,win):
        """Sets this button to 'active'."""
        self.circ.draw(win)
        self.label.draw(win)
        self.label.setFill("white")
        self.active = True

    def deactivate(self,win):
        """Sets this button to 'inactive'."""
        self.circ.undraw()
        self.label.undraw()
        self.active = False

# ==============================================================================
# SAMPLE CODE FOR EACH STYLE BUTTON IMPLAMENTATION

# Button ex.
#    rollButton = Button(win, Point(5,4.5), 6, 1, "Roll Dice")
#    rollButton.activate()
#    quitButton = Button(win, Point(5,1), 2, 1, "Quit")
#
#    # Event loop
#    pt = win.getMouse()
#    while not quitButton.clicked(pt):
#        if rollButton.clicked(pt):
#            value1 = randrange(1,7)
#            die1.setValue(value1)
#            value2 = randrange(1,7)
#            die2.setValue(value2)
#            quitButton.activate()
#        pt = win.getMouse()

# ==============================================================================
# Cbutton ex.
#    rollButton = CButton(win, Point(3,1.9), 1.75, "Roll Dice")
#    rollButton.activate()
#    quitButton = CButton(win, Point(7,1.9), 1.75, "Quit")
#
#    # Event loop
#    pt = win.getMouse()
#    while not quitButton.clicked(pt): # check for quit button clicked after each click
#        if rollButton.clicked(pt): # check for roLl button clicked if not quit button
#            value1 = randrange(1,7) #rolls die
#            die1.setValue(value1)
#            value2 = randrange(1,7) #rolls die
#            die2.setValue(value2)
#            quitButton.activate()
#        pt = win.getMouse()



