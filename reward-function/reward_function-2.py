def reward_function(params):

    center_variance = params["distance_from_center"] / params["track_width"]

    left_lane = [13,14,15,16,17,18,19,20,21,22,23,24,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67]
    right_lane = [30,31,32,33,34,35,36,37]
    center_lane = [0,1,2,3,4,5,6,7,8,9,10,11,12,25,26,27,28,29,38,39,68,69]

    reward = 0
    
    if params["all_wheels_on_track"]:
        if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]:
            reward = 10
        elif params["closest_waypoints"][1] in right_lane and not params["is_left_of_center"]:
            reward = 10
        elif params["closest_waypoints"][1] in center_lane and center_variance < 0.3:
            reward = 10
        else:
            reward = 0.01
    else:
        reward = 0.01
        
    reward *= params["speed"]**2

    return float(reward)