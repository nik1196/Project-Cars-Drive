import carseour
game = carseour.live()
player = game.mParticipantInfo[0]

with open('train_data.txt', 'w+') as train_data:
    while player.mLapsCompleted < 10:
        y_data = [game.mUnfilteredThrottle, game.mUnfilteredBrake]
        x_axis = game.mUnfilteredSteering
        lap_distance = player.mCurrentLapDistance
        speed = game.mSpeed
        x_pos = player.mWorldPosition[0]
        z_pos = player.mWorldPosition[2]

        y_axis = 0
        if y_data[0] > y_data[1]:
            y_axis = y_data[0]
        else:
            y_axis = -y_data[1]

        data = [[speed, lap_distance, x_pos, z_pos], [x_axis, y_axis]]
        print(data)
        train_data.write(str(data)+'\n')
            
