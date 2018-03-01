
# coding: utf-8

# # <strong>Sigma Aldrich Nitric Oxide Synthase Detection</strong>

# ## <em>Measures free nitric oxide and nictric oxide synthase activity in living cells</em>

# In[1]:


# Imports
from opentrons import containers, instruments, robot
from IPython.display import Image


# #### Supply Initialization

# In[2]:


# Tip Racks

tiprack_1 = containers.load('tiprack-1000ul', 'B1')
tiprack_2 = containers.load('tiprack-200ul', 'B2')
tiprack_3 = containers.load('tiprack-10ul', 'B3')

# Assay, trash, and supplies
    # Assay is set to be a 96-flat, but the measurements of a black/clr bottom plate
    # Should be compared and updated if relevant

assay_plate = containers.load('96-flat', 'A1')
trash = containers.load('trash-box', 'D1')
large_supplies = containers.load('tube-rack-15_50ml', 'C1')
small_supplies = containers.load('tube-rack-2ml', 'C2')

# Pipettes

pipette_1000 = instruments.Pipette(axis = 'a', name = 'P1000',
                                  max_volume = 1000, min_volume = 100,
                                  tip_racks = [tiprack_1], trash_container = trash)
pipette_200 = instruments.Pipette(axis = 'a', name = 'P200',
                                 max_volume = 200, min_volume = 20,
                                 tip_racks = [tiprack_2], trash_container = trash)
pipette_10 = instruments.Pipette(axis = 'a', name = 'P10',
                                 max_volume = 10, min_volume = 1,
                                 tip_racks = [tiprack_3], trash_container = trash)

# #### Making Stock Solution

# In[5]:


# Dependent on number of wells being used
# Assumes 1 control well for each condition with no dye, 3 for everything else
dye_well_number = 75  # this should be changed to match well numbers adjusted with
                      # pipetting error
nodye_well_number = 35

# Amount of the solutions needed (taken from image above)
dye_arginine_substrate_solution = 10*dye_well_number
dye_daf2da_solution = 0.1*dye_well_number
dye_reaction_buffer = 190*dye_well_number

nodye_arginine_substrate_solution = 10*nodye_well_number
nodye_reaction_buffer = 190*nodye_well_number

# Supply Assignment is in wells corresponding to plates above
# Arginine Substrate A1
# DAF-2 DA A2
# Reaction Buffer A3 (50 mL)

# Makes stock for Dye (50 mL in A4)
pipette_1000.transfer(dye_arginine_substrate_solution, small_supplies('A1'),
                      large_supplies('A4'))  # Arginine substrate
pipette_1000.transfer(dye_reaction_buffer, large_supplies('A3'), large_supplies('A4'))
pipette_10.transfer(dye_daf2da_solution, small_supplies('A2'), large_supplies('A4'))
pipette_1000.mix(4, 1000, large_supplies('A4'))  # Mixes stock solution

# Makes stock without Dye (50 mL in B3)
pipette_1000.transfer(nodye_arginine_substrate_solution, small_supplies('A1'),
                     large_supplies('B3')) # Arginine substrate
pipette_1000.transfer(nodye_reaction_buffer, large_supplies('A3'), large_supplies('B3'))
pipette_1000.mix(4, 1000, large_supplies('B3'))


# #### Assay

# In[6]:


# Transfer 200 ul of stock to each well

Active_wells = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
               'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
               'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
               'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
               'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
               'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
               'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',
               'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']

# Dye stock
pipette_1000.distribute(200, large_supplies('A4'), assay_plate())

pipette_1000.delay(minutes=40)
