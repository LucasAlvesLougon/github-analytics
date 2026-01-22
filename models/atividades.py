from pydantic.dataclasses import dataclass


@dataclass
class Atividade:
    daily_activity: list[int] = None
    event_types: list[int] = None
    total_events: int = 0