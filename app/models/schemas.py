
from typing import Literal

from pydantic import BaseModel, Field


class ComponentCreate(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    type: Literal[
        "server",
        "database",
        "api",
        "service",
        "application",
    ]
    criticality: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ] = "medium"


class Component(ComponentCreate):
    pass


class DependencyCreate(BaseModel):
    source_id: str = Field(..., min_length=1)
    target_id: str = Field(..., min_length=1)
