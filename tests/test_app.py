from src.app import utils


def test_perform_calculation():
    res = utils.perform_calculation("{}")
    assert "digest" in res
    # default config yields 0 when expression missing
    assert res["value"] == 0


def test_expression_from_config():
    res = utils.perform_calculation('{"expression": "2 + 3"}')
    assert res["value"] == 5
