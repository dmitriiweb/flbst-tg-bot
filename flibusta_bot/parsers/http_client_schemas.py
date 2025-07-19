from __future__ import annotations

import io
from dataclasses import asdict, dataclass


@dataclass
class Serializable:
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Serializable:
        return cls(**data)


@dataclass
class HttpResponse(Serializable):
    status_code: int
    content: str
    headers: dict
    url: str


@dataclass
class BinaryHttpResponse:
    status_code: int
    content: io.BytesIO
    headers: dict
    url: str
