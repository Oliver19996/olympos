from typing import Literal
from pydantic import BaseModel, Field, field_validator

AgeBand = Literal['20-24','25-29','30-34','35-39']
Gender = Literal['male','female']
Role = Literal['host','candidate']

class ParticipantIn(BaseModel):
    consent_version: str = 'phase0-v1'
    gender_identity: Gender
    target_gender: Gender
    age_band: AgeBand
    area: str = Field(min_length=1, max_length=40)
    role: Role
    required_age_bands: list[AgeBand]
    preferred_age_bands: list[AgeBand] = []
    availability: list[str] = Field(min_length=3, description='ISO time-slot IDs; at least 3')
    portrait_opt_in: bool = False

    @field_validator('target_gender')
    @classmethod
    def heterosexual_phase0(cls, value, info):
        own = info.data.get('gender_identity')
        if own and own == value:
            raise ValueError('Phase 0は異性間マッチングのみです')
        return value

class SurveyIn(BaseModel):
    participant_id: str
    participation_intent: int = Field(ge=1, le=5)
    payment_intent: int = Field(ge=1, le=5)
    price_plan: Literal['external-current','iap-baseline']
    usability_score: int = Field(ge=1, le=5)
    comment: str = Field(default='', max_length=1000)

class PortraitRequest(BaseModel):
    participant_id: str
    source_reference: str = Field(description='Phase 0では一時アップロード参照。画像本体をDBへ保存しない')

class PortraitDecision(BaseModel):
    approved: bool
    rejection_reason: str | None = Field(default=None, max_length=300)

class MatchGroup(BaseModel):
    course_type: Literal['MALE_HOST','FEMALE_HOST']
    display_name: Literal['ZEUS','APHRODITE']
    host_id: str
    candidate_ids: list[str]
    shared_slots: list[str]

class SimulationResult(BaseModel):
    run_id: str
    applications: int
    assigned: int
    formation_rate: float
    groups: list[MatchGroup]
