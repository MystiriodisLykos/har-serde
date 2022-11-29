import json

from hypothesis import given, strategies as st, note
from serde.json import to_json
from serde.se import to_obj
from serde import to_dict

from harf_serde import Cache, BeforeAfterRequest, MISSING

missing = st.just(MISSING())
before_after = st.from_type(BeforeAfterRequest) | st.none() | missing
cache = st.builds(Cache, before_after, before_after)


@given(cache)
def test_cache_is_serializable(cache):
    to_json(cache)


@given(cache)
def test_cache_nmap_doesnt_explode(cache):
    cache.nmap(id, id)


def test_missing_value_not_in_serialization():
    assert "MISSING" not in to_json(Cache())


def test_harf_types_are_importable_from_harf():
    from harf_serde.harf import TimingsF
    from harf_serde.harf import BeforeAfterRequestF
    from harf_serde.harf import CacheF
    from harf_serde.harf import ContentF
    from harf_serde.harf import ResponseF
    from harf_serde.harf import ParamF
    from harf_serde.harf import PostDataF
    from harf_serde.harf import PostDataTextF
    from harf_serde.harf import PostDataParamF
    from harf_serde.harf import QueryStringF
    from harf_serde.harf import HeaderF
    from harf_serde.harf import CookieF
    from harf_serde.harf import RequestF
    from harf_serde.harf import EntryF
    from harf_serde.harf import PageTimingsF
    from harf_serde.harf import PageF
    from harf_serde.harf import BrowserF
    from harf_serde.harf import CreatorF
    from harf_serde.harf import LogF
    from harf_serde.harf import TopF
    from harf_serde.harf import FHar


def test_har_types_are_importable_from_har():
    from harf_serde.har import Timings
    from harf_serde.har import BeforeAfterRequest
    from harf_serde.har import Cache
    from harf_serde.har import Content
    from harf_serde.har import Response
    from harf_serde.har import Param
    from harf_serde.har import PostData
    from harf_serde.har import PostDataText
    from harf_serde.har import PostDataParam
    from harf_serde.har import QueryString
    from harf_serde.har import Header
    from harf_serde.har import Cookie
    from harf_serde.har import Request
    from harf_serde.har import Entry
    from harf_serde.har import PageTimings
    from harf_serde.har import Page
    from harf_serde.har import Browser
    from harf_serde.har import Creator
    from harf_serde.har import Log
    from harf_serde.har import Har


def test_morphisms_are_importable_from_morphism():
    from harf_serde.morphism import harf_cata
    from harf_serde.morphism import harf


def all_of_harf_is_importable_from_the_top_layer():
    from harf_serde import TimingsF
    from harf_serde import BeforeAfterRequestF
    from harf_serde import CacheF
    from harf_serde import ContentF
    from harf_serde import ResponseF
    from harf_serde import ParamF
    from harf_serde import PostDataF
    from harf_serde import PostDataTextF
    from harf_serde import PostDataParamF
    from harf_serde import QueryStringF
    from harf_serde import HeaderF
    from harf_serde import CookieF
    from harf_serde import RequestF
    from harf_serde import EntryF
    from harf_serde import PageTimingsF
    from harf_serde import PageF
    from harf_serde import BrowserF
    from harf_serde import CreatorF
    from harf_serde import LogF
    from harf_serde import TopF
    from harf_serde import FHar
    from harf_serde import Timings
    from harf_serde import BeforeAfterRequest
    from harf_serde import Cache
    from harf_serde import Content
    from harf_serde import Response
    from harf_serde import Param
    from harf_serde import PostData
    from harf_serde import PostDataText
    from harf_serde import PostDataParam
    from harf_serde import QueryString
    from harf_serde import Header
    from harf_serde import Cookie
    from harf_serde import Request
    from harf_serde import Entry
    from harf_serde import PageTimings
    from harf_serde import Page
    from harf_serde import Browser
    from harf_serde import Creator
    from harf_serde import Log
    from harf_serde import Har
    from harf_serde import harf_cata
    from harf_serde import harf
