from tempfile import tempdir

import pytest

from src.utils import random_string, random_uds


def test_random_string() -> None:
    assert set(random_string(charset="_")) == {"_"}

    assert len(random_string(length=16)) == 16
    with pytest.raises(ValueError, match=r"`length` should be greater than 0"):
        random_string(length=-1)

    with pytest.raises(ValueError, match=r"`length` should be greater than 0"):
        random_string(length=0)

    assert random_string(prefix="prefix-").startswith("prefix-")
    assert random_string(suffix="-suffix").endswith("-suffix")


def test_random_uds() -> None:
    uds = random_uds()
    assert uds.startswith(f"unix://{tempdir}/kkowa-")
    assert uds.endswith(".sock")
