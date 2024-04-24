import math

# Locations can also be created programmatically, e.g. 10 locations in a semicircle
# in the temporal retina, with radius 4 deg:

standard_org = True
add_center = False # if True, (0,0) appended to script--should be the last place to test
nasal = False # for normals we use the temporal side

if not standard_org:
    location_script = [(0,0),(2,0),(4,0),(6,0),(0,2),(2,2),(4,2),(6,2),(0,-2),(2,-2),(4,-2),(6,-2)]
    dx,dy = 2,2
    location_script = [(x+dx,y+dy) for x,y in location_script]
else:
    location_script = []
    #radius_array = [2]
    radius_array = [2,4,6,8,10]
    #radius_array = [4,6,8,10]

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
            x = math.sqrt(radius**2-y**2)
            if nasal:
                x = -x
            location_script.append((x,y))
        

    # for radius in radius_array:
    #     for theta_deg in theta_deg_array:
    #         theta = theta_deg/180.0*math.pi
            
    #         x = math.cos(theta)*radius
    #         y = math.sin(theta)*radius
    #         location_script.append((x,y))
        
if add_center:
    location_script = location_script+[(0,0)]