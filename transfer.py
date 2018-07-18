from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed
from RNN_utils import *

BATCH_SIZE = 10
HIDDEN_DIM = 50
SEQ_LENGTH = 10
WEIGHTS = 'ckpt_1740.hdf5'
GENERATE_LENGTH = 140
LAYER_NUM = 2
MAX_ITERS = 2 # CAUTION ALWAYS SET >=2 (len-2 tweet is used in js)


def train(data):
  '''
    Specify weights and train further with fetched tweets corpus
  '''
  if len(data) < 3 * SEQ_LENGTH:
    return '-1'

  # Creating training data
  X, y, VOCAB_SIZE, ix_to_char = load_data(data, SEQ_LENGTH)

  # Creating and compiling the Network
  model = Sequential()
  model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
  for i in range(LAYER_NUM - 1):
    model.add(LSTM(HIDDEN_DIM, return_sequences=True))
  model.add(TimeDistributed(Dense(VOCAB_SIZE)))
  model.add(Activation('softmax'))
  model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

  model.load_weights(WEIGHTS)
  epochs = 1740

  generated_tweets = []
  iterations = MAX_ITERS
  while iterations > 0:
    # print('\n\nEpoch: {}\n'.format(epochs))
    model.fit(X, y, batch_size=BATCH_SIZE, verbose=1, epochs=1)
    epochs += 1
    tweet = generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
    generated_tweets.append(tweet)
    iterations -= 1
  return generated_tweets
