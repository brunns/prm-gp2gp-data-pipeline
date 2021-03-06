from datetime import timedelta
from typing import NamedTuple, Optional
from enum import Enum, auto

ERROR_SUPPRESSED = 15


class Transfer(NamedTuple):
    conversation_id: str
    sla_duration: Optional[timedelta]
    requesting_practice_ods: str
    sending_practice_ods: str
    error_code: Optional[int]
    pending: bool


class SlaBand(Enum):
    WITHIN_3_DAYS = auto()
    WITHIN_8_DAYS = auto()
    BEYOND_8_DAYS = auto()


class PracticeSlaMetrics(NamedTuple):
    ods: str
    within_3_days: int
    within_8_days: int
    beyond_8_days: int
