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


def test_missing_value_not_in_serialization():
    assert "MISSING" not in to_json(Cache())

@given(cache)
def test_cache_nmap_doesnt_explode(cache):
    cache.nmap(id, id)

# test_missing_value_not_in_serialization()
# test_cache_is_serializable()
# test_cache_nmap_doesnt_explode()
