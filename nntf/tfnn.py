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
      
        if epoch % 100 == 0: 
            print('')
      
        print('.', end='')

###############################################################################

def use_seq_model(train_data, train_labels, test_data, test_labels,
        totepochs, topredict, earlystop=False, dumpgraphs=False):

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

  #print (model.summary())
  
  #hist = pd.DataFrame(history.history)
  #hist['epoch'] = history.epoch
  #print(hist.tail())
  
  if dumpgraphs:
      plot_history(history, topredict)
  
  loss, mae, mse = model.evaluate(test_data, test_labels, verbose=0)
 
  test_predictions = model.predict(test_data).flatten()

  return mae, test_predictions

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
  plt.savefig('histoty.png')


###############################################################################

def replace_by_number (features, name):

  gsset = set()
  for c in features[name]:
      gsset.add(c)

  gsmap = {}
  num = 0
  for c in gsset:
      num = num + 1
      gsmap[c] = num
     
  features[name].replace(gsmap, inplace=True)

###############################################################################

def drop_all_but (features, alllist):
    for name in features.head(1):
        if not (name in alllist):
            print (name)
            features = features.drop(name, axis=1)


    return features

###############################################################################

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-f","--file", help="input csv file ", \
          required=True, type=str)
  parser.add_argument("-t","--topredict", help="input property to predict ", \
          required=True, type=str)
  parser.add_argument("-r","--descriptor", help="input descriptor to use \"name1;...\" ", \
          required=True, type=str)

 
  parser.add_argument("-d","--dumpgraphs", help="dump graphs ", \
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
  
  # replace class
  replace_by_number (features, "Class")

  # replace ground_state
  replace_by_number (features, "ground_state")

  fulllist = []

  if not (args.topredict in features.head(1)):
      print ("Error in topredict option")
      exit()

  fulllist.append(args.topredict)

  for desc in args.descriptor.split(";"):
       if not (desc in features.head(1)):
           print ("Error in descriptor")
           exit()

       fulllist.append(desc)

  features = drop_all_but (features, fulllist)

  print (features)

  train_dataset = features.sample(frac=0.8,random_state=0)
  test_dataset = features.drop(train_dataset.index)
  
  train_stats = train_dataset.describe()
  train_stats = train_stats.transpose()
  print(train_stats)
  
  if args.dumpgraphs:
      sns.pairplot(train_dataset[fulllist], 
              diag_kind="kde")
      plt.savefig('train_dataset.png')
  
  test_stats = test_dataset.describe()
  test_stats = test_stats.transpose()
  print(test_stats)
  
  if args.dumpgraphs:
      sns.pairplot(test_dataset[fulllist], 
              diag_kind="kde")
      plt.savefig('test_dataset.png')
  
  train_labels = train_dataset.pop(args.topredict)
  test_labels = test_dataset.pop(args.topredict)
  
  train_stats = train_dataset.describe()
  train_stats = train_stats.transpose()
  
  normed_train_data = norm(train_dataset, train_stats)
  normed_test_data = norm(test_dataset, train_stats)

  mae, test_predictions = \
          use_seq_model (normed_train_data, train_labels, normed_test_data, 
          test_labels, args.epochs, args.topredict, (args.epochs <= 0), 
          args.dumpgraphs)

  print("\nTesting set Mean Abs Error: %5.2f %s"%(mae, args.topredict))
  
  plt.clf()
  plt.cla()
  plt.scatter(test_labels, test_predictions)
  plt.xlabel('True Values ['+args.topredict+']')
  plt.ylabel('Predictions ['+args.topredict+']')
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
  plt.xlabel("Prediction Error ["+args.topredict+"]")
  _ = plt.ylabel("Count")
  
  plt.savefig('predictionerror.png')
