from opentrons import containers, instruments, robot



containers.create(

	'washing-pool',
	grid = (1, 8),
	
	#add spacing 
	spacing = (),
	diameter = 6.4,
	depth = 50

	)

1000rack = containers.load('tiprack-1000ul', 'A1', 'p20-rack')

#Change from 300 to 200
p200rack = containers.load('tiprack-200ul', 'C1', 'p200-rack')
p200rack2 = containers.load('tiprack-200ul', 'E1', 'p200-rack')

serial_dilution_plate = containers.load('96-deep-well', 'B1')
reaction_plate = containers.load('96-deep-well', 'D1')
samples = containers.load('tube-rack-2ml', 'C2')

wash_buffers = containers.load('trough-1row-25ml', 'D2')

liquid_trash = containers.load('point', 'A2', 'liquid trash')
