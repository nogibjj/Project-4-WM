from mylib.logic import get_headlines

def test_get_headlines():
    assert len(get_headlines("soccer")) == 3