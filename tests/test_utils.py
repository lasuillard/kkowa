import pytest

from src.utils import random_string


def test_random_string() -> None:
    assert set(random_string(charset="_")) == {"_"}

    assert len(random_string(length=16)) == 16
    with pytest.raises(ValueError, match=r"`length` should be greater than 0"):
        random_string(length=-1)

    with pytest.raises(ValueError, match=r"`length` should be greater than 0"):
        random_string(length=0)

    assert random_string(prefix="prefix-").startswith("prefix-")
    assert random_string(suffix="-suffix").endswith("-suffix")
