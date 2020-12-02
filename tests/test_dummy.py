import pytest


@pytest.mark.parametrize(
    ("fst", "snd", "expected"),
    [
        (1, 2, 3),
        (-20, 7, -13),
    ],
)
def test_add(fst, snd, expected):
    assert fst + snd == expected
