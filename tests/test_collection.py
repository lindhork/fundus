import pytest

from fundus.publishers.base_objects import (
    PublisherCollectionMeta,
    PublisherEnum,
    PublisherSpec,
)


class TestCollection:
    def test_iter_empty_collection(self, empty_collection):
        assert list(empty_collection) == []

    def test_iter_collection_with_empty_publisher_enum(self, collection_with_empty_publisher_enum):
        assert list(collection_with_empty_publisher_enum) == []

    def test_iter_collection_with_publisher_enum(self, collection_with_validate_publisher_enum):
        assert list(collection_with_validate_publisher_enum) == [collection_with_validate_publisher_enum.pub.value]

    def test_publisher_enum_with_wrong_enum_value(self):
        with pytest.raises(ValueError):

            class PublisherEnumWithWrongValue(PublisherEnum):
                value = "Enum"

    def test_publisher_spec_without_source(self, empty_parser_proxy):
        with pytest.raises(ValueError):
            PublisherSpec(domain="https//:test.com/", parser=empty_parser_proxy)

    def test_duplicate_publisher_names_in_same_collection(self, publisher_enum_with_news_map):
        with pytest.raises(AttributeError):

            class Test(metaclass=PublisherCollectionMeta):
                a = publisher_enum_with_news_map
                b = publisher_enum_with_news_map

    def test_supports(self, publisher_enum_with_news_map):
        assert publisher_enum_with_news_map.value.supports("news")
        assert not publisher_enum_with_news_map.value.supports("sitemap")
        assert not publisher_enum_with_news_map.value.supports("rss")
        with pytest.raises(ValueError):
            publisher_enum_with_news_map.value.supports("")

    def test_search(self, publisher_enum_with_news_map, proxy_with_two_versions_and_different_attrs):
        proxy = proxy_with_two_versions_and_different_attrs()
        publisher_enum_with_news_map.value.parser = proxy

        latest, earlier = proxy.attribute_mapping.values()

        assert len(publisher_enum_with_news_map.search(latest.names)) == 1
        assert len(publisher_enum_with_news_map.search(earlier.names)) == 0

        with pytest.raises(AssertionError):
            publisher_enum_with_news_map.search([])
            publisher_enum_with_news_map.search()
