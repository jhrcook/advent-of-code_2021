"""General utilities."""

from dataclasses import dataclass
from typing import NoReturn


def assert_never(value: NoReturn) -> NoReturn:
    """Force runtime and static enumeration exhaustiveness.

    Args:
        value (NoReturn): Some value passed as an enum value.

    Returns:
        NoReturn: Nothing.
    """
    assert False, f"Unhandled value: {value} ({type(value).__name__})"  # noqa: B011


@dataclass(frozen=True)
class PuzzleInfo:
    """Information for a day's puzzle."""

    day: int
    title: str

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"Day {self.day}: {self.title}"

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)
