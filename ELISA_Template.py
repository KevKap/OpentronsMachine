# General ELISA Protocol from Ray-Biotech

# https://www.raybiotech.com/files/manual/ELISA/ELH-IL6.pdf

##############################################################################
# Import Statements
from opentrons import containers, instruments, robot

######################################################
# Container Initialization

# 200 ul Tip Racks at 'B1', 'B2', 'B3' and 1000 uL at D3
p200rack = containers.load('tiprack-200ul', 'C1', 'p200-rack')
p200rack2 = containers.load('tiprack-200ul', 'C2', 'p200-rack2')
p200rack3 = containers.load('tiprack-200ul', 'C3', 'p200-rack3')
p1000rack = containers.load('tiprack-1000ul', 'D3', 'p1000-rack')

# Assay Plate (dilution plate and actual ELISA plate) and samples in 96 well
# These three plates are in A column
reaction_plate = containers.load('96-PCR-flat', 'A1')
serial_dilution_samples = containers.load('tube-rack-2ml', 'A2')
samples = containers.load('96-PCR-flat', 'A3')

# Supplies and trash (supplies in B column, trash in D)
wash_buffer = containers.load('trough-1row-25ml', 'B1')
reagents = containers.load('tube-rack-15_50ml', 'B2')
# Bottom of tip container
liquid_trash1 = containers.load('point', 'D1', 'liquid trash')
tip_trash = containers.load('trash-box', 'D2', 'tip trash')

diluentB = reagents.wells('A3')  # 50 mL conical
detection_antibody = reagents.wells('A1')  # 15 mL conical
HRP_strep = reagents.wells('B1')  # 15 mL conical
# Standard stock is in C1 of serial plate, the dilution series will be in
# The A1-A2 columns of this plate
standard_stock = serial_dilution_samples.wells('A3')

# Pipettes

p200_multi = instruments.Pipette(axis = 'a',
            name='p200-multi',
            max_volume=200,
            min_volume=20,
            channels=8,
            trash_container=tip_trash,
            tip_racks=[p200rack, p200rack2, p200rack3])

p1000 = instruments.Pipette(
            axis='a',
            name='p1000',
            max_volume=1000,
            min_volume=100,
            channels=1,
            trash_container=tip_trash,
            tip_racks=[p1000rack])

p200 = instruments.Pipette(
        axis='a',
        name='p200',
        max_volume=200,
        min_volume=20,
        channels=1,
        trash_container=tip_trash,
        tip_racks=[p200rack, p200rack2, p200rack3])

######################################################
# Standard Creation

# First dispense 400 uL of diluent B to every well (440 in A1)
p1000.distribute(400, diluentB, serial_dilution_samples.wells(length = 8),
                    disposal_vol=0)

p200.transfer(40, diluentB, serial_dilution_samples.wells('A1'))

# Trasnfer 40 uL of standard into A1 with 4 mixes of 100 uL after
p200.transfer(40, standard_stock, serial_dilution_samples('A1'),
                mix_after=(4,100))

# Repeatedly trasnfer 200 uL from one well into the next to make serial dilution
p200.transfer(200, serial_dilution_samples('A1'), serial_dilution_samples('B1'),
            mix_after=(4,100))
p200.transfer(200, serial_dilution_samples('B1'), serial_dilution_samples('C1'),
            mix_after=(4,100))
p200.transfer(200, serial_dilution_samples('C1'), serial_dilution_samples('D1'),
            mix_after=(4,100))
p200.transfer(200, serial_dilution_samples('D1'), serial_dilution_samples('A2'),
            mix_after=(4,100))
p200.transfer(200, serial_dilution_samples('A2'), serial_dilution_samples('B2'),
            mix_after=(4,100))
p200.transfer(200, serial_dilution_samples('B2'), serial_dilution_samples('C2'),
            mix_after=(4,100))

######################################################
# Sample and standard distribution (100 uL into each well of assay plate)
p200.transfer(100, serial_dilution_samples(length = 8), reaction_plate(length=8),
            new_tip='always')

# Trasnfers 100 uL from each of the samples into the assay plate following the
# standards in the plate
for i in range(11):
    # It starts from the beginning on the sample plate, but the second column
    # of the reaction plate due to the standards being in column 1
    p200_multi.transfer(100,
    samples[8*i:8*(i+1)],
    reaction_plate[8*(i+1):8*(i+2)],
    new_tip='always')

# 2.5 hour delay for incubation at room temperature
# delay(minutes=150)

# Transfering all samples back to original wells for use in other tests
for i in range(11):
    # Reverse of the for loop above
    p200_multi.transfer(100,
    reaction_plate[8*(i+1):8*(i+2)],
    samples[8*i:8*(i+1)],
    new_tip='always')

######################################################
# Defining Wash Function

def ElisaWash():
    # Pick up set of tips used for wash steps (one set the entire time)
    p200_multi.pick_up_tip(p200rack3)
    for i in range(3):
        # Repeats 4 times (through every well)
            for i in range(12):
                # Adds 300 uL wash buffer to each well
                p200_multi.transfer(300, wash_buffer,
                                    reaction_plate[8*i:8*(i+1)],
                                    new_tip='never')
            for i in range(12):
                #Removes 300 uL wash buffer and puts in liquid trash_container
                p200_multi.transfer(300, reaction_plate[8*i:8*(i+1)],
                                liquid_trash1, new_tip='never')
    # Drop tips off in waste after wash step
    p200_multi.drop_tip(tip_trash)
    return None

ElisaWash()

# Just for testing new pieces of code
#robot.clear_commands()
#for c in robot.commands():
    #print(c)
