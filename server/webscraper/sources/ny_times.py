
import asyncio
from webscraper.utils import *

session = ClientSession()
session = session.get()
links = []


async def get_all_articles():
    sections = ['world', 'us', 'nyregion', 'buisness', 'technology', 'opinion', 'science', 'health', 'sports', 'arts', 'books', 'style', 'food', 'travel', 't-magazine']
    await asyncio.gather(*map(get_article_links, sections))
    print('obtained links')
    articles = await asyncio.gather(*map(get_article, links))
    articles = remove_nulls(articles)
    await session.close()
    return articles

async def get_article_links(section):
    url = 'https://www.nytimes.com/section/' + section
    soup = await soupify(url, session)
    articles = soup.findAll('h2')
    for link in articles:
        if link.a is not None and link.a.has_attr("href"):
            article_link = 'https://www.nytimes.com' + link.a['href']
            if article_link not in links:
              links.append(article_link)


async def get_article(link):
  try:
    article_soup = await soupify(link, session)
    title = article_soup.find('h1', itemprop='headline')
    title = getText(title)
    text = article_soup.find('section', itemprop='articleBody')
    text = clean_HTML(text)
    meta = []
    if text == "" and title != "":
        summary = article_soup.find('div', class_='g-cliff-summary')
        summary = getText(summary)
        try:
            text = article_soup.find('div', class_='rad-story-body')
            text = text.findAll('p', class_='paragraph')
            text = unpack_strs(text)
            article_meta = article_soup.find('div', class_='g-cliff-meta')
            article_meta = article_meta.findAll('span')
            for info in article_meta:
                meta.append(getText(info))
        except AttributeError:
            failed = []
            failed.append(link)
            for failure in failed:
                print('failed to load:' + failure)

    else:
        summary = article_soup.find('p', id='article-summary')
        summary = getText(summary)
        authors = article_soup.find('p', itemprop='author')
        authors = getText(authors)
        meta.append(authors)
        date = article_soup.find('time')
        date = getText(date)
        meta.append(date)
        
    if is_valid_article(text):
        article = dict(url=link, title=title, summary=summary, meta=meta, text=text)
        return article
  except:
        print('failed to get:' + link)