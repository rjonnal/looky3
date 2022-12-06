import math

# Locations can also be created programmatically, e.g. 10 locations in a semicircle
# in the temporal retina, with radius 4 deg:

standard_org = True
if not standard_org:
    location_script = [(0,0),(-1.5,-1.5),(1.5,-1.5),(1.5,1.5)]
else:
    location_script = []
    radius_array = [2.0,4.0,6.0,8.0]
    steps = 5
    #theta_start_deg = 45.0
    #theta_step_deg = -22.5

    theta_start_deg = 60
    theta_step_deg = -30

    theta_deg_array = [theta_start_deg+theta_step_deg*k for k in range(steps)]

    # let's establish the vertical coordinates at the first radius, and then use those
    # to calculate the coordinates for all eccentricities

    y_coordinates = [-2,-1,0,1,2]

    #for theta_deg in theta_deg_array:
    #    theta = theta_deg/180.0*math.pi
    #    x = math.cos(theta)*radius_array[0]
    #    y = math.sin(theta)*radius_array[0]
    #    y_coordinates.append(y)

    for radius in radius_array:
        for y in y_coordinates:
            # no negative sign because right eye
            x = math.sqrt(radius**2-y**2)
            location_script.append((x,y))
        

    # for radius in radius_array:
    #     for theta_deg in theta_deg_array:
    #         theta = theta_deg/180.0*math.pi
            
    #         x = math.cos(theta)*radius
    #         y = math.sin(theta)*radius
    #         location_script.append((x,y))
        
