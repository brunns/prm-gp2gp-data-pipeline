from typing import NamedTuple
from datetime import timedelta


class Transfer(NamedTuple):
    conversation_id: str
    sla_duration: timedelta
