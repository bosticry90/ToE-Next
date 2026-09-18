"""Fail-closed errors for the verified calculator trusted core."""
from __future__ import annotations


class CalculatorError(ValueError):
    """A deterministic validation or verification failure.

    ``code`` is stable and suitable for receipts.  The optional ``location``
    identifies a contract field, node, source, or output without putting an
    implementation traceback into canonical evidence.
    """

    def __init__(self, code: str, location: str = "", detail: str = "") -> None:
        self.code = code
        self.location = location
        self.detail = detail
        message = code
        if location:
            message += f":{location}"
        if detail:
            message += f":{detail}"
        super().__init__(message)


def require(condition: bool, code: str, location: str = "", detail: str = "") -> None:
    if not condition:
        raise CalculatorError(code, location, detail)
