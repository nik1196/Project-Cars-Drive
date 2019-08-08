import tensorflow as tf, numpy as np, matplotlib.pyplot as plt, re, sys
import carseour, pyvjoy, joystick

from tensorflow.python.client import device_lib

def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']

def get_available_cpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'CPU']
with tf.device('/cpu:0'):
    model = tf.keras.models.load_model('new_models/model1')

    joystick.stick.set_axis(pyvjoy.HID_USAGE_X, int(joystick.JOY_AXIS_CTR))
    joystick.stick.set_axis(pyvjoy.HID_USAGE_Y, int(joystick.JOY_AXIS_CTR))
    game = carseour.live()
    player = game.mParticipantInfo[0]

    print(get_available_gpus())
    print(get_available_cpus())


    while True:
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
        ip = np.array(data[0],ndmin=2)
        pred = model.predict(ip)
        joystick.stick.set_axis(pyvjoy.HID_USAGE_X, int(pred[0][0] * joystick.JOY_AXIS_CTR + joystick.JOY_AXIS_CTR))
        joystick.stick.set_axis(pyvjoy.HID_USAGE_Y, int(pred[0][1] * joystick.JOY_AXIS_CTR + joystick.JOY_AXIS_CTR))
        
