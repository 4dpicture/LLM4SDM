from typing import List

from pydantic import BaseModel, Field, computed_field


class SDMItemAssessment(BaseModel):
    score: int = Field(..., ge=0, le=4, description="Score")
    evidence: str = Field(
        ..., description="Evidence quote(s)", max_length=300
    )
    justification: str = Field(
        ..., description="Justification", max_length=400
    )


class SDMAssessmentResponse(BaseModel):
    items: List[SDMItemAssessment] = Field(
        ..., min_length=12, max_length=12
    )

    @computed_field
    @property
    def mean(self) -> float:
        return sum(item.score for item in self.items) / len(self.items)
