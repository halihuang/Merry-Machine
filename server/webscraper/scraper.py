import asyncio
import json
import time
import numpy as np
import tensorflow_datasets as tfds
import tensorflow
from webscraper.source_list import my_sources

imdb_dataset, imdb_info = tfds.load('imdb_reviews/subwords8k', with_info=True,
                          as_supervised=True)
encoder = imdb_info.features['text'].encoder

def create_training_json():
    result = get_scraped()
    with open('server/example.json', 'w') as file:
        json.dump(result, file)

def create_official_json():
  with open('articles.json', 'w') as file:
    parsed = json.load(file)
    print(encode_text(parsed))

def get_scraped():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(scrape_articles())
    return result

async def scrape_articles():
    all_news = []
    for source in my_sources.sources:
        start = time.perf_counter()
        print('start getting ' + source['source'] + ' articles')
        articles = await source['module'].get_all_articles()
        news = dict(source=source['source'],
                    articles=articles)
        all_news.append(news)
        end = time.perf_counter()
        print(source['source'] + " Articles obtained in: " + str(end - start) + "seconds")
    return all_news

def encode_text(articles):
  encoded = []
  for source in articles:
    x = 0
    encoded_arr = np.zeros(len(source['articles']), 2**12, dtype=np.float32)
    for article in source['articles']:
      y = 0
      x += 1
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
    print(encoded_arr)
    encoded.append(encoded_arr)
  return encoded

def test():
    with open('articles.json') as file:
        obj = json.load(file)
        print(obj)
        print('success')

if __name__ == "__main__":
    create_official_json()