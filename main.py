import os
import sys
from classes.plall import PlAll

param = ''
if (len(sys.argv) > 1):
	param = sys.argv[1]

configPath = os.path.dirname(os.path.realpath(__file__))
PlAll(configPath).pullall(param)
