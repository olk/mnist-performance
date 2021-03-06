import keras
import time

from keras import backend as K
from keras.datasets import mnist
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.losses import categorical_crossentropy
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import to_categorical

BATCH_SIZE_PER_REPLICA = 512
BATCH_SIZE = BATCH_SIZE_PER_REPLICA * 1
NUM_CLASSES = 10
EPOCHS = 10
# input image dimensions
IMG_ROWS, IMG_COLS = 28, 28
N = 5

print('backend: ' + K.backend())

# the data, split between train and test sets
(train_x, train_y), (test_x, test_y) = mnist.load_data()
train_x, test_x = train_x.astype('float32')/255., test_x.astype('float32')/255.

train_x = train_x.reshape(train_x.shape[0], 1, IMG_ROWS, IMG_COLS)
test_x = test_x.reshape(test_x.shape[0], 1, IMG_ROWS, IMG_COLS)
input_shape = (1, IMG_ROWS, IMG_COLS)

print(train_x.shape)
print(train_x.shape[0])
print(test_x.shape)
print(test_x.shape[0])

# convert class vectors to binary class matrices
train_y = to_categorical(train_y, NUM_CLASSES)
test_y = to_categorical(test_y, NUM_CLASSES)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(NUM_CLASSES, activation='softmax'))

model.compile(loss=categorical_crossentropy,
              optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-8),
              metrics=['accuracy'])

total_elapsed = 0
for i in range(N):
    start = time.perf_counter()
    model.fit(train_x, train_y,
              batch_size=BATCH_SIZE,
              epochs=EPOCHS,
              verbose=1)
    elapsed = time.perf_counter() - start
    total_elapsed += elapsed
    print('elapsed: {:0.3f}'.format(elapsed))
print('elapsed at average: {:0.3f}'.format(total_elapsed/N))

score = model.evaluate(test_x, test_y, verbose=0)
print('validation accuracy=', score[1])
