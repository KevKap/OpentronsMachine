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
# Water in A3 of tube rack (can be changed)
water = tube_rack15_50mL.wells('A3')
redColor = tube_rack15_50mL.wells('A1')  # Red liquid in A1
blueColor = tube_rack15_50mL.wells('A2')  # Blue liquid in A2

# Tips (10, 200 and 1000) in B1 and B2
tip_rack200 = containers.load('tiprack-200ul', 'B1')
tip_rack1000 = containers.load('tiprack-1000ul', 'B2')

# Trash Container B3
tip_trash = containers.load('trash-box', 'B3')
###############################################################################
# Initialize Pipettes

p300_multi = instruments.Pipette(
        axis='a',
        name='p300_multi',
        max_volume=300,
        min_volume=0,
        channels=8,
        trash_container=tip_trash,
        tip_racks=[tip_rack200])

p1000 = instruments.Pipette(
        axis='b',
        name='p1000',
        max_volume=1000,
        min_volume=0,
        channels=1,
        trash_container=tip_trash,
        tip_racks=[tip_rack1000])

###############################################################################

###############################################################################
# Actual code

# Serial dilution of blue color in 1 column of 96 well plate
# 200 -> 175 -> 150 -> 125 -> 100 -> 75 -> 50 -> 25
dilution_list = [200, 175, 150, 125, 100, 75, 50, 25]

# Blue dispensation (gets new tip each time)
for i in range(len(dilution_list)):
    p1000.transfer(dilution_list[i], blueColor, well_plate96[i])

# Water dispensation (gets new tip and mixes each time)
for i in range(1,len(dilution_list)):
    p200.transfer(200-dilution_list[i], water, well_plate96[i],
                    mix_after=(4,100))

# Using multi channel to split the 200 uL in column 1 to 75 in column 3 and
# column 5
p300_multi.transfer(75, well_plate96[0:8], well_plate96.wells('A3', length = 8))
p300_multi.transfer(75, well_plate96[0:8], well_plate96.wells('A5', length = 8))

# Red dispensation dilution seris (gets new tip each time, same as blue)

# Red dispensation (gets new tip each time)
for i in range(len(dilution_list)):
    p200.transfer(dilution_list[i], redColor, well_plate96[i+9])

# Water dispensation (gets new tip and mixes each time)
for i in range(1,len(dilution_list)):
    p200.transfer(200-dilution_list[i], water, well_plate96[i+9],
                    mix_after=(4,100))

# Using multi channel to split the 200 uL in column 2 to the tubes in 2mL tube
# rack
p200.transfer(75, well_plate96[8:16], tube_rack2mL.wells('A1', length = 8),
                new_tip='always')
p200.transfer(75, well_plate96[0:8], tube_rack2mL.wells('A3', length = 8),
                new_tip='always')


###############################################################################
for c in robot.commands():
    print(c)

###############################################################################















###############################################################################
