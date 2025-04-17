from pydantic import BaseModel
from typing import Optional, List, Dict


class GeneratePayload(BaseModel):
    topic: str


class AnalysisPayload(BaseModel):
    content: str
