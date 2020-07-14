from sources import ny_times
from sources import abc_news

class SourceList:

    ny_times_source = dict(source="NY Times",
                           module=ny_times)
    abc_news_source = dict(source="ABC News",
                           module=abc_news)
    sources = [ny_times_source, abc_news_source]

my_sources = SourceList()