"""
Singleton metaclass implementations for service management.
"""
from abc import ABCMeta
from typing import Any, ClassVar, Dict


class SingletonABCMeta(ABCMeta):
    """Singleton metaclass for ABC classes."""
    _instances: ClassVar[Dict[type, object]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(type):
    """Singleton metaclass for regular classes."""
    _instances: ClassVar[Dict[type, object]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
