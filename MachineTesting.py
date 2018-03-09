# Program to test different functions of machine and to learn how it works

# Import library
from opentrons import robot, instruments, containers

###############################################################################
# Initialize containers
containers.list()

# 96 well plate in A1
well_plate96 = containers.load('96-flat', 'A1')

# Tube rack (2 mL) in A2
tube_rack2mL = containers.load('tube-rack-2ml', 'A2')

# Tube rack (15/50 mL) in A3
tube_rack15_50mL = containers.load('tube-rack-15_50ml', 'A3')

# Tips (10, 200 and 1000) in B1 and B2
tip_rack200 = containers.load('tiprack-200ul', 'B1')
tip_rack1000 = contaienrs.load('tiprack-1000ul', 'B2')

###############################################################################
