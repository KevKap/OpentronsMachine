# THE ROBOT DOES NOT HAVE THE PORT FOR THE MAGNETIC BOX

from opentrons import instruments


mag_deck = instruments.Magbead(name='mag_deck')

for i in range(4):
    mag_deck.engage()
    mag_deck.delay(10)
    mag_deck.disengage()
    mag_deck.delay(10)
