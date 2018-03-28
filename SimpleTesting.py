# Program to test different functions of machine and to learn how it works

# Import library
from opentrons import robot, instruments, containers

###############################################################################

tube_rack15_50mL = containers.load('tube-rack-15_50ml', 'A2')
water = tube_rack15_50mL.wells('A3')
tip_rack1000 = containers.load('tiprack-1000ul', 'B1')
tip_trash = containers.load('trash-box', 'B2')
well_plate24 = containers.load('24-well-plate', 'A1')

p1000 = instruments.Pipette(
        axis='b',
        name='p1000',
        max_volume=1000,
        min_volume=0,
        channels=1,
        trash_container=tip_trash,
        tip_racks=[tip_rack1000])

###############################################################################

p1000.distribute(1000, water, well_plate24('A3'), blow_out=True)
# p1000.transfer(200, well_plate24('A3'), well_plate24('B3'), mix_after=(4,300))
# p1000.distribute(300, well_plate24('B1'), well_plate24('A4', 'B4', 'C4', 'D4'))
# p1000.transfer(600, well_plate24('C1'), well_plate24('A4'), mix_after=(4, 500))
