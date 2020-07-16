import asyncio
from utils import *

session = ClientSession(50)
session = session.get()
links = []


async def get_all_articles():
    sections = ['US', 'International', 'Health', 'Entertainment', 'Business', 'Technology', 'Lifestyle', 'Sports']
    await asyncio.gather(*map(get_article_links, sections))
    print('obtained links')
    articles = await asyncio.gather(*map(get_article, links))
    articles = remove_nulls(articles)
    await session.close()
    return articles

async def get_article_links(section):
    url = 'https://abcnews.go.com/' + section
    soup = await soupify(url, session)
    articles = soup.findAll('a', class_="AnchorLink")
    for link in articles:
        if url in link['href'] and (("/wireStory/" in link['href']) or ("/story?" in link['href'])):
            article_link = link['href']
            if not article_link in links:
                links.append(article_link)


async def get_article(link):
  try:
    article_soup = await soupify(link, session)
    title = article_soup.find('h1', class_='Article__Headline__Title')
    title = getText(title)
    summary = article_soup.find('p', class_="Article__Headline__Desc")
    summary = getText(summary)
    authors = article_soup.find('div', class_="Byline__Author")
    authors = getText(authors)
    date = article_soup.find('div', class_='Byline__Meta--publishDate')
    date = getText(date)
    text = article_soup.find('article', class_="Article__Content story")
    text = text.findAll('p')
    text = unpack_strs(text)
    if is_valid_article(text):
        article = dict(url=link, title=title, summary=summary, authors=authors, date=date, text=text)
        return article
  except:
        print('failed to get:' + link)