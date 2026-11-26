from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict

class PolicyMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    version: str = Field(min_length=1)
    category: str = Field(min_length=1)

    effective_from: date

    status: Literal["active", "draft", "archived"]

    source_path: str = Field(min_length=1)


class PolicyDocument(BaseModel):
    metadata: PolicyMetadata

    content: str = Field(min_length=1)

    content_hash: str = Field(min_length=64, max_length=64)

    

