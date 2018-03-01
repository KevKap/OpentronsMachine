
# coding: utf-8

# ### Quantifying dsDNA in solution
#### Invitrogen Quant-iTTM PicoGreen ® dsDNA

# #### Things to Do First

# 1. Dilute the 20X TE Buffer in nucleic acid and DNase free water
#     a. Need enough for 100 uL per reaction (give extra of 100 wells for pipetting error/other uses)
#     b. Place in 50 mL conical in position A3 in 15_50 mL tube rack
# 2. Prepare Quant-iT PicoGreen reagent (200 dilution in TE buffer)
#     a. Enough for 100 uL per reaction (should be using the 1X TE buffer made above)
#     b. Wrap tube in foil and place in 15 mL conical in position A1 in the 15_50 mL tube rack
# 3. Preapre dsDNA Lambda 2 ug/mL standard in 2 mL cap and place in A1 in 2mL tube rack
#     a. 1.47 mL 1X TE buffer
#     b. 30 uL 100 ug/mL standard
# 4. Edit plate_layout below to match the wells being used in the assay
# 5. Edit high_range in code for choice of high range standard curve or low range (True for high/False for low range)
#     a. High: 1 ng/mL - 1 ug/mL
#     b. Low: 25 pg/mL - 25 ng/mL
# 6. Load empty 2 mL caps in A2-A6 and B1 for standards
# 7. Change number_of_samples to number of samples being analyzed (analyzed in triplicates)
# 8. Change dilution_fold to represent fold of dilution for samples (1:10 would be 10)
# 9. Place samples in 2 mL tube rack starting in row C

# #### Code

# In[44]:


# User Variables for Experiment
plate_layout = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
               'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
               'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
               'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
               'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
               'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
               'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',
               'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']

high_range = True
low_range = not(high_range)

number_of_samples = 10
dilution_fold = 10


# In[53]:


# Import Statements
from opentrons import containers, instruments, robot

# In[46]:


# Supply Initializing

# Tip Racks
tiprack_1000 = containers.load('tiprack-1000ul', 'B1')
tiprack_200 = containers.load('tiprack-200ul', 'B2')
tiprack_10 = containers.load('tiprack-10ul', 'B3')

# Assay Plate
assay_plate = containers.load('96-flat', 'A1')

# Trash
trash = containers.load('trash-box', 'D1')

# Supplies
large_supplies = containers.load('tube-rack-15_50ml', 'C1')
small_supplies = containers.load('tube-rack-2ml', 'C2')

TE = large_supplies.wells('A3')
dsDNA = small_supplies.wells('A1')
standards = small_supplies.wells('A2','A3', 'A4', 'A5', 'A6')
dilutedsDNA = small_supplies.wells('B1')

print(standards[5])

# Pipettes
pipette_1000 = instruments.Pipette(axis='a', name='P1000',
                               max_volume=1000, min_volume=100,
                               tip_racks=[tiprack_1000], trash_container=trash)
pipette_200 = instruments.Pipette(axis='a', name='P200',
                              max_volume=200, min_volume=20,
                              tip_racks=[tiprack_200], trash_container=trash)
pipette_10 = instruments.Pipette(axis='a', name='P10',
                                max_volume=10, min_volume=1,
                                tip_racks=[tiprack_10], trash_container=trash)


# In[47]:


# Everything adjusted for 200 uL per well for reading in a 96 well microplate (protocol for 2 mL)
# 100 uL of picogreen reagent per well
# Assumes that the assay buffer and 2 ug/mL workign solution is already made

# Standard Creation
# Uses 2 ug/mL working solution in position A1 in 2 mL plate

if high_range:
    # Putting 1X TE in appropriate standard wells
    pipette_1000.transfer(900, TE, standards[1])  # 100 ng/mL
    pipette_1000.transfer(990, TE, standards[2])  # 10 ng/mL
    pipette_1000.transfer(999, TE, standards[3])  # 1 ng/mL
    pipette_1000.transfer(1000, TE, standards[4])  # 0 ng/mL

    # Putting in 2 ug/mL DNA stock
    pipette_1000.transfer(1000, dsDNA, standards[1])  # 1 ug/mL
    pipette_200.transfer(100, dsDNA, standards[2], mix_after=(3, 50))  # 100 ng/mL
    pipette_10.transfer(10, dsDNA, standards[3], mix_after=(3, 10))  # 10 ng/mL
    pipette_10.transfer(1, dsDNA, standards[4], blow_out=True, mix_after=(3, 10))  # 1 ng/mL

