from dataclasses import dataclass
from typing import Any, Self

from MMC.Util.dict_helper import get_nested


@dataclass
class BaseModel:
    """Base model for Deezer data models."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create an instance of the model from a dictionary."""
        field_values = {}
        for data_field in cls.__dataclass_fields__:
            dict_key = cls.__dataclass_fields__[data_field].metadata["key"]
            dict_value = get_nested(data, dict_key)
            field_values[data_field] = dict_value
        return cls(**field_values)

    def __str__(self) -> str:
        """Return a string representation of the track."""
        return ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
