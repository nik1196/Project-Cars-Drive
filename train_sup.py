import tensorflow as tf, numpy as np, matplotlib.pyplot as plt, re,sys

data = []
with open('train_data.txt') as in_file:
    for line in in_file:
        res = re.findall('(-{0,1}\d+\.\d+)', line)
        inputs = [np.float32(res[i]) for i in range(4)]
        outputs = [np.float32(res[i]) for i in range(4,6)]
        data.append([inputs, outputs])
#data = np.array(data)
print(data[0])

ips = []
ops = []

ips = np.array([data[i][0] for i in range(len(data))])
ops = np.array([data[i][1] for i in range(len(data))])
print(np.shape(ips))
print(ips[:10])
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation=tf.nn.sigmoid, input_shape=(4,)),
    tf.keras.layers.Dense(10, activation = tf.nn.sigmoid),
    tf.keras.layers.Dense(2)
    ])

optimizer = tf.keras.optimizers.SGD(0.001)

model.compile(loss='mean_squared_error', optimizer = optimizer, metrics=['mean_absolute_error', 'mean_squared_error'])



epochs = 2000

class PrintDot(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        print(epoch+1)

def scheduler(epoch):
    if epoch < 1014:
        return 0.001
    else:
        return 0.001 * tf.math.exp(0.1*(1014-epoch))

history = model.fit(ips, ops, epochs=epochs, validation_split = 0.2, verbose=0, callbacks=[PrintDot(),tf.keras.callbacks.LearningRateScheduler(scheduler)])

plt.figure()
x = [i for i in range(1,epochs+1)]
y = history.history['val_loss']
plt.plot(x, y)
plt.show()

tf.keras.models.save_model(model, 'new_models/model1',save_format='h5')
