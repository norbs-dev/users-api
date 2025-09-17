from pydantic import BaseModel, field_validator

class TeamInsight(BaseModel):
    name: str
    total_members: int
    leaders: int
    completed_projects: int
    active_percentage: float

    @field_validator("active_percentage")
    def round_active_percentage(cls, value):
        return round(value, 2)