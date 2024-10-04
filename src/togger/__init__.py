"""
from togger import debug

debug"this is a debug log message using {debug!r}"
"""
from __future__ import annotations

import logging
import sys
from functools import partial, wraps
from typing import Any, Decoded, Interpolation


def _make_log(name: str, level: int) -> callable[..., None]:
    logger = logging.getLogger(name)
    # I want pretty func reprs
    levelname = logging.getLevelName(level).lower()
    func = getattr(logger, levelname, logger.log)

    @wraps(func)
    def _log(*args: Decoded | Interpolation) -> None:
        if not logger.isEnabledFor(level):
            return None  # NO-OP

        result = []
        for arg in args:
            match arg:
                case Decoded() as decoded:
                    result.append(decoded)
                case Interpolation() as interpolation:
                    value = interpolation.getvalue()
                    if not isinstance(value, str):
                        value = str(value)
                    result.append(value)
        logger.log(level, ''.join(result))

    return _log


def __getattr__(name: str) -> Any:
    name_to_level = logging.getLevelNamesMapping()
    level_name = name.upper()
    caller = sys._getframemodulename(1)
    if name == "log":
        return partial(_make_log, caller)
    level: int | None = name_to_level.get(level_name)
    if level is not None:
        return _make_log(caller, level)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return [*[name.lower() for name in logging.getLevelNamesMapping()], "log"]