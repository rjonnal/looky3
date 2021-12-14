import math

# Locations can also be created programmatically, e.g. 10 locations in a semicircle
# in the temporal retina, with radius 4 deg:

location_script = []
radius_array = [2.0,4.0,6.0,8.0]
steps = 5
theta_start_deg = 45.0
theta_step_deg = -22.5

theta_deg_array = [theta_start_deg+theta_step_deg*k for k in range(steps)]


for radius in radius_array:
    for theta_deg in theta_deg_array:
        theta = theta_deg/180.0*math.pi
        
        x = math.cos(theta)*radius
        y = math.sin(theta)*radius
        location_script.append((x,y))
        
