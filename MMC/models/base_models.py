from dataclasses import dataclass
from typing import Any, Self

from mmc.utils.dict_helper import get_nested


@dataclass
class BaseModel:
    """Base model for Deezer data models."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create an instance of the model from a dictionary.

        Raises:
            KeyError: If a required key is not found in the input data.

        """
        field_values = {}
        for data_field in cls.__dataclass_fields__:
            dict_key = cls.__dataclass_fields__[data_field].metadata["key"]
            try:
                dict_value = get_nested(data, dict_key)
            except KeyError as err:
                msg = f"Key '{dict_key}' not found in data for field '{data_field}'. "
                raise KeyError(msg) from err
            field_values[data_field] = dict_value
        return cls(**field_values)

    def __str__(self) -> str:
        """Return a string representation of the track."""
        return ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
