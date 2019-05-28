import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import argparse
import sys

###############################################################################

def norm(x, train_stats):
    return (x - train_stats['mean']) / train_stats['std']

###############################################################################

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

###############################################################################

def build_seq_model(train_data, train_labels,
        totepochs, earlystop=False):

  model = keras.Sequential([
    layers.Dense(64, activation=tf.nn.relu, 
    input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation=tf.nn.relu),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mean_squared_error',
                optimizer=optimizer,
                metrics=['mean_absolute_error', 
                'mean_squared_error'])

  history = None 

  early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

  if earlystop:
      history = model.fit(train_data, train_labels, 
              epochs=totepochs,
              validation_split = 0.2, verbose=0, 
              callbacks=[early_stop, PrintDot()])
  else:
      history = model.fit(train_data, train_labels,
              epochs=totepochs, validation_split = 0.2, 
              verbose=0, callbacks=[PrintDot()])

  return model, history

###############################################################################

def plot_history(history, name = ""):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch
  
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error '+name)
  plt.plot(hist['epoch'], hist['mean_absolute_error'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
           label = 'Val Error')
  #plt.ylim([max(hist['val_mean_absolute_error'])])
  plt.legend()
  
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error [$'+name+'^2$]')
  plt.plot(hist['epoch'], hist['mean_squared_error'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_squared_error'],
           label = 'Val Error')
  #plt.ylim([max(hist['val_mean_squared_error'])])
  plt.legend()
  plt.show()


###############################################################################

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-f","--file", help="input csv file ", \
          required=True, type=str)
  parser.add_argument("-s","--showgraphs", help="shows graphs ", \
          required=False, default=False, action='store_true')
  parser.add_argument("-e","--epochs", help="use an excat number of epochs  ", \
          required=False, default=-1, type=int)
  
  if len(sys.argv) == 1:
      parser.print_help()
      exit(1)
  
  args = parser.parse_args()
  
  filename = args.file
  
  features = pd.read_excel(filename)
  print('The shape of our features is:', features.shape)
  print ("Header: ")
  i = 0
  for name in features.head(1):
      print("%5d "%(i) + name)
      i = i + 1
  
  # Remove non numeric data 
  features = features.drop("Name", axis = 1)
  features = features.drop("P", axis = 1)
  
  # remove all non needed 
  # features = features.drop("GM2-", axis = 1)
  # features = features.drop("ep1", axis = 1)
  # features = features.drop("ep2", axis = 1)
  features = features.drop("GM5+", axis = 1)
  features = features.drop("M2-", axis = 1)
  features = features.drop("DV/V(% AFE-FE)", axis = 1)
  features = features.drop("DeltaE", axis = 1)
  features = features.drop("Delta", axis = 1)
  features = features.drop("eta1", axis = 1)
  features = features.drop("eta2", axis = 1)
  features = features.drop("eta3", axis = 1)
  features = features.drop("DV/V(% FE-PA)", axis = 1)
  features = features.drop("ground_state", axis = 1)
  features = features.drop("DV/V(% AFE-PA)", axis = 1)

  # replace class
  #features = features.drop("Class", axis = 1)
  
  classset = set()
  for c in features["Class"]:
      classset.add(c)

  classmap = {}
  num = 0
  for c in classset:
      num = num + 1
      classmap[c] = num
     
  features["Class"].replace(classmap, inplace=True)

  train_dataset = features.sample(frac=0.8,random_state=0)
  test_dataset = features.drop(train_dataset.index)
  
  train_stats = train_dataset.describe()
  train_stats = train_stats.transpose()
  print(train_stats)
  
  topredict = "DE_sw"
  desc1 = "GM2-"
  desc2 = "ep1"
  desc3 = "ep2"
  desc4 = "Class"
  fulllist = [desc1, desc2, desc3, desc4, topredict]
  
  if args.showgraphs:
      sns.pairplot(train_dataset[fulllist], 
              diag_kind="kde")
      plt.show()
  
  test_stats = test_dataset.describe()
  test_stats = test_stats.transpose()
  print(test_stats)
  
  if args.showgraphs:
      sns.pairplot(test_dataset[fulllist], 
              diag_kind="kde")
      plt.show()
  
  train_labels = train_dataset.pop(topredict)
  test_labels = test_dataset.pop(topredict)
  
  train_stats = train_dataset.describe()
  train_stats = train_stats.transpose()
  
  normed_train_data = norm(train_dataset, train_stats)
  normed_test_data = norm(test_dataset, train_stats)
  
  #print(normed_train_data)
  #print(test_dataset)
  
  EPOCHS = 1000
  
  model, history = build_seq_model (normed_train_data, 
          train_labels, args.epochs, (args.epochs <= 0))
  
  print (model.summary())
  
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch
  print(hist.tail())
  
  if args.showgraphs:
      plot_history(history, topredict)
  
  loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
  print("Testing set Mean Abs Error: %5.2f %s"%(mae, topredict))
  
  test_predictions = model.predict(normed_test_data).flatten()
  
  plt.scatter(test_labels, test_predictions)
  plt.xlabel('True Values ['+topredict+']')
  plt.ylabel('Predictions ['+topredict+']')
  plt.axis('equal')
  plt.axis('square')
  plt.xlim([0,plt.xlim()[1]])
  plt.ylim([0,plt.ylim()[1]])
  _ = plt.plot([-100, 100], [-100, 100])
  
  plt.savefig('truevspredicted.png')
  
  error = test_predictions - test_labels
  
  plt.clf()
  plt.cla()
  plt.hist(error, bins = 25)
  plt.xlabel("Prediction Error ["+topredict+"]")
  _ = plt.ylabel("Count")
  
  plt.savefig('predictionerror.png')
