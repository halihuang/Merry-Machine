import tensorflow_datasets as tfds
import tensorflow as tf
import numpy as np
from webscraper.scraper import get_scraped
import json

imdb_dataset, imdb_info = tfds.load('imdb_reviews/subwords8k', with_info=True,
                          as_supervised=True)
encoder = imdb_info.features['text'].encoder

def encode_text(articles):
  for source in articles:
    x = 0
    encoded_arr = np.zeros((len(source['articles']), 2**14), dtype=np.float32)
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
        encoded_arr[x][y] = element
        y += 1
      x += 1
    source['encoded'] = encoded_arr
  return articles

def predict_labels():
  positive_model = tf.keras.models.load_model('saved_models/positive_model')
  negative_model = tf.keras.models.load_model('saved_models/negative_model')
  political_model = tf.keras.models.load_model('saved_models/political_model')
  # articles = get_scraped()
  with open('example.json') as file:
    articles = json.load(file)
    encoded_sources = encode_text(articles)
    for source in encoded_sources:
      pos_predictions = positive_model.predict(source['encoded'])
      neg_predictions = negative_model.predict(source['encoded'])
      pol_predictions = political_model.predict(source['encoded'])

      print(pos_predictions)
      print(neg_predictions)
      print(pol_predictions)

def test():
  predict_labels()

if __name__ == '__main__':
  test()