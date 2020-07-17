from webscraper.sources import ny_times
from webscraper.sources import abc_news
from webscraper.sources import washington_post

class SourceList:

    ny_times_source = dict(source="NY Times",
                           module=ny_times)
    abc_news_source = dict(source="ABC News",
                           module=abc_news)
    washington_post_source = dict(source="Washington Post",
                           module=washington_post)                      
    sources = [ny_times_source, abc_news_source, washington_post_source]

my_sources = SourceList()