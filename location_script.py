import math

# Locations can also be created programmatically, e.g. 10 locations in a semicircle
# in the temporal retina, with radius 4 deg:

location_script = []
radius_array = [2.0,4.0]
steps = 5

theta_start_deg = 60
theta_step_deg = -30

theta_deg_array = [theta_start_deg+theta_step_deg*k for k in range(steps)]

# let's establish the vertical coordinates at the first radius, and then use those
# to calculate the coordinates for all eccentricities

y_coordinates = [-2,-1,0,1,2]

for radius in radius_array:
    for y in y_coordinates:
        x = math.sqrt(radius**2-y**2)
        location_script.append((x,y))
    

        
