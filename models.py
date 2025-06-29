from dataclasses import dataclass
from datetime import datetime

@dataclass
class Claim:
    title: str
    verdict: str
    summary: str
    url: str
    date: datetime
    source: str