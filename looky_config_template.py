# Load some color presets
from colors import *

MAX_FPS = 60
FONT = 'Courier'
FONT_SIZE = 24

SNAP_MOUSE_TO_FINE_GRID = True

# Use the 'm' key to cycle through display modes. If there's
# a preferable one, note its number and write it here.
DEFAULT_DISPLAY_MODE_INDEX = 0
# DISPLAY_MODE = (1920,1080) # prepends this to the automatically generated list of modes
# DEFAULT_DISPLAY_X_OFFSET = 1920*2 # use this to specify monitor

# DATA_MONITORING_DIRECTORY = 'E:/foo'

# Offsets for aligning the target origin with the imaging beam
X_OFFSET_DEG = 0.0
Y_OFFSET_DEG = 0.0

# Step size in visual angle degrees, as well as versions for
# fine-grained steps and offset steps (to correct misalignment
# with beam).
STEP_SIZE_DEG = 1.0
STEP_FINE_DEG = 1.0/8.0
STEP_VERY_FINE_DEG = 1.0/16.0
STEP_OFFSET_DEG = 1.0/8.0

# Screen distance and magnification
# If there are optics between the screen and the eye, calculate
# and use the optical dist. Inversions indicate whether the target
# image is flipped horizontally or vertically w/r/t the viewer.
# To invert, set relevant orientation(s) to -1.
SCREEN_DISTANCE_M = 20.5*.0254
VERTICAL_ORIENTATION = 1
HORIZONTAL_ORIENTATION = -1

# Target characteristics
RADIUS_DEG = 1.0
LINE_WIDTH_PX = 2
LINE_COLOR = WHITE
BACKGROUND_COLOR = BLACK
HELP_COLOR = BANANA
OFFSET_COLOR = RED4
EMPTY_CENTER = 1.0/16.0

# Location script--navigate to these locations using PageUp and PageDown:
# Each entry in the script should be a tuple (x,y), where x and y represent
# eccentricities given in degrees.

# Locations can be imported from a separate script:
from location_script import location_script

# Locations can be listed explicitly:
# location_script = [(-8.0,0.0),(-6.0,0.0),(-4.0,0.0),(-2.0,0.0)]

# Locations can also be created programmatically, e.g. 10 locations in a semicircle
# in the temporal retina, with radius 4 deg:

# location_script = []
# import math
# radius = 4.0
# n_steps = 10

# for theta_index in range(n_steps+1):
#     theta = theta_index*math.pi/float(n_steps)+math.pi/2.0
#     x = math.cos(theta)*radius
#     y = math.sin(theta)*radius
#     location_script.append((x,y))

