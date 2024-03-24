reward_object = reward()

def reward_function(params):
    # all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    speed = params['speed']
    is_left_of_center = params['is_left_of_center']
    is_offtrack = params['is_offtrack']
    is_reversed = params['is_reversed']
    steering_angle = params['steering_angle']
    multiplier = 1
    # distance_from_center = params['distance_from_center']
    # heading = params['heading']
    # progress = params['progress']
    # steps = params['steps']
    # track_width = params['track_width']
    # waypoints = params['waypoints']
    # closest_waypoints = params['closest_waypoints']

    if is_offtrack or is_reversed:
        return zero_val
    
    reward = reward_object.reward_fuction(params)

    # calculate reward amunt
    if pixcelmap_blue_dict.get((x,y), 0):
        reward += 5

    # calculate reward amount
    if pixcelmap_red_dict.get((x,y), 0):
        reward *= 10

    return max(zero_val, reward)
