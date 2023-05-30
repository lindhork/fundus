from fundus.scraping.source import RSSFeed
from fundus.publishers.base_objects import PublisherEnum, PublisherSpec

from .orf import OrfParser

# noinspection PyPep8Naming


class AT(PublisherEnum):
    ORF = PublisherSpec(
        domain="https://www.orf.at",
        sources=[RSSFeed("https://rss.orf.at/news.xml")],
        parser=OrfParser,
    )