elif low_range:
    # Making 40-fold dilution of 2 ug/mL working solution (going into B1)
    pipette_1000.transfer(1462.5, TE, dilutedsDNA)
    pipette_200.trasnfer(37.5, dsDNA, dilutedsDNA, mix_after=(3, 100))

    # Putting 1X TE in appropriate standard wells
    pipette_1000.transfer(900, TE, standards[1])  # 2.5 ng/mL
    pipette_1000.transfer(990, TE, standards[2])  # 250 pg/mL
    pipette_1000.transfer(999, TE, standards[3])  # 25 pg/mL
    pipette_1000.transfer(1000, TE, standards[4])  # 0 ng/mL

    # Putting in 50 ng/mL DNA stock
    pipette_1000.transfer(1000, dilutedsDNA, standards[0])  # 25 ug/mL
    pipette_200.transfer(100, dilutedsDNA, standards[1], mix_after=(3, 50))  # 2.5 ng/mL
    pipette_10.transfer(10, dilutedsDNA, standards[2], mix_after=(3, 10))  # 250 pg/mL
    pipette_10.transfer(1, dilutedsDNA, standards[3], blow_out=True, mix_after=(3, 10))  # 25 pg/mL


# In[51]:


# Analysis

# Used for automating replicate well placements
plate_lettering = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
plate_numbers = [i for i in range(1,13)]

# Determines amount of TE buffer needed to make dilution
TE_amount = 100 - 100/dilution_fold
sample_amount = 100/dilution_fold
# Standards done in triplicates
for i in range(2,7):
    # Places 100 uL of the appropriate standard into the first three columns of rows A-E in assay plate
    pipette_1000.distribute(100, small_supplies('A'+str(i)), assay_plate(plate_lettering[i-2]+'1',
                                                                         plate_lettering[i-2]+'2',
                                                                        plate_lettering[i-2]+'3'))

# Samples

for i in range(number_of_samples):
    # Places required amount of TE in wells in assay plate for dilution
    if i <= 7:
        pipette_1000.distribute(TE_amount, large_supplies('A3'), assay_plate(plate_lettering[i]+'4',
                                                                            plate_lettering[i]+'5',
                                                                            plate_lettering[i]+'6'))
    elif 7 < i <= 14:
        pipette_1000.distribute(TE_amount, large_supplies('A3'), assay_plate(plate_lettering[i%8]+'7',
                                                                            plate_lettering[i%8]+'8',
                                                                            plate_lettering[i%8]+'9'))
    elif 15 <= i:
        pipette_1000.distribute(TE_amount, large_supplies('A3'), assay_plate(plate_lettering[(i+1)%8]+'10',
                                                                            plate_lettering[(i+1)%8]+'11',
                                                                          plate_lettering[(i+1)%8]+'12'))

for i in range(1,number_of_samples+1):
    # Places sample in each of the designated wells
    # Sample 1 -> A4-A6, Sample 2 -> B4-B6, ...., Sample 9 -> A7-9, etc
    if i <= 6:
        pipette_200.distribute(sample_amount, small_supplies('C'+str(i)), assay_plate(plate_lettering[i-1]+'4',
                                                                                     plate_lettering[i-1]+'5',
                                                                                     plate_lettering[i-1]+'6'))
    elif 7 <= i <= 8:
        pipette_200.distribute(sample_amount, small_supplies('D'+str((i%7)+1)), assay_plate(plate_lettering[i-1]+'4',
                                                                                           plate_lettering[i-1]+'5',
                                                                                           plate_lettering[i-1]+'6'))
    elif 9 <= i <= 12:
        pipette_200.distribute(sample_amount, small_supplies('D'+str((i%7)+1)), assay_plate(plate_lettering[(i%8)-1]+'7',
                                                                                           plate_lettering[(i%8)-1]+'8',
                                                                                           plate_lettering[(i%8)-1]+'9'))

# Putting 100 uL of picoGreen reagent into each well that was Used

pipette_1000.distribute(100, large_supplies('A1'), assay_plate(','.join(plate_layout)))
