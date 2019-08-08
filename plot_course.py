import numpy as np, matplotlib.pyplot as plt, re,sys
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf, datetime
data = []

def normalize(x):
    mx = np.max(x)
    mn = np.min(x)
    for i in range(len(x)):
        if x[i] > 0:
            x[i] /= mx
        else:
            x[i] /= np.abs(mn)
    return x
    

with open('train_data.txt') as in_file:
    for line in in_file:
        res = re.findall('(-{0,1}\d+\.\d+)', line)
        inputs = [np.float32(res[i]) for i in range(4)]
        outputs = [np.float32(res[i]) for i in range(4,6)]
        data.append([inputs, outputs])

ips = np.array([data[i][0] for i in range(len(data))])

ops = np.array([data[i][1] for i in range(len(data))])

coords = np.array([ips[i][2:] for i in range(len(ips))])
lap_dist = np.array([ips[i][1] for i in range(len(ips))])
lap_dist = np.divide(lap_dist,np.max(lap_dist))
#lap_dist = np.divide(lap_dist,2)
lap_dist = np.subtract(lap_dist,0.5)
x = np.array([coords[i][0] for i in range(len(coords))])
print(np.max(x))
print(np.min(x))
x = np.divide(x, np.abs(np.max(x) - np.min(x)))
x = normalize(x)

y = np.array([coords[i][1] for i in range(len(coords))])
y = np.divide(y, np.abs(np.max(y) - np.min(y)))
y = normalize(y)

actual = np.transpose(np.array([x,y],ndmin=2))
print(np.shape(actual))

inputs = tf.keras.Input(shape=(1,))
layer1 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(inputs)
layer2 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer1)
layer3 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer2)
layer4 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer3)
layer5 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer4)
layer6 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer5)
layer7 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer6)
layer8 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer7)
layer9 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer8)
layer10 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer9)
layer11 = tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer10)
layer12= tf.keras.layers.Dense(16, activation=tf.keras.activations.tanh)(layer11)
layer13 = tf.keras.layers.Dense(4, activation=tf.keras.activations.tanh)(layer12)
output = tf.keras.layers.Dense(2)(layer8)
model = tf.keras.Model(inputs=inputs, outputs = output)

optimizer = tf.keras.optimizers.RMSprop(1e-3)

model.compile(loss=tf.keras.losses.mean_squared_error.__name__, optimizer = optimizer)



epochs = 4000

class PrintDot(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        print(epoch+1)

class PrintWt(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        print(layer1.get_weights())

##def scheduler(epoch):
##    if epoch < 3:
##        return 0.1
##    else:
##        return 0.1 * 0.1 * (1+(epoch-3)/10)

##,tf.keras.callbacks.LearningRateScheduler(scheduler)
history = model.fit(lap_dist,actual ,batch_size=len(ips),epochs=epochs, verbose=0)

fig = plt.figure()
x1 = [i for i in range(1,epochs+1)]
y1 = history.history['loss']
surf1 = fig.add_subplot(221)
surf1.plot(x1, y1)

##model = tf.keras.models.load_model('new_models/model2')
x2 = [ele[0] for ele in coords]
z2 = [ele[1] for ele in coords]
i = 0
print(len(lap_dist))
op = model.predict(lap_dist)
print(np.shape(op))
predicted_x = [ele[0] for ele in op]
predicted_z = [ele[1] for ele in op]


surf =fig.add_subplot(222,projection='3d')
##surf.set_xlabel('lap_dist')
##surf.set_ylabel('Y')
##surf.set_zlabel('Z')
surf2 =fig.add_subplot(223,projection='3d')
##surf2.set_xlabel('lap_dist')
##surf2.set_ylabel('Y')
##surf2.set_zlabel('Z')
surf2.plot3D(lap_dist,predicted_x,predicted_z, 'r')
surf.plot(lap_dist,x,y, 'b')


tf.keras.models.save_model(model, 'new_models/model2',save_format='h5')

plt.show()
