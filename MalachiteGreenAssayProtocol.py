
# coding: utf-8

# ## Malachite Green Assay

# In[1]:


# http://docs.opentrons.com/writing.html
get_ipython().system('pip install --upgrade opentrons')


# In[10]:


# Imports
from opentrons import robot, containers, instruments


# In[18]:


# Supply initialization

# Tip Racks

tiprack_1 = containers.load('tiprack-1000ul', 'A1')  # 1000 uL tips
tiprack_2 = containers.load('tiprack-10ul', 'A2')  # 10 uL tips
tiprack_3 = containers.load('tiprack-200ul', 'A3') # 200 uL tips

# Plates

standard_tubes = containers.load('tube-rack-2ml', 'B1')
assay_plate = containers.load('96-flat', 'B2')
trash = containers.load('trash-box', 'C1')
supplies = containers.load('tube-rack-15_50ml', 'C2') # 15 mL A1 holds DI

# Pipettes

pipette_1 = instruments.Pipette(axis = 'a', name = 'my-p1000',
                                max_volume = 1000, min_volume = 100,
                               tip_racks = [tiprack_1], trash_container = trash)
pipette_2 = instruments.Pipette(axis = 'a', name = 'my-p10',
                               max_volume = 10, min_volume = 1,
                               tip_racks = [tiprack_2], trash_container = trash)
pipette_3 = instruments.Pipette(axis = 'a', name = 'my-p200',
                               max_volume = 200, min_volume = 20,
                               tip_racks = [tiprack_3], trash_container = trash)


# In[15]:


# Creating Standards

# Tube layout: D1 D2 D3 S1 S2 S3 S4 S5 S6
# Starting at 1 M Phosphate standard and make 1 mL of 10 mM by dilution 10 uL in 990 uL DI
# This is the bulk standard (bs) (D1 will be made by researcher)
# Aliquot 990 uL DI to D2, 500 uL to D3 - S6
# Add 10 uL bs to D2 (mix), then 500 uL of D2 to D3
# Take 500 uL D3 and move to S1 and repeat down line to S5 (S6 is blank)

# Moves 990 uL DI to D2 (Picks up new tip from A1 then keeps for all DI dispensing)
pipette_1.transfer(990, supplies('A1'), standard_tubes('A2'))

# Moves 500 uL DI to D2 - S6
pipette_1.distribute(500, supplies('A1'), standard_tubes('A3', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6'))

# Moves 10 uL BS to D2
pipette_2.transfer(10, standard_tubes('A1'), standard_tubes('A2'))

# Moves 500 uL D2 to D3
pipette_1.transfer(500, standard_tubes('A2'),
                   standard_tubes('A3'),
                   mix_before = (2, 300),
                   mix_after = (2, 300))  # mixes D3 after dispensing 4 times with 300 uL

# Function to move 500 uL to next one and mix

def dilution(source, destination):
    """Given source well and destination well for standard tubes it transfers 500 uL
    and mixes before and after then gets rid of tip"""
    pipette_1.transfer(500, standard_tubes(source), standard_tubes(destination),
                       mix_before = (2,300), mix_after = (2,300))

# Creating dilution series

dilution('A3', 'B1')  # Creation of S1 (25 uM)
dilution('B1', 'B2')  # Creation of S2 (12.5 uM)
dilution('B2', 'B3')  # Creation of S3 (6.25 uM)
dilution('B3', 'B4')  # Creation of S4 (3.13 uM)
dilution('B4', 'B5')  # Creation of S5 (1.56 uM)


# In[20]:


# Performing Assay (Takes place in 96 well plate)

active_wells = ['A1', 'A2', 'A3',
                'B1', 'B2', 'B3',
               'C1', 'C2', 'C3',
               'D1', 'D2', 'D3',
               'E1', 'E2', 'E3',
               'F1', 'F2', 'F3']
# Moving over standards

pipette_3.distribute(50, standard_tubes('B1'), assay_plate('A1', 'A2', 'A3'))  # Puts S1 in A1, A2, A3 on plate (triplicate)
pipette_3.distribute(50, standard_tubes('B2'), assay_plate('B1', 'B2', 'B3'))  # Puts S2 in B1, B2, B3 on plate (triplicate)
pipette_3.distribute(50, standard_tubes('B3'), assay_plate('C1', 'C2', 'C3'))  # Puts S3 in C1, C2, C3 on plate (triplicate)
pipette_3.distribute(50, standard_tubes('B4'), assay_plate('D1', 'D2', 'D3'))  # Puts S4 in D1, D2, D3 on plate (triplicate)
pipette_3.distribute(50, standard_tubes('B5'), assay_plate('E1', 'E2', 'E3'))  # Puts S5 in E1, E2, E3 on plate (triplicate)
pipette_3.distribute(50, standard_tubes('B6'), assay_plate('F1', 'F2', 'F3'))  # Puts S6 in F1, F2, F3 on plate (triplicate)

# INSERT CODE FOR INPUTTING SAMPLES (CAN BE IN OTHER TUBE RACK)

# Adding in MG Acidic Solution (in standard_tubes rack 'C1')

for well in active_wells:
    # Transfers 5 uL MG Acidic solution to each well then mixes 3 times at 7 uL
    pipette_2.transfer(5, standard_tubes('C1'), assay_plate(well), mix_after = (3, 7))

pipette_2.delay(minutes = 10)  # 10 minute RT incubation period

# Adding in MG Blue solution (in standard_tubes rack 'C2')

for well in active_wells:
    # Transfers 15 uL MG Blue solution to each well then mixes 3 times at 20 uL
    pipette_3.transfer(15, standard_tubes('C2'), assay_plate(well), mix_after = (3, 20))

pipette_3.delay(minutes = 20)  # 20 minute RT incubation period

# PROTOCOL DONE READ AT 620 NM
