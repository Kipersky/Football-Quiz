import pytest
from project import get_player_nat, get_wikis, get_names

player_names = ['<a href="/wiki/Lionel_Messi" title="Lionel Messi">Lionel Messi</a>', '<a href="/wiki/Neymar" title="Neymar">Neymar</a>']

def test_get_player_nat():
    assert get_player_nat("https://en.wikipedia.org/wiki/Lionel_Messi") == "Argentina"
    assert get_player_nat("https://en.wikipedia.org/wiki/Neymar") == "Brazil"


def test_get_wikis():
    assert get_wikis(player_names) == ["/wiki/Lionel_Messi", "/wiki/Neymar"]

def test_get_names():
    assert get_names(player_names) == ["Lionel Messi", "Neymar"]