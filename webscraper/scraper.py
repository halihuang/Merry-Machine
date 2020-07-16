import asyncio
import json
import time
from source_list import my_sources

def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(scrape_articles())
    with open('training_server/example.json', 'w') as file:
        json.dump(result, file)

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


def test():
    with open('articles.json') as file:
        obj = json.load(file)
        print(obj)
        print('success')

if __name__ == "__main__":
    main()