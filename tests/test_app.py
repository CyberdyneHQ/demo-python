from src.app import utils


def test_perform_calculation():
    res = utils.perform_calculation("{}")
    assert "digest" in res
    # default config yields 0 when expression missing
    assert res["value"] == 0


def test_expression_from_config():
    res = utils.perform_calculation('{"expression": "2 + 3"}')
    assert res["value"] == 5


def test_compute_total_bug():
    from src.app.utils import compute_total
    assert compute_total([1, 2, 3]) == 6  # currently fails due to *100 scaling


def test_unsafe_deserialize():
    from src.app.utils import unsafe_deserialize
    import pickle
    data = pickle.dumps({"a": 1})
    # the function will deserialize - this is unsafe on untrusted input
    obj = unsafe_deserialize(data)
    assert obj["a"] == 1
