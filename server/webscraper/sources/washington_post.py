import asyncio
from webscraper.utils import *

# session = ClientSession(40)
# session = session.get()
links = []

async def get_all_articles():
    sections = [
     'national/investigations', 'consumer-tech', 'news/innovations', 'internet-culture', 'space', 'tech-policy', 'technology/video-gaming', 'world/africa', 'world/americas', 'world/asia-pacific', 'world/middle-east', 'world/europe/', 'local/public-safety', 'education', 'local/obituaries', 'transportation', 'local/weather/', 'sports', 'entertainment/books/', 'goingoutguide/movies', 'goingoutguide/music', 'goingoutguide/museums', 'goingoutguide/theater-dance', 'entertainment/tv', 'pop-culture', 'economic-policy', 'economy', 'energy', 'health-care', 'business/on-leadership', 'markets', 'personal-finance', 'business/on-small-business', 'climate-environment', 'climate-solutions', 'food', 'health', 'history', 'immigration', 'media', 'news/inspired-life', 'foreign-policy', 'justice', 'military', 'religion', 'science']
    await asyncio.gather(*map(get_article_links, sections))
    print('obtained links')
    articles = await asyncio.gather(*map(get_article, links))
    articles = remove_nulls(articles)
    await session.close()
    return articles


async def get_article_links(section):
    base_url = 'https://www.washingtonpost.com/'
    url = base_url + section
    soup = await soupify(url, session)
    articles = (soup.findAll)(*('a', ), **{'data-pb-local-content-field': 'web_headline'})
    if len(articles) == 0:
        articles = (soup.findAll)(*('a', ), **{'data-pb-field': 'headlines.basic'})
    for link in articles:
        article_link = link['href']
        if base_url not in article_link:
            article_link = base_url + article_link
        if article_link not in links and 'video.html' not in article_link and 'graphic.html' not in article_link and 'livediscussion.html' not in article_link:
            links.append(article_link)


async def get_article(link):
    try:
      article_soup = await soupify(link, session)
      text = article_soup.find('div', class_='article-body')
      text = find_all_p(text)
      if text is '':
        text = article_soup.find('article')
        text = clean_HTML(text)
      if text is '':
          text = article_soup.find('div', class_='main')
          text = find_all_p(text)
          if text is '':
            title = article_soup.find('h1', class_='pg-h1')
            title = getText(title)
            authors = article_soup.findAll('span', class_="pg-byline--author")
            authors = unpack_strs(authors)
            text = article_soup.findAll('p', class_="pg-body-copy")
            text = unpack_strs(text)
            date = article_soup.find('div', itemprop='datePublished')
            date = getText(date)
          else:
            title = article_soup.find('h1', class_='title')
            title = getText(title)
            authors = article_soup.findAll('span', itemprop='author')
            authors = unpack_strs(authors)
            date = article_soup.find('div', class_='date')
            date = getText(date)
      else:
          title = (article_soup.find)(*('h1', ), **{'data-qa': 'headline'})
          title = getText(title)
          if title == '':
              title = article_soup.find('h1', itemprop='headline')
              title = getText(title)
              date = article_soup.find('div', itemprop='datePublished')
              date = getText(date)
          else:
              date = article_soup.find('div', class_='display-date')
              date = getText(date)
          authors = article_soup.findAll(class_='author-name')
          authors = unpack_strs(authors, ', ')
      meta = 'By ' + authors + ' ' + date
      if is_valid_article(text):
          if meta == 'By  ':
              print(link)
          article = dict(url=link, title=title, summary='', meta=meta, text=text)
          return article
      else:
        print('failed to find content in:' + link)
    except asyncio.TimeoutError:
        print('failed to get:' + link)