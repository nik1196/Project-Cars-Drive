import tensorflow as tf, matplotlib.pyplot as plt, carseour, joystick, pyvjoy
import numpy as np
from pyautogui import press

#tf.enable_eager_execution()
game = carseour.live()
player = game.mParticipantInfo[0]

def sigmoid(x,a=1, b=1):
    return (a*np.exp(x)/(1+b*np.exp(x)))
def positive_sigmoid(x, a=1, b=1):
    if x >= 0:
        return 1/(1+np.exp(b*x))
    else:
        return 0.01 * np.abs(x)
op = []
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(6,)),
    tf.keras.layers.Dense(10, activation = tf.nn.relu),
    tf.keras.layers.Dense(2)
    ])

track_exit_detected = False
recovery_direction = 0

def score(ip,y_):
    global op, track_exit_detected, recovery_direction
    x = tf.Session().run(ip)
    terrain_score = np.zeros(4)
    recovery_completed = 0
    for i in range(2,6):
        if (x[0][i] != carseour.definitions.TERRAIN_ROAD):
            if not track_exit_detected:
                recovery_direction = np.power(-1,(i-2)%2)
                track_exit_detected = True
        elif track_exit_detected:
            recovery_completed += 1
    if(recovery_completed == 4):
        track_exit_detected = False
        recovery_direction = 0
        recovery_completed = 0
    ret = np.zeros(2)
    ret[0] = (positive_sigmoid(x[0][0],b=-0.2) * recovery_direction)/(recovery_completed+1);
    if x[0][0] <= 0 or x[0][1] < 0:
        ret[1] = 1
    elif track_exit_detected:
        ret[1] = 0
    else:
        ret[1] = sigmoid(x[0][0])*(1/x[0][1])
    op = ret
    tfret = np.array(ret, ndmin=2)
    return tf.losses.mean_squared_error(y_, tfret)

def loss(model, x):
    y_ = model(x)
    return score(x,y_)



def grad(model, inputs):
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs)
    return loss_value, tape.gradient(loss_value, model.trainable_variables)

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
global_step = tf.Variable(0)

num_epochs = 3

epoch = 0
snap = carseour.snapshot()
prev_lap_dist = snap.mParticipantInfo[0].mCurrentLapDistance
prev_speed = snap.mSpeed
reset = False
time_after_reset = 0
while  game.mParticipantInfo[0].mLapsCompleted < num_epochs:
    joystick.stick.set_button(1,0)
    snap2 = carseour.snapshot()
    cur_lap_dist = snap2.mParticipantInfo[0].mCurrentLapDistance
    cur_speed = snap2.mSpeed
    if reset:
        time_after_reset += 1
    if time_after_reset > 20:
        reset = False
        time_after_reset = 0
    if(cur_speed < 1 and not reset):
        joystick.stick.set_axis(pyvjoy.HID_USAGE_X, int(joystick.JOY_AXIS_CTR))
        joystick.stick.set_axis(pyvjoy.HID_USAGE_Z, int(joystick.JOY_AXIS_CTR))
        joystick.stick.set_button(1,1)
        track_exit_detected = False
        recovery_direction = 0
        print(reset)
        reset = True
        continue
    lap_dist_delta = cur_lap_dist - prev_lap_dist
    speed_delta = cur_speed - prev_speed
    prev_lap_dist = cur_lap_dist
    prev_speed = cur_speed
    ip = np.array([lap_dist_delta, speed_delta, game.mTerrain[0], game.mTerrain[1], game.mTerrain[2], game.mTerrain[3]], ndmin=2)
    x = tf.convert_to_tensor(ip)
    loss_value, grads = grad(model, x)
    optimizer.apply_gradients(zip(grads, model.trainable_variables),
                              global_step)
    joystick.stick.set_axis(pyvjoy.HID_USAGE_X, int(op[0] * joystick.JOY_AXIS_CTR + joystick.JOY_AXIS_CTR))
    joystick.stick.set_axis(pyvjoy.HID_USAGE_Z, int(op[1] * joystick.JOY_AXIS_CTR + joystick.JOY_AXIS_CTR))
    epoch += 1
