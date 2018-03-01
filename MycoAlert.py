# Lonza MycoAlert(TM) mycoplasma detection kit

# Import statements for opentrons library
from opentrons import robot, instruments, containers

##########################################################################
# Outline of PROTOCOL

# Volume to resuspent reagents in given kit
# 10 Test kit 600 uL
# 25 Test kit 600 ul
# 50 Test kit 2.5 mL
# 100 test kit 10 mL


# 1. Bring Reagents to RT
# 2. Reconsistitue MycoAlert reagent and MycoAlert substrate in assay Buffer
#    Leave for 15 min at RT
# 3. Transfer 2 mL of cell culture supernatant and pellet at 1500 rpm (200g)
#   for 5 minutes
# 4. Transfer 100 uL of supernatant
# 5. Add 100 uL of MycoAlert reagent and wait 5 minutes
# 6. Read plate (reading A) (1 second integrated reading)
# 7. Add 100 uL of MycoAlert substrate to each sample and wait 10 min
# 8. Read plate (reading B)
# 9. Calculate ratio: Reading B/Reading A

# <0.9 negative
# 0.9 - 1.2 Borderline/quarantine cells/retest in 24 hr
# >1.2 mycoplasma contamination

## Negative control of 100 uL buffer or HPLC water

##########################################################################

# User Variables and Set Up

# Place 200 uL tips in spot B1
# Place 96 well opaque assay plate in A1
# Place 24 sample tube plate in A2 (make note of what samples are where)
# Place 15/50 mL reageent container in B2 with reagent in A1 and subsrate in B1
# Place 15 mL water in C1 in 15/50 mL container
# Place trash box in B3

# Delete cells to represent layout of assay plate, leaving comma between entries
assay_layout = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
               'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
               'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
               'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
               'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
               'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
               'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',
               'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']

# Delete cells to represent layout of sample plate
sample_layout = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6',
               'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
               'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
               'D1', 'D2', 'D3', 'D4', 'D5', 'D6']

sampleplate_number = 1

# If there is more than one sample plate (ie > 24 samples) copy and paste
# sample_layout and rename as sample_layout_2, 3, etc.. placing in A3, C1, C2
# and change sampleplate_number = 1 to reflect sample plates (up to 4)
# Additionally, place a second 200 uL tip box in spot C3

##########################################################################
# DO NOT EDIT ANYTHING BELOW THIS LINE
##########################################################################

sample_list = ['A2', 'A3', 'C1', 'C2']

# Tip Rack Initialization

tiprack_200 = containers.load('tiprack-200ul', 'B1')

if sampleplate_number >= 3:
    # If there are more than 48 samples, need more than 96 tips
    # Second box is in C3
    tiprack_200 = containers.load('tiprack-200ul', 'C3')


# Assay plate/trash
assay_plate = containers.load('96-flat', 'A1')

for plate in range(sampleplate_number):
    sample_plate = containers.load('tube-rack-2ml', sample_list[plate])

trash = containers.load('trash-box', 'B3')

# MycoAlert Reagent and Substrate

supplies = containers.load('tube-rack-15_50ml', 'B2')
reagent = supplies.wells('A1')
substrate = supplies.wells('B1')
water = supplies.wells('C1')

# Pipettes

p200 = instruments.Pipette(
            axis='a',
            name='p200',
            max_volume=200,
            min_volume=20,
            channels=1,
            trash_container=trash,
            tip_racks =[tiprack_200])

##########################################################################


# Step 4 (with blank)

# 3 blank (A1, A2, A3)
p200.distribute(100, water, assay_plate('A1', 'A2', 'A3'))

# Sample dispensing (chunks of 3 for technical replicates)
for num in range(len(sample_layout)):
    # This picks the well from the sample plates
    # Then picks the next 3 open wells in the assay plate layout by slicing
    # the plate_layout
    p200.distribute(100,
                sample_plate(sample_layout[num]),
                assay_plate(plate_layout[3*(num+1):3*(num+1)+3]))

# Distributes 100 of reagent into each well in plate_layout
p200.distribute(100, reagent, sample_layout(','.join(plate_layout)))

# 5 minute incubation period then read after delay
p200.delay(min = 5)

# 20 minute delay to allow for reading (needs to be adjusted to
# decide what is best)
p200.delay(min = 20)
