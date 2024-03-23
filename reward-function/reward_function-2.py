# Import package (needed for heading)
import math

def reward_function(params):

    ################## HELPER FUNCTIONS ###################
    # 计算两点之间的欧几里得距离
    # 用来计算赛车与赛道上特定点之间的距离
    def dist_2_points(x1, x2, y1, y2):
        return abs(abs(x1-x2)**2 + abs(y1-y2)**2)**0.5

    # 在找到赛车当前位置最近的两个赛道点
    def closest_2_racing_points_index(racing_coords, car_coords):

        # Calculate all distances to racing points
        distances = []
        for i in range(len(racing_coords)):
            distance = dist_2_points(x1=racing_coords[i][0], x2=car_coords[0],
                                        y1=racing_coords[i][1], y2=car_coords[1])
            distances.append(distance)

        # Get index of the closest racing point
        closest_index = distances.index(min(distances))

        # Get index of the second closest racing point
        distances_no_closest = distances.copy()
        distances_no_closest[closest_index] = 999
        second_closest_index = distances_no_closest.index(
            min(distances_no_closest))

        return [closest_index, second_closest_index]

    # 计算赛车与最近的赛道线之间的距离
    def dist_to_racing_line(closest_coords, second_closest_coords, car_coords):
        
        # Calculate the distances between 2 closest racing points
        a = abs(dist_2_points(x1=closest_coords[0],
                                x2=second_closest_coords[0],
                                y1=closest_coords[1],
                                y2=second_closest_coords[1]))

        # Distances between car and closest and second closest racing point
        b = abs(dist_2_points(x1=car_coords[0],
                                x2=closest_coords[0],
                                y1=car_coords[1],
                                y2=closest_coords[1]))
        c = abs(dist_2_points(x1=car_coords[0],
                                x2=second_closest_coords[0],
                                y1=car_coords[1],
                                y2=second_closest_coords[1]))

        # Calculate distance between car and racing line (goes through 2 closest racing points)
        # try-except in case a=0 (rare bug in DeepRacer)
        try:
            distance = abs(-(a**4) + 2*(a**2)*(b**2) + 2*(a**2)*(c**2) -
                            (b**4) + 2*(b**2)*(c**2) - (c**4))**0.5 / (2*a)
        except:
            distance = b

        return distance

    # Calculate which one of the closest racing points is the next one and which one the previous one
    # 通过模拟赛车沿着当前航向前进的情况，来计算赛车与最近两个赛道点的新距离，并根据这些距离来判断哪个是下一个赛道点
    # def next_prev_racing_point(closest_coords, second_closest_coords, car_coords, heading):

    #     # Virtually set the car more into the heading direction
    #     heading_vector = [math.cos(math.radians(
    #         heading)), math.sin(math.radians(heading))]
    #     new_car_coords = [car_coords[0]+heading_vector[0],
    #                         car_coords[1]+heading_vector[1]]

    #     # Calculate distance from new car coords to 2 closest racing points
    #     distance_closest_coords_new = dist_2_points(x1=new_car_coords[0],
    #                                                 x2=closest_coords[0],
    #                                                 y1=new_car_coords[1],
    #                                                 y2=closest_coords[1])
    #     distance_second_closest_coords_new = dist_2_points(x1=new_car_coords[0],
    #                                                         x2=second_closest_coords[0],
    #                                                         y1=new_car_coords[1],
    #                                                         y2=second_closest_coords[1])

    #     if distance_closest_coords_new <= distance_second_closest_coords_new:
    #         next_point_coords = closest_coords
    #         prev_point_coords = second_closest_coords
    #     else:
    #         next_point_coords = second_closest_coords
    #         prev_point_coords = closest_coords

    #     return [next_point_coords, prev_point_coords]

    #  函数生成一个循环索引列表
    def indexes_cyclical(start, end, array_len):

        if end < start:
            end += array_len

        return [index % array_len for index in range(start, end)]

    #################### RACING LINE ######################

    # Optimal racing line for the DeepRacer Championship Cup
    # Each row: [x, y]
    racing_track = []

    ################## INPUT PARAMETERS ###################

    # Read all input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    heading = params['heading']
    progress = params['progress']
    steps = params['steps']
    speed = params['speed']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    is_offtrack = params['is_offtrack']

    ############### OPTIMAL X,Y,SPEED,TIME ################

    # Get closest indexes for racing line (and distances to all points on racing line)
    closest_index, second_closest_index = closest_2_racing_points_index(
        racing_track, [x, y])

    # Get optimal [x, y, speed, time] for closest and second closest index
    optimals = racing_track[closest_index]
    optimals_second = racing_track[second_closest_index]

    # Save first racingpoint of episode for later
    if steps == 1:
        first_racingpoint_index = closest_index
    else: first_racingpoint_index = 0

    ################ REWARD AND PUNISHMENT ################

    ## Define the default reward ##
    reward = 1

    ## Reward if car goes close to optimal racing line ##
    DISTANCE_MULTIPLE = 1
    dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])
    distance_reward = max(1e-3, 1 - (dist/(track_width*0.5)))
    reward += distance_reward * DISTANCE_MULTIPLE

    ## Reward if speed is close to optimal speed ##
    SPEED_DIFF_NO_REWARD = 1
    SPEED_MULTIPLE = 3
    speed_diff = abs(optimals[2]-speed)
    if speed_diff <= SPEED_DIFF_NO_REWARD:
        # we use quadratic punishment (not linear) bc we're not as confident with the optimal speed
        # so, we do not punish small deviations from optimal speed
        speed_reward = (1 - (speed_diff/(SPEED_DIFF_NO_REWARD))**2)**2
    else:
        speed_reward = 0
    reward += speed_reward * SPEED_MULTIPLE


        
    ## Incentive for finishing the lap in less steps ##
    # REWARD_FOR_FASTEST_TIME = 2000 # should be adapted to track length and other rewards
    # STANDARD_TIME = 9.5  # seconds (time that is easily done by model)
    # FASTEST_TIME = 7.5  # seconds (best time of 1st place on the track)
    # if progress == 100:
    #     finish_reward = max(1e-3, (-REWARD_FOR_FASTEST_TIME /
    #                 (15*(STANDARD_TIME-FASTEST_TIME)))*(steps-STANDARD_TIME*15))
    # else:
    #     finish_reward = 0
    # reward += finish_reward
    
    ## Zero reward if off track ##
    if all_wheels_on_track == False:
        reward = 1e-3
        
    #################### RETURN REWARD ####################
    
    # Always return a float value
    return float(reward)