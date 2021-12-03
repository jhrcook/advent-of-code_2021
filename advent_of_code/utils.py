"""General utilities."""

from typing import NoReturn


def assert_never(value: NoReturn) -> NoReturn:
    """Force runtime and static enumeration exhaustiveness.

    Args:
        value (NoReturn): Some value passed as an enum value.

    Returns:
        NoReturn: Nothing.
    """
    assert False, f"Unhandled value: {value} ({type(value).__name__})"  # noqa: B011
