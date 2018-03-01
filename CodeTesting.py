from opentrons import containers, instruments, robot

plate = containers.load('96-flat', 'A1')
reagents = containers.load('tube-rack-2ml', 'A2')


for well in plate.rows(0, 1, 2):
    print(well)
for well in plate.cols(0,1,2):
    print(well)

f_primer = reagents.wells('A2', length=8)

for well in f_primer:
    print(well)




    
