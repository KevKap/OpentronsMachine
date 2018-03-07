# General ELISA Protocol from Ray-Biotech

# V. REAGENT PREPARATION
# 1. Bring all reagents and samples to room temperature (18 - 25ºC) before use.
# 2. Assay Diluent B (Item E) should be diluted 5-fold with deionized or distilled water before
# use.
# 3. Sample dilution: Assay Diluent A (Item D) should be used for dilution of serum and
# plasma samples. 1X Assay Diluent B (Item E) should be used for dilution of cell culture
# supernatant samples. The suggested dilution for normal serum/plasma is 2 fold.
# Note: Levels of IL-6 may vary between different samples. Optimal dilution factors for
# each sample must be determined by the investigator.
# 4. Preparation of standard: Briefly spin a vial of Item C. Add 500 µl Assay Diluent A (for
# serum/plasma samples) or 1X Assay Diluent B (for cell culture medium) into Item C vial
# to prepare a 12,000 pg/ml standard. Dissolve the powder thoroughly by a gentle mix.
# Add 40 µl IL-6 standard from the vial of Item C, into a tube with 440 µl Assay Diluent A
# or 1X Assay Diluent B to prepare a 1000 pg/ml standard solution. Pipette 400 µl Assay
# Diluent A or 1X Assay Diluent B into each tube. Use the 1000 pg/ml standard solution to
# produce a dilution series (shown below). Mix each tube thoroughly before the next
# transfer. Assay Diluent A or 1X Assay Diluent B serves as the zero standard (0 pg/ml).
# 5. If the Wash Concentrate (20X) (Item B) contains visible crystals, warm to room
# temperature and mix gently until dissolved. Dilute 20 ml of Wash Buffer Concentrate into
# deionized or distilled water to yield 400 ml of 1X Wash Buffer.
# 6. Briefly spin the Detection Antibody vial (Item F) before use. Add 100 µl of 1X Assay
# Diluent B (Item E) into the vial to prepare a detection antibody concentrate. Pipette up
# and down to mix gently (the concentrate can be stored at 4ºC for 5 days). The detection
# antibody concentrate should be diluted 80-fold with 1X Assay Diluent B (Item E) and
# used in step 5 of Part VI Assay Procedure.
# 7. Briefly spin the HRP-Streptavidin concentrate vial (Item G) and pipette up and down to
# mix gently before use, as precipitates may form during storage. HRP-Streptavidin
# concentrate should be diluted 600-fold with 1X Assay Diluent B (Item E).
# For example: Briefly spin the vial (Item G) and pipette up and down to mix gently. Add
# 25 µl of HRP-Streptavidin concentrate into a tube with 15 ml 1X Assay Diluent B to
# prepare a final 600 fold diluted HRP-Streptavidin solution (don't store the diluted solution
# for next day use). Mix well.
#
# VI. ASSAY PROCEDURE
# 1. Bring all reagents and samples to room temperature (18 - 25ºC) before use. It is
# recommended that all standards and samples be run at least in duplicate.
# 2. Label removable 8-well strips as appropriate for your experiment.
# 3. Add 100 µl of each standard (see Reagent Preparation step 3) and sample into
# appropriate wells. Cover wells and incubate for 2.5 hours at room temperature with
# gentle shaking.
# 4. Discard the solution and wash 4 times with 1X Wash Solution. Wash by filling each well
# with Wash Buffer (300 µl) using a multi-channel Pipette or autowasher. Complete
# removal of liquid at each step is essential to good performance. After the last wash,
# remove any remaining Wash Buffer by aspirating or decanting. Invert the plate and blot
# it against clean paper towels.
# 5. Add 100 µl of 1X prepared biotinylated antibody (Reagent Preparation step 6) to each
# well. Incubate for 1 hour at room temperature with gentle shaking.
# 6. Discard the solution. Repeat the wash as in step 4.
# 7. Add 100 µl of prepared Streptavidin solution (see Reagent Preparation step 7) to each
# well. Incubate for 45 minutes at room temperature with gentle shaking.
# 6
# 8. Discard the solution. Repeat the wash as in step 4.
# 9. Add 100 µl of TMB One-Step Substrate Reagent (Item H) to each well. Incubate for 30
# minutes at room temperature in the dark with gentle shaking.
# 10. Add 50 µl of Stop Solution (Item I) to each well. Read at 450 nm immediately.


##############################################################################
# Import Statements
from opentrons import containers, instruments, robot

####################################
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
wash_buffer = containers.load('point', 'B1')
reagents = containers.load('tube-rack-15_50ml', 'B2')
# Bottom of tip container
liquid_trash1 = containers.load('point', 'D1', 'liquid trash')

diluentB = reagents.wells('A3')  # 50 mL conical
detection_antibody = reagents.wells('A1')  # 15 mL conical
HRP_strep = reagents.wells('B1')  # 15 mL conical
# Standard stock is in B2 of sample plate, the dilution series will be in
# The A row of this plate
standard_stock = serial_dilution_samples.wells('B1')

####################################
# Standard Creation
