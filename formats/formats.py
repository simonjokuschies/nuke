import nuke

def setFormats():
	# formats 
	formats = [
	    '1920 1080 1.0 FullHD',
	    '960 540 1.0 HalfHD',
	    '1920 817 cinemaHD'
	]
	for curFormat in formats:
	    nuke.addFormat (curFormat)


	root = nuke.root()
	root['format'].setValue( 'FullHD' )

