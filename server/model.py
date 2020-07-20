import tensorflow_datasets as tfds
import numpy as np
import json
import gc

def encode_text():
  gc.collect()
  print('encoding text')
  encoder = tfds.features.text.SubwordTextEncoder.load_from_file('encoder')
  with open("example.json") as articles_file:
    articles = json.load(articles_file)
    for source in articles:
      x = 0
      encoded_arr = np.zeros((len(source['articles']), 2**11), dtype=np.float32)
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
          if (y < 2**11):
            encoded_arr[x][y] = element
          y += 1
        x += 1
      source['encoded'] = encoded_arr.tolist()
      
    print('encoded text')
    with open('encoded.json', 'w') as file:
      json.dump(articles, file)
      gc.collect()
      print('written')


# def predict_pol_labels():
#   gc.collect()
#   political_model = tf.keras.models.load_model('saved_models/political_model')
#   print('got political')
#   with open('encoded.json') as file:
#     encoded_sources = json.load(file)
#     print('making predicitions')
#     with open('predictions.json') as readfile:
#         predictions = json.load(readfile)
#     source_index = 0
#     for source in encoded_sources:
#       pol_predictions = political_model.predict(np.asarray(source['encoded']))

#       i = 0
#       for article in source['articles']:
#         if (pol_predictions[i] > -1.1) and source['source'] != "NY Times":
#           predictions[source_index]['political'].append(article)
#         i+=1
#       source_index += 1

#   with open('predictions.json', 'w') as outfile:
#     json.dump(predictions, outfile)

#   gc.collect()
#   print('made predicitions')

# def predict_neg_labels():
#   gc.collect()
#   negative_model = tf.keras.models.load_model('saved_models/negative_model')
#   print('got negative')
#   with open('encoded.json') as file:
#     encoded_sources = json.load(file)
#     print('making predicitions')
#     with open('predictions.json') as readfile:
#         predictions = json.load(readfile)
#     source_index = 0
#     for source in encoded_sources:
#       neg_predictions = negative_model.predict(np.asarray(source['encoded']))

#       i = 0
#       for article in source['articles']:
#         if (neg_predictions[i] > -0.825) and source['source'] != "NY Times":
#           predictions[source_index]['negative'].append(article)
#         i+=1
#       source_index += 1

#   with open('predictions.json', 'w') as outfile:
#     json.dump(predictions, outfile)

#   gc.collect()
#   print('made predicitions')


# def predict_pos_labels():
#   gc.collect()
#   positive_model = tf.keras.models.load_model('saved_models/positive_model')
#   print('got positive')
#   with open('encoded.json') as file:
#     encoded_sources = json.load(file)
#     print('making predicitions')
#     with open('predictions.json') as readfile:
#         predictions = json.load(readfile)
#     source_index = 0
#     for source in encoded_sources:
#       pos_predictions = positive_model.predict(np.asarray(source['encoded']))

#       i = 0
#       for article in source['articles']:
#         if (pos_predictions[i] > -1):
#           predictions[source_index]['positive'].append(article)
#         i+=1
#       source_index += 1

#   with open('predictions.json', 'w') as outfile:
#     json.dump(predictions, outfile)

#   gc.collect()
#   print('made predicitions')


# def predict_labels():
#   print('getting models')
#   positive_model = tf.keras.models.load_model('saved_models/positive_model')
#   print('got positive')
#   negative_model = tf.keras.models.load_model('saved_models/negative_model')
#   print('got negative')
#   political_model = tf.keras.models.load_model('saved_models/political_model')
#   print('got political')
#   print('got models')
#   print('getting data')
#   # articles = get_scraped()

#   num_pos, num_neg, num_pol, num_tot = 0, 0, 0, 0
#   with open('example.json') as file:
#     articles = json.load(file)
#     encoded_sources = encode_text(articles)

#     print('making predicitions')

#     predictions_json = []
#     for source in encoded_sources:
#       pos_predictions = positive_model.predict(source['encoded'])
#       neg_predictions = negative_model.predict(source['encoded'])
#       pol_predictions = political_model.predict(source['encoded'])
#       predictions = dict(source=source['source'], positive=[], negative=[], political=[])

#       i = 0
#       for article in source['articles']:
#         if pos_predictions[i] > -1:
#           predictions['positive'].append(article)
#           num_pos+=1
#         i+=1
#         num_tot+=1

#       i = 0
#       for article in source['articles']:
#         if (neg_predictions[i] > -0.825) and source['source'] != "NY Times":
#           predictions['negative'].append(article)
#           num_neg+=1
#         i+=1

#       i = 0
#       for article in source['articles']:
#         if (pol_predictions[i] > -1.1 and source['source'] != "NY Times"):
#           predictions['political'].append(article)
#           num_pol+=1
#         i+=1

#       predictions_json.append(predictions)

#   with open('predictions.json', 'w') as outfile:
#     json.dump(predictions_json, outfile)

#   print('made predicitions')
#   print('Pos: ' + str(num_pos) + '\nNeg: ' + str(num_neg) + '\nPol: ' + str(num_pol) + '\nTot: ' + str(num_tot))


if __name__ == '__main__':
  encode_text()