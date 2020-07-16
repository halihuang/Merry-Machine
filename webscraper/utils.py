from bs4 import BeautifulSoup
import re
import aiohttp

def unpack_arrs(arr):
  new_arr = []
  for item in arr:
    new_arr.extend(item)
  return new_arr

def unpack_strs(arr, sep=""):
  new_str = ""
  for item in arr:
    new_str += clean_HTML(item) + sep
  return new_str

def getText(prop):
  if prop is not None:
    return prop.getText()
  return ""

async def soupify(url, session):
    async with session.get(url) as response:
      html = await response.text()
      soup = BeautifulSoup(html, 'html5lib')
      return soup

def remove_nulls(arr):
  return list(filter(lambda x: x != None, arr))

def clean_HTML(html):
  if html is not None:
    for script in html(["script", "style"]):  # remove all javascript and stylesheet code
      script.extract()
    # get text
    text = html.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = re.sub("\\n[^\\n]+", "", text)
    return text
  else:
    return ""

def is_valid_article(text):
  if text is not "" and text is not None:
    return True
  return False

class ClientSession:
    def __init__(self, limit=100):
      connector = aiohttp.TCPConnector(limit=limit)
      self.session = aiohttp.ClientSession(connector=connector)

    def get(self):
      return self.session

    async def close(self):
      await self.session.close()


def find_all_p(article, class_=""):
  if article is not None:
    if class_ is "":
      text = article.findAll('p')
    else:
      text = article.findAll('p', class_=class_)
    text = unpack_strs(text)
    return text
  return ""