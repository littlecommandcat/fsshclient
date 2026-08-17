from dataclasses import dataclass, asdict

@dataclass
class News:
    title: str
    unitname: str
    clicks: int
    time: str
    id: int

    def to_dict(self):
        return asdict(self)

@dataclass
class PageInfo:
    num: int
    rows: int
    total: int

    def to_dict(self):
        return asdict(self)