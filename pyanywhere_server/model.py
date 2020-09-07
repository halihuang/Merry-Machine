import tensorflow as tf
import numpy as np
import json
import gc
from multiprocessing import Process
from multiprocessing import Queue

tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

def predict_pol_labels(encoded_sources):
  with tf.device('/CPU:0'):
    gc.collect()
    political_model = tf.keras.models.load_model('saved_models/political_model')
    print('got political')
    print('making predictions')
    with open('predictions.json') as readfile:
        predictions = json.load(readfile)
    source_index = 0
    for source in encoded_sources:
      predictions[source_index]['political'] = []
      pol_predictions = political_model.predict(np.asarray(source['encoded']))

      i = 0
      for article in source['articles']:
        if (pol_predictions[i] > -1.1) and source['source'] != "NY Times":
          predictions[source_index]['political'].append(article)
        i+=1
      source_index += 1
    with open('predictions.json', 'w') as outfile:
      json.dump(predictions, outfile)

    print('made predictions')
    return predictions


def predict_neg_labels(encoded_sources):
  with tf.device('/CPU:0'):
    gc.collect()
    negative_model = tf.keras.models.load_model('saved_models/negative_model')
    print('got negative')
    print('making predictions')
    print('making predictions')
    with open('predictions.json') as readfile:
        predictions = json.load(readfile)

    source_index = 0
    for source in encoded_sources:
      predictions[source_index]['negative'] = []
      neg_predictions = negative_model.predict(np.asarray(source['encoded']))

      i = 0
      for article in source['articles']:
        if (neg_predictions[i] > -0.825) and source['source'] != "NY Times":
          predictions[source_index]['negative'].append(article)
        i+=1
      source_index += 1

    with open('predictions.json', 'w') as outfile:
      json.dump(predictions, outfile)

    print('made predictions')
    return predictions


def predict_pos_labels(encoded_sources):
  with tf.device('/CPU:0'):
    gc.collect()
    positive_model = tf.keras.models.load_model('saved_models/positive_model')
    print('got positive')
    print('making predictions')
    with open('predictions.json') as readfile:
        predictions = json.load(readfile)
    source_index = 0
    for source in encoded_sources:
      predictions[source_index]['positive'] = []
      pos_predictions = positive_model.predict(np.asarray(source['encoded']))

      i = 0
      for article in source['articles']:
        if (pos_predictions[i] > -1):
          predictions[source_index]['positive'].append(article)
        i+=1
      source_index += 1

    with open('predictions.json', 'w') as outfile:
      json.dump(predictions, outfile)

    print('made predictions')
    return predictions

def run_process(func, args):

  def wrapper_func(queue, args):
    try:
      result = func(args)
    except Exception:
      result = None
    queue.put(result)

  def process(args):
    queue = Queue()
    p = Process(target=wrapper_func, args=(queue, args))
    p.start()
    data = queue.get()
    p.join()
    return data

  result = process(args)
  return result

if __name__ == '__main__':
  predict_pos_labels()