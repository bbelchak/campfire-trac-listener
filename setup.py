from setuptools import setup

setup(
    name='TracCampfireListener', version='0.2',
    packages=['campfirelistener'],
    entry_points = {
        'trac.plugins' : [
	    'campfirelistener.campfirelistener = campfirelistener.campfirelistener',
	    'campfirelistener.campfirewikilistener = campfirelistener.campfirewikilistener'
	]
    },
)
				
