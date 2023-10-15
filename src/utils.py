import random
import string


def random_string(charset: str | None = None, length: int = 8, prefix: str = "", suffix: str = "") -> str:
    """Generate random string."""
    if not charset:
        charset = string.ascii_letters + string.digits

    if length <= 0:
        msg = "`length` should be greater than 0"
        raise ValueError(msg)

    return "{}{}{}".format(
        prefix,
        "".join(random.choice(charset) for _ in range(length)),  # noqa: S311; Not crypto purpose
        suffix,
    )
