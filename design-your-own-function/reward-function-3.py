def reward_function(params):
    
    # 如果赛车在赛道上并且已经行驶了一些步数，计算奖励
    if params["all_wheels_on_track"] and params["steps"] > 0: 
        # 奖励现在更加重视速度
        # 速度被提高到三次方以更加强调
        reward = ((params["progress"] / params["steps"]) * 10) + (params["speed"]**3)
    else:
        # 如果赛车偏离赛道或者还没有开始，奖励是最小的
        reward = 0.01
        
    return float(reward)
