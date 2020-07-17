import tensorflow_datasets as tfds
import tensorflow as tf
import numpy as np
from webscraper.scraper import get_scraped
import json

imdb_dataset, imdb_info = tfds.load('imdb_reviews/subwords8k', with_info=True,
                          as_supervised=True)
encoder = imdb_info.features['text'].encoder

def encode_text(articles):
  print('encoding text')
  for source in articles:
    x = 0
    encoded_arr = np.zeros((len(source['articles']), 2**13), dtype=np.float32)
    for article in source['articles']:
      y = 0
      if (article['title'] != None):
        encoded_title = (encoder.encode(article['title']))
      else:
        encoded_title = (encoder.encode(' '))
      if (article['text'] != None):
        encoded_text = (encoder.encode(article['text']))
      else:
        encoded_text = (encoder.encode(' '))
      encoded_title.extend(encoded_text)
      for element in encoded_title:
        if (y < 2**13):
          encoded_arr[x][y] = element
        y += 1
      x += 1
    source['encoded'] = encoded_arr
    
  print('encoded text')
  return articles

def predict_labels():
  print('getting models')
  positive_model = tf.keras.models.load_model('saved_models/positive_model')
  print('got positive')
  negative_model = tf.keras.models.load_model('saved_models/negative_model')
  print('got negative')
  political_model = tf.keras.models.load_model('saved_models/political_model')
  print('got political')
  print('got models')
  print('getting data')
  # articles = get_scraped()

  num_pos, num_neg, num_pol, num_tot = 0, 0, 0, 0
  with open('example.json') as file:
    articles = json.load(file)
    encoded_sources = encode_text(articles)

    print('making predicitions')

    predictions_json = []
    for source in encoded_sources:
      pos_predictions = positive_model.predict(source['encoded'])
      neg_predictions = negative_model.predict(source['encoded'])
      pol_predictions = political_model.predict(source['encoded'])
      predictions = dict(source=source['source'], positive=[], negative=[], political=[])

      i = 0
      for article in source['articles']:
        if pos_predictions[i] > -1.15:
          predictions['positive'].append(article)
          num_pos+=1
        i+=1
        num_tot+=1

      i = 0
      for article in source['articles']:
        if (neg_predictions[i] > -1.1):
          predictions['negative'].append(article)
          num_neg+=1
        i+=1

      i = 0
      for article in source['articles']:
        if (pol_predictions[i] > -1.1):
          predictions['political'].append(article)
          num_pol+=1
        i+=1

      predictions_json.append(predictions)

    with open('predictions.json', 'w') as outfile:
      json.dump(predictions_json, outfile)

    print('made predicitions')
    print('Pos: ' + str(num_pos) + '\nNeg: ' + str(num_neg) + '\nTot: ' + str(num_tot))


if __name__ == '__main__':
  predict_labels()